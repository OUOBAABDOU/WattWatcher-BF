from pathlib import Path
import sys

sys.path.insert(0, 'backend')

import app as watt_app


PAGES = {
    'index.html': '/',
    'suivi.html': '/suivi',
    'carte.html': '/carte',
    'coupures.html': '/coupures',
    'recommandations.html': '/recommandations',
    'qualite.html': '/qualite',
    'sources.html': '/sources',
    'modele.html': '/modele',
    'modele_fiche.html': '/modele/fiche',
    'modele_erreurs.html': '/modele/erreurs',
    'prediction.html': '/prediction',
    'pipeline.html': '/pipeline',
    'api_stats.json': '/api/stats',
    'api_coupures.json': '/api/coupures',
    'api_map_points.json': '/api/map-points',
    'api_data_quality.json': '/api/data-quality',
    'api_source_traceability.json': '/api/source-traceability',
    'api_model_metrics.json': '/api/model-metrics',
    'api_model_card.json': '/api/model-card',
    'api_model_predictions.json': '/api/model-predictions',
    'api_pipeline_runs.json': '/api/pipeline-runs',
}

PREDICTION_PAYLOAD = {
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


def main():
    out_dir = Path('data/rendered')
    out_dir.mkdir(parents=True, exist_ok=True)

    watt_app.load_sample_if_empty(watt_app.app)
    client = watt_app.app.test_client()

    for filename, route in PAGES.items():
        response = client.get(route)
        response.raise_for_status = getattr(response, 'raise_for_status', None)
        if response.status_code != 200:
            raise RuntimeError(f'{route} returned HTTP {response.status_code}')
        path = out_dir / filename
        path.write_text(response.get_data(as_text=True), encoding='utf-8')
        print(f'{route} -> {path}')

    prediction_response = client.post('/prediction', data=PREDICTION_PAYLOAD)
    if prediction_response.status_code != 200:
        raise RuntimeError(f'/prediction returned HTTP {prediction_response.status_code}')
    prediction_path = out_dir / 'prediction_result.html'
    prediction_path.write_text(prediction_response.get_data(as_text=True), encoding='utf-8')
    print(f'/prediction POST -> {prediction_path}')

    api_prediction_response = client.post('/api/predict-duration', json=PREDICTION_PAYLOAD)
    if api_prediction_response.status_code != 200:
        raise RuntimeError(f'/api/predict-duration returned HTTP {api_prediction_response.status_code}')
    api_prediction_path = out_dir / 'api_predict_duration.json'
    api_prediction_path.write_text(api_prediction_response.get_data(as_text=True), encoding='utf-8')
    print(f'/api/predict-duration POST -> {api_prediction_path}')

    model_card = client.get('/api/model-card').get_json()
    model_card_path = Path('docs/rapport/fiche_modele.md')
    model_card_path.write_text(model_card['markdown'], encoding='utf-8')
    print(f'/api/model-card markdown -> {model_card_path}')


if __name__ == '__main__':
    main()
