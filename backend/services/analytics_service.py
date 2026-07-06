from sqlalchemy import func
from extensions import db
from models import Coupure

def get_kpis():
    total = db.session.query(func.count(Coupure.id_coupure)).scalar() or 0
    avg_duration = db.session.query(func.avg(Coupure.duree_minutes)).scalar() or 0
    max_duration = db.session.query(func.max(Coupure.duree_minutes)).scalar() or 0
    total_duration = db.session.query(func.sum(Coupure.duree_minutes)).scalar() or 0
    durations = [row[0] for row in db.session.query(Coupure.duree_minutes).filter(Coupure.duree_minutes.isnot(None)).order_by(Coupure.duree_minutes).all()]
    median_duration = 0
    if durations:
        mid = len(durations) // 2
        median_duration = durations[mid] if len(durations) % 2 else (durations[mid - 1] + durations[mid]) / 2
    zones = db.session.query(func.count(func.distinct(Coupure.zone))).scalar() or 0
    active = Coupure.query.filter(Coupure.statut.in_(['prévue', 'en cours'])).count()
    return {
        'total_coupures': total,
        'duree_moyenne': round(float(avg_duration), 2),
        'duree_mediane': round(float(median_duration), 2),
        'duree_max': int(max_duration or 0),
        'duree_totale': int(total_duration or 0),
        'zones_suivies': zones,
        'coupures_actives': int(active),
    }

def group_count(field_name):
    field = getattr(Coupure, field_name)
    rows = db.session.query(field, func.count(Coupure.id_coupure)).group_by(field).order_by(func.count(Coupure.id_coupure).desc()).all()
    return [{'label': str(r[0] or 'Non renseigné'), 'value': int(r[1])} for r in rows]

def average_duration_by(field_name):
    field = getattr(Coupure, field_name)
    rows = db.session.query(field, func.avg(Coupure.duree_minutes)).group_by(field).order_by(func.avg(Coupure.duree_minutes).desc()).all()
    return [{'label': str(r[0] or 'Non renseigné'), 'value': round(float(r[1] or 0), 2)} for r in rows]

def map_points(limit=200):
    rows = (
        db.session.query(
            Coupure.region,
            Coupure.ville,
            Coupure.zone,
            func.avg(Coupure.latitude),
            func.avg(Coupure.longitude),
            func.count(Coupure.id_coupure),
            func.avg(Coupure.duree_minutes),
            func.max(Coupure.date_debut),
        )
        .filter(Coupure.latitude.isnot(None), Coupure.longitude.isnot(None))
        .group_by(Coupure.region, Coupure.ville, Coupure.zone)
        .order_by(func.count(Coupure.id_coupure).desc())
        .limit(limit)
        .all()
    )
    return [
        {
            'region': row[0] or 'Non renseigné',
            'ville': row[1] or 'Non renseigné',
            'zone': row[2] or 'Non renseigné',
            'latitude': round(float(row[3]), 6),
            'longitude': round(float(row[4]), 6),
            'nb_coupures': int(row[5] or 0),
            'duree_moyenne': round(float(row[6] or 0), 2),
            'derniere_coupure': row[7].isoformat() if row[7] else None,
        }
        for row in rows
    ]
