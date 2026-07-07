import os
from datetime import date, datetime
import csv
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, Response
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from config import Config, BASE_DIR
from extensions import db
from models import Abonnement, Coupure, Notification, Signalement
from processing.real_data import is_real_source
from services.analytics_service import average_duration_by, get_kpis, group_count, map_points
from services.data_quality_service import get_data_quality_report
from services.model_card_service import build_model_card
from services.model_metrics_service import load_model_metrics
from services.model_predictions_service import get_model_predictions_report
from services.pipeline_service import list_pipeline_runs
from services.prediction_service import DEFAULT_INPUT, run_prediction
from services.recommendation_service import build_zone_recommendations
from services.source_traceability_service import get_source_traceability


def is_real_row(row):
    return is_real_source(row.get('source_type'), row.get('source_name'))


def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date() if value else None


def parse_time(value):
    return datetime.strptime(value, '%H:%M').time() if value else None


def normalized(value):
    return value.strip().title() if value else None


def request_payload_values():
    payload = request.get_json(silent=True)
    if isinstance(payload, dict):
        return payload

    raw_body = request.get_data(cache=True)
    if raw_body:
        for encoding in ('utf-8-sig', 'utf-16', 'latin-1'):
            try:
                decoded = raw_body.decode(encoding).strip()
                if not decoded:
                    continue
                payload = json.loads(decoded)
                if isinstance(payload, dict):
                    return payload
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

    if request.form:
        return request.form
    return request.args


def ensure_runtime_schema():
    db.create_all()
    engine_name = db.engine.url.get_backend_name()
    if engine_name.startswith('postgresql'):
        statements = [
            "ALTER TABLE notifications ADD COLUMN IF NOT EXISTS id_abonnement INT REFERENCES abonnements(id_abonnement)",
            "ALTER TABLE notifications ADD COLUMN IF NOT EXISTS destinataire VARCHAR(120)",
            "CREATE TABLE IF NOT EXISTS pipeline_runs (id_run SERIAL PRIMARY KEY, pipeline_name VARCHAR(120) NOT NULL, date_start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, date_end TIMESTAMP, status VARCHAR(40) NOT NULL DEFAULT 'running', records_read INT DEFAULT 0, records_inserted INT DEFAULT 0, records_rejected INT DEFAULT 0, error_message TEXT)",
            "CREATE INDEX IF NOT EXISTS idx_abonnements_region ON abonnements(region)",
            "CREATE INDEX IF NOT EXISTS idx_notifications_date ON notifications(date_envoi)",
            "CREATE INDEX IF NOT EXISTS idx_pipeline_runs_date ON pipeline_runs(date_start)",
        ]
        for statement in statements:
            db.session.execute(text(statement))
        db.session.commit()
    elif engine_name.startswith('sqlite'):
        notification_columns = {
            row[1]
            for row in db.session.execute(text("PRAGMA table_info(notifications)")).fetchall()
        }
        if 'id_abonnement' not in notification_columns:
            db.session.execute(text("ALTER TABLE notifications ADD COLUMN id_abonnement INTEGER"))
        if 'destinataire' not in notification_columns:
            db.session.execute(text("ALTER TABLE notifications ADD COLUMN destinataire VARCHAR(120)"))
        db.session.commit()


def notification_matches(coupure, abonnement):
    if not abonnement.actif:
        return False
    checks = (
        (abonnement.region, coupure.region),
        (abonnement.ville, coupure.ville),
        (abonnement.zone, coupure.zone),
    )
    return all(not expected or (actual or '').lower() == expected.lower() for expected, actual in checks)


def build_alert_message(coupure):
    debut = f"{coupure.date_debut} à {coupure.heure_debut.strftime('%H:%M') if coupure.heure_debut else 'heure non précisée'}"
    lieu = ', '.join(x for x in [coupure.region, coupure.ville, coupure.zone] if x)
    return f"Alerte coupure {coupure.statut or 'prévue'} : {lieu} le {debut}. Source : {coupure.source_name or 'WattWatcher BF'}."


def generate_notifications_for_coupure(coupure):
    created = 0
    for abonnement in Abonnement.query.filter_by(actif=True).all():
        if not notification_matches(coupure, abonnement):
            continue
        exists = Notification.query.filter_by(id_coupure=coupure.id_coupure, id_abonnement=abonnement.id_abonnement).first()
        if exists:
            continue
        db.session.add(Notification(
            id_coupure=coupure.id_coupure,
            id_abonnement=abonnement.id_abonnement,
            message=build_alert_message(coupure),
            canal=abonnement.canal,
            destinataire=abonnement.contact,
            statut_envoi='simulée',
        ))
        created += 1
    return created


def filtered_coupures_query():
    query = Coupure.query
    for field in ('region', 'ville', 'zone', 'statut'):
        value = request.args.get(field)
        if value:
            query = query.filter(getattr(Coupure, field).ilike(f'%{value}%'))
    today_only = request.args.get('aujourdhui') == '1'
    if today_only:
        query = query.filter(Coupure.date_debut == date.today())
    return query.order_by(Coupure.date_debut.desc(), Coupure.heure_debut.desc())


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template(
            'index.html',
            kpis=get_kpis(),
            by_region=group_count('region')[:8],
            by_month=group_count('mois'),
            by_source=group_count('source_type'),
            by_status=group_count('statut'),
            by_type=group_count('type_coupure'),
            map_points=map_points(),
        )

    @app.route('/suivi')
    def suivi():
        items = filtered_coupures_query().limit(300).all()
        active_items = [c for c in items if (c.statut or '').lower() in ('prévue', 'en cours')]
        return render_template('suivi.html', coupures=items, active_coupures=active_items, filters=request.args)

    @app.route('/carte')
    def carte():
        points = map_points()
        return render_template('carte.html', map_points=points)

    @app.route('/coupures', methods=['GET', 'POST'])
    def coupures():
        if request.method == 'POST':
            date_debut = parse_date(request.form.get('date_debut'))
            c = Coupure(
                date_debut=date_debut,
                heure_debut=parse_time(request.form.get('heure_debut')),
                date_fin=parse_date(request.form.get('date_fin')),
                heure_fin=parse_time(request.form.get('heure_fin')),
                duree_minutes=int(request.form.get('duree_minutes') or 0),
                annee=date_debut.year if date_debut else None,
                mois=date_debut.month if date_debut else None,
                region=normalized(request.form.get('region')), ville=normalized(request.form.get('ville')), zone=normalized(request.form.get('zone')),
                type_coupure=request.form.get('type_coupure'), cause=request.form.get('cause'), statut=request.form.get('statut') or 'prévue',
                source_name=request.form.get('source_name') or 'Saisie admin', source_type='interne', niveau_confiance=0.75,
                niveau_impact=request.form.get('niveau_impact') or 'moyen'
            )
            db.session.add(c)
            db.session.flush()
            nb_alertes = generate_notifications_for_coupure(c)
            db.session.commit()
            flash(f'Coupure ajoutée avec succès. {nb_alertes} alerte(s) générée(s).', 'success')
            return redirect(url_for('coupures'))
        items = Coupure.query.order_by(Coupure.date_debut.desc()).limit(200).all()
        return render_template('coupures.html', coupures=items)

    @app.route('/signalements', methods=['GET', 'POST'])
    def signalements():
        if request.method == 'POST':
            sig = Signalement(
                nom_signalant=request.form.get('nom_signalant'), telephone=request.form.get('telephone'),
                region=normalized(request.form.get('region')), ville=normalized(request.form.get('ville')), zone=normalized(request.form.get('zone')),
                date_signalement=parse_date(request.form.get('date_signalement')),
                heure_debut=parse_time(request.form.get('heure_debut')), heure_fin=parse_time(request.form.get('heure_fin')),
                description=request.form.get('description')
            )
            db.session.add(sig); db.session.commit(); flash('Signalement enregistré.', 'success')
            return redirect(url_for('signalements'))
        return render_template('signalements.html', signalements=Signalement.query.order_by(Signalement.created_at.desc()).limit(100).all())

    @app.route('/notifications', methods=['GET', 'POST'])
    def notifications():
        if request.method == 'POST':
            abonnement = Abonnement(
                nom=request.form.get('nom'), contact=request.form.get('contact'), canal=request.form.get('canal') or 'web',
                region=normalized(request.form.get('region')), ville=normalized(request.form.get('ville')), zone=normalized(request.form.get('zone'))
            )
            db.session.add(abonnement)
            db.session.commit()
            flash('Abonnement aux alertes enregistré.', 'success')
            return redirect(url_for('notifications'))
        abonnements = Abonnement.query.order_by(Abonnement.created_at.desc()).limit(100).all()
        alerts = Notification.query.order_by(Notification.date_envoi.desc()).limit(100).all()
        return render_template('notifications.html', abonnements=abonnements, notifications=alerts)

    @app.route('/recommandations')
    def recommandations():
        region = request.args.get('region')
        zone = request.args.get('zone')
        recommandations_data = build_zone_recommendations(region=region, zone=zone)
        return render_template('recommandations.html', kpis=get_kpis(), top_zones=group_count('zone')[:5], recommandations=recommandations_data, filters=request.args)

    @app.route('/qualite')
    def qualite():
        return render_template('qualite.html', report=get_data_quality_report())

    @app.route('/sources')
    def sources():
        return render_template('sources.html', traceability=get_source_traceability())

    @app.route('/modele')
    def modele():
        return render_template('modele.html', metrics=load_model_metrics())

    @app.route('/modele/fiche')
    def modele_fiche():
        return render_template('modele_fiche.html', card=build_model_card())

    @app.route('/modele/erreurs')
    def modele_erreurs():
        return render_template('modele_erreurs.html', report=get_model_predictions_report())

    @app.route('/prediction', methods=['GET', 'POST'])
    def prediction():
        result = None
        form_values = {**DEFAULT_INPUT}
        if request.method == 'POST':
            form_values.update(request.form.to_dict())
            result = run_prediction(request.form)
        return render_template('prediction.html', form_values=form_values, result=result)

    @app.route('/pipeline')
    def pipeline():
        return render_template('pipeline.html', runs=list_pipeline_runs())


    @app.route('/favicon.ico')
    def favicon():
        return Response(status=204)
    @app.route('/api/coupures')
    def api_coupures():
        items = filtered_coupures_query().limit(500).all()
        return jsonify([{'id': c.id_coupure, 'date_debut': c.date_debut.isoformat() if c.date_debut else None, 'heure_debut': c.heure_debut.strftime('%H:%M') if c.heure_debut else None, 'region': c.region, 'ville': c.ville, 'zone': c.zone, 'statut': c.statut, 'duree_minutes': c.duree_minutes, 'type_coupure': c.type_coupure, 'source': c.source_name} for c in items])

    @app.route('/api/stats')
    def api_stats():
        return jsonify({
            'kpis': get_kpis(),
            'par_region': group_count('region'),
            'par_zone': group_count('zone')[:10],
            'par_source': group_count('source_type'),
            'par_statut': group_count('statut'),
            'par_type': group_count('type_coupure'),
            'duree_moyenne_region': average_duration_by('region'),
            'carte_points': map_points(),
        })

    @app.route('/api/map-points')
    def api_map_points():
        return jsonify(map_points())

    @app.route('/api/data-quality')
    def api_data_quality():
        return jsonify(get_data_quality_report())

    @app.route('/api/source-traceability')
    def api_source_traceability():
        return jsonify(get_source_traceability())

    @app.route('/api/model-metrics')
    def api_model_metrics():
        return jsonify(load_model_metrics())

    @app.route('/api/model-card')
    def api_model_card():
        return jsonify(build_model_card())

    @app.route('/api/model-predictions')
    def api_model_predictions():
        return jsonify(get_model_predictions_report())

    @app.route('/api/predict-duration', methods=['POST'])
    def api_predict_duration():
        values = request_payload_values()
        return jsonify(run_prediction(values))

    @app.route('/api/pipeline-runs')
    def api_pipeline_runs():
        return jsonify(list_pipeline_runs())

    @app.route('/notifications/simuler')
    def simuler_notification():
        coupure = Coupure.query.filter(Coupure.statut.in_(['prévue', 'en cours'])).order_by(Coupure.date_debut.desc()).first()
        if not coupure:
            flash('Aucune coupure prévue ou en cours pour générer une alerte.', 'warning')
            return redirect(url_for('notifications'))
        nb_alertes = generate_notifications_for_coupure(coupure)
        db.session.commit()
        flash(f'{nb_alertes} alerte(s) simulée(s) générée(s).', 'warning')
        return redirect(url_for('notifications'))

    return app


def load_sample_if_empty(app):
    with app.app_context():
        try:
            ensure_runtime_schema()
            if Coupure.query.count() == 0:
                csv_path = BASE_DIR / 'data' / 'final' / 'dataset_coupures_2020_2026.csv'
                with csv_path.open(newline='', encoding='utf-8') as file:
                    for row in csv.DictReader(file):
                        if not is_real_row(row):
                            continue
                        db.session.add(Coupure(
                            date_publication=parse_date(row['date_publication']), date_debut=parse_date(row['date_debut']), heure_debut=parse_time(row['heure_debut'][:5]),
                            date_fin=parse_date(row['date_fin']), heure_fin=parse_time(row['heure_fin'][:5]), duree_minutes=int(row['duree_minutes']),
                            annee=int(row['annee']), mois=int(row['mois']), jour_semaine=row['jour_semaine'], periode_journee=row['periode_journee'],
                            region=row['region'], province=row['province'], ville=row['ville'], zone=row['zone'], latitude=float(row['latitude']), longitude=float(row['longitude']),
                            type_coupure=row['type_coupure'], cause=row['cause'], statut=row['statut'], source_name=row['source_name'], source_type=row['source_type'], url_source=row['url_source'],
                            niveau_confiance=float(row['niveau_confiance']), niveau_impact=row['niveau_impact'], temperature_max=float(row['temperature_max']), precipitation=float(row['precipitation']), irradiation_solaire=float(row['irradiation_solaire'])
                        ))
                db.session.commit(); print('Dataset exemple chargé.')
        except OperationalError as exc:
            print('Connexion PostgreSQL impossible. Lance docker compose up -d ou vérifie DATABASE_URL.'); print(exc)

app = create_app()
if __name__ == '__main__':
    load_sample_if_empty(app)
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes')
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    app.run(debug=debug_mode, host=host, port=port)

