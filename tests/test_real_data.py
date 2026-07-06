import pandas as pd

from processing.real_data import is_real_source, keep_real_data


def test_keep_real_data_excludes_simulation_rows():
    df = pd.DataFrame([
        {'source_type': 'simulation', 'source_name': 'Donnee experimentale'},
        {'source_type': 'officielle', 'source_name': 'SONABEL'},
        {'source_type': 'media', 'source_name': 'Wakat Sera'},
        {'source_type': 'terrain', 'source_name': 'Signalement utilisateur'},
    ])

    out = keep_real_data(df)

    assert out['source_name'].tolist() == ['SONABEL', 'Wakat Sera', 'Signalement utilisateur']


def test_is_real_source_rejects_simulations():
    assert is_real_source('simulation', 'SONABEL') is False
    assert is_real_source('officielle', 'Donnee experimentale') is False
    assert is_real_source('officielle', 'SONABEL') is True
