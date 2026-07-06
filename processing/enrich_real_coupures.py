import argparse
from pathlib import Path

import pandas as pd


def enrich(coupures, weather, solar):
    df = coupures.copy()
    df['date_debut'] = pd.to_datetime(df['date_debut']).dt.date.astype(str)

    weather = weather.rename(columns={
        'time': 'date_debut',
        'temperature_2m_max': 'temperature_max',
        'precipitation_sum': 'precipitation',
    })
    solar = solar.copy()
    solar['date_debut'] = pd.to_datetime(solar['date'].astype(str), format='%Y%m%d').dt.date.astype(str)
    solar = solar.rename(columns={'ALLSKY_SFC_SW_DWN': 'irradiation_solaire'})

    df = df.drop(columns=['temperature_max', 'precipitation', 'irradiation_solaire'], errors='ignore')
    df = df.merge(weather[['date_debut', 'temperature_max', 'precipitation']], on='date_debut', how='left')
    df = df.merge(solar[['date_debut', 'irradiation_solaire']], on='date_debut', how='left')
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--coupures', default='data/raw/medias/coupures_structurees.csv')
    parser.add_argument('--weather', required=True)
    parser.add_argument('--solar', required=True)
    parser.add_argument('--out', default='data/final/dataset_coupures_reelles_collectees.csv')
    args = parser.parse_args()

    enriched = enrich(
        pd.read_csv(args.coupures),
        pd.read_csv(args.weather),
        pd.read_csv(args.solar),
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(out, index=False)
    print(f'{len(enriched)} coupure(s) reelles enrichies -> {out}')


if __name__ == '__main__':
    main()
