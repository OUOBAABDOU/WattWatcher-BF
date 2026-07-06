import os
import sys
import json

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
sys.path.insert(0, "backend")

import app as watt_app


def test_web_pages_and_api_endpoints_load():
    watt_app.load_sample_if_empty(watt_app.app)

    client = watt_app.app.test_client()
    for path in (
        "/",
        "/suivi",
        "/carte",
        "/coupures",
        "/signalements",
        "/notifications",
        "/recommandations",
        "/qualite",
        "/sources",
        "/modele",
        "/modele/fiche",
        "/modele/erreurs",
        "/prediction",
        "/pipeline",
        "/api/stats",
        "/api/coupures",
        "/api/map-points",
        "/api/data-quality",
        "/api/source-traceability",
        "/api/model-metrics",
        "/api/model-card",
        "/api/model-predictions",
        "/api/pipeline-runs",
    ):
        response = client.get(path)
        assert response.status_code == 200


def test_sample_loader_excludes_simulation_rows():
    watt_app.load_sample_if_empty(watt_app.app)

    with watt_app.app.app_context():
        assert watt_app.Coupure.query.filter_by(source_type='simulation').count() == 0
        assert watt_app.Coupure.query.count() >= 327


def test_stats_api_exposes_advanced_dashboard_metrics():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    data = client.get('/api/stats').get_json()

    assert 'duree_mediane' in data['kpis']
    assert 'duree_totale' in data['kpis']
    assert 'coupures_actives' in data['kpis']
    assert 'par_source' in data
    assert 'par_statut' in data
    assert 'par_type' in data
    assert 'carte_points' in data


def test_map_points_api_exposes_geographic_zones():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    data = client.get('/api/map-points').get_json()

    assert data
    assert {'latitude', 'longitude', 'zone', 'nb_coupures', 'duree_moyenne'}.issubset(data[0])


def test_map_page_contains_real_map_and_table():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    response = client.get('/carte')
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'Carte des zones touchées' in html
    assert 'page-map' in html
    assert 'scattergeo' in html


def test_model_metrics_page_and_api_expose_real_training_results():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    page = client.get('/modele')
    data = client.get('/api/model-metrics').get_json()

    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert 'Modèle prédictif ML' in html
    assert 'Comparaison des variantes' in html
    assert 'Distribution des classes' in html
    assert data['available'] is True
    assert 'classification' in data
    assert 'regression' in data
    assert data['comparison']['variants']
    assert data['comparison']['best_by_macro_f1'] in ('standard', 'balanced')
    assert data['feature_importance']['available'] is True
    assert data['feature_importance']['regression']
    assert data['dataset']['real_only'] is True
    assert data['dataset']['class_distribution']
    assert data['dataset']['class_balance']['imbalance_ratio'] >= 1
    assert data['dataset']['duration_stats']


def test_model_card_page_and_api_expose_report_ready_markdown():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    page = client.get('/modele/fiche')
    data = client.get('/api/model-card').get_json()

    assert page.status_code == 200
    assert 'Fiche modèle ML' in page.get_data(as_text=True)
    assert data['available'] is True
    assert data['summary']['usable_rows'] >= 327
    assert data['summary']['misclassified_rows'] == 32
    assert data['summary']['class_distribution']
    assert data['summary']['class_balance']['imbalance_ratio'] >= 1
    assert data['summary']['duration_stats']
    assert data['error_analysis']['worst_errors']
    assert data['error_analysis']['confidence_summary']
    assert '## Comparaison des variantes' in data['markdown']
    assert '## Distribution des classes' in data['markdown']
    assert '## Déséquilibre des classes' in data['markdown']
    assert '## Variables les plus importantes' in data['markdown']
    assert '## Analyse des erreurs de test' in data['markdown']
    assert '### Fiabilite par niveau de confiance' in data['markdown']


def test_model_predictions_page_and_api_expose_test_errors():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    page = client.get('/modele/erreurs')
    data = client.get('/api/model-predictions').get_json()

    assert page.status_code == 200
    assert 'Erreurs du modèle ML' in page.get_data(as_text=True)
    assert data['available'] is True
    assert data['summary']['rows'] == 66
    assert data['confidence_summary']
    assert data['worst_errors']
    assert {'actual_duration', 'predicted_duration', 'absolute_error'}.issubset(data['worst_errors'][0])
    assert 'predicted_class_confidence' in data['misclassified'][0]
    assert data['misclassified'][0]['confidence_level'] in ('faible', 'moyenne', 'elevee', 'inconnu')
    assert data['misclassified'][0]['confidence_level_label'] in ('faible', 'moyenne', 'élevée', 'inconnu')


def test_source_traceability_page_and_api_expose_real_files():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    page = client.get('/sources')
    data = client.get('/api/source-traceability').get_json()

    assert page.status_code == 200
    assert 'Traçabilité des sources' in page.get_data(as_text=True)
    assert data['kpis']['combined_rows'] >= 327
    assert data['seeds']
    assert any(item['path'].endswith('dataset_coupures_reelles_combine.csv') for item in data['files'])


def test_prediction_page_and_api_return_model_result():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()
    payload = {
        'region': 'Centre',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
        'type_coupure': 'prévue',
        'mois': 3,
        'heure_num': 8,
        'jour_num': 1,
        'temperature_max': 38,
        'precipitation': 0,
        'irradiation_solaire': 5.8,
        'model_variant': 'balanced',
    }

    page = client.post('/prediction', data=payload)
    data = client.post('/api/predict-duration', json=payload).get_json()

    assert page.status_code == 200
    assert 'Durée estimée' in page.get_data(as_text=True)
    assert data['available'] is True
    assert data['model_variant'] == 'balanced'
    assert data['model_path'].endswith('model_real_balanced.pkl')
    assert data['prediction']['duree_minutes'] > 0
    assert data['prediction']['classe_duree'] in ('courte', 'moyenne', 'longue')
    assert data['prediction']['classe_confiance'] is not None
    assert data['prediction']['classe_proba']
    assert data['prediction']['niveau_confiance'] in ('faible', 'moyenne', 'élevée')
    assert data['prediction']['message_decision']


def test_prediction_api_accepts_raw_utf16_json_body():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()
    payload = {
        'region': 'Centre',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
        'type_coupure': 'prévue',
        'mois': 7,
        'heure_num': 8,
        'jour_num': 4,
        'temperature_max': 36,
        'precipitation': 0,
        'irradiation_solaire': 5.5,
        'model_variant': 'standard',
    }

    data = client.post(
        '/api/predict-duration',
        data=json.dumps(payload, ensure_ascii=False).encode('utf-16'),
        content_type='application/json',
    ).get_json()

    assert data['model_variant'] == 'standard'
    assert data['model_path'].endswith('model_real.pkl')
    assert data['features']['temperature_max'] == 36.0
    assert data['features']['irradiation_solaire'] == 5.5


def test_subscription_generates_notification_for_matching_cut():
    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    response = client.post('/notifications', data={
        'nom': 'Test',
        'contact': 'test@example.com',
        'canal': 'email',
        'region': 'Centre',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/coupures', data={
        'region': 'Centre',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
        'date_debut': '2026-07-10',
        'heure_debut': '08:00',
        'date_fin': '2026-07-10',
        'heure_fin': '10:00',
        'duree_minutes': '120',
        'type_coupure': 'prévue',
        'statut': 'prévue',
        'niveau_impact': 'moyen',
        'source_name': 'Test',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'alerte' in response.get_data(as_text=True).lower()
