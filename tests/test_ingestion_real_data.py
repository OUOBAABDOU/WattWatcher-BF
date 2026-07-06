import pandas as pd

from ingestion.scrape_medias import extract_hours, extract_zones
from processing.enrich_real_coupures import enrich


def test_extract_hours_and_zones_from_realistic_sonabel_text():
    text = 'La SONABEL annonce une coupure dans les zones de Tanghin et Gounghin de 8h à 13h.'

    assert extract_hours(text) == [('8', '', '13', '')]
    assert extract_zones(text) == ['Tanghin', 'Gounghin']


def test_enrich_merges_weather_and_solar_values():
    coupures = pd.DataFrame([{
        'date_debut': '2026-03-07',
        'temperature_max': '',
        'precipitation': '',
        'irradiation_solaire': '',
    }])
    weather = pd.DataFrame([{
        'time': '2026-03-07',
        'temperature_2m_max': 39.4,
        'precipitation_sum': 0.0,
    }])
    solar = pd.DataFrame([{
        'date': 20260307,
        'ALLSKY_SFC_SW_DWN': 6.1661,
    }])

    out = enrich(coupures, weather, solar)

    assert out.loc[0, 'temperature_max'] == 39.4
    assert out.loc[0, 'precipitation'] == 0.0
    assert out.loc[0, 'irradiation_solaire'] == 6.1661
