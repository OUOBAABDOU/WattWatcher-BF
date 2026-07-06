import pandas as pd

from processing.merge_real_datasets import merge_real_datasets


def test_merge_real_datasets_filters_simulations_and_dedupes_collected_rows():
    base = pd.DataFrame([
        {
            'date_debut': '2026-03-07',
            'id_coupure': 1,
            'heure_debut': '08:00',
            'heure_fin': '13:00',
            'ville': 'Ouagadougou',
            'zone': 'Tanghin',
            'url_source': 'https://example.test/tanghin',
            'source_type': 'media',
            'source_name': 'Old',
            'temperature_max': '',
        },
        {
            'date_debut': '2026-01-01',
            'heure_debut': '08:00',
            'heure_fin': '10:00',
            'ville': 'Ouagadougou',
            'zone': 'Test',
            'url_source': '',
            'source_type': 'simulation',
            'source_name': 'Donnee experimentale',
            'temperature_max': '',
        },
    ])
    collected = pd.DataFrame([{
        'date_debut': '2026-03-07',
        'heure_debut': '08:00',
        'heure_fin': '13:00',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
        'url_source': 'https://example.test/tanghin',
        'source_type': 'media',
        'source_name': 'Collected',
        'temperature_max': 39.4,
    }])

    out = merge_real_datasets(base, collected)

    assert len(out) == 1
    assert 'id_coupure' not in out.columns
    assert out.iloc[0]['source_name'] == 'Collected'
    assert out.iloc[0]['temperature_max'] == 39.4
