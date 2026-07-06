import pandas as pd

from processing.data_quality import data_quality_report


def test_data_quality_report_counts_missing_duplicates_and_anomalies():
    df = pd.DataFrame([
        {
            'date_debut': '2026-03-07',
            'date_fin': '2026-03-07',
            'heure_debut': '08:00',
            'heure_fin': '13:00',
            'duree_minutes': 300,
            'region': 'Centre',
            'ville': 'Ouagadougou',
            'zone': 'Tanghin',
            'source_name': 'Wakat Sera',
            'source_type': 'media',
            'url_source': 'https://example.test/a',
        },
        {
            'date_debut': '2026-03-07',
            'date_fin': '2026-03-07',
            'heure_debut': '08:00',
            'heure_fin': '13:00',
            'duree_minutes': 0,
            'region': 'Centre',
            'ville': 'Ouagadougou',
            'zone': 'Tanghin',
            'source_name': '',
            'source_type': 'inconnu',
            'url_source': 'https://example.test/a',
        },
    ])

    report = data_quality_report(df)

    assert report['total_lignes'] == 2
    assert report['doublons'] == 1
    assert report['anomalies']['duree_negative_or_zero'] == 1
    assert report['anomalies']['source_type_inconnu'] == 1
    assert report['repartition_sources']['media'] == 1
    assert report['score_qualite'] < 100
