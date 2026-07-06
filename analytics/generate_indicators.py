import argparse, json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from processing.real_data import keep_real_data

def generate(df):
    return {
        'nombre_total_coupures': int(len(df)),
        'duree_moyenne_minutes': round(float(df['duree_minutes'].mean()), 2),
        'duree_max_minutes': int(df['duree_minutes'].max()),
        'regions_suivies': int(df['region'].nunique()),
        'zones_suivies': int(df['zone'].nunique()),
        'top_regions': df['region'].value_counts().head(10).to_dict(),
        'top_zones': df['zone'].value_counts().head(10).to_dict(),
        'duree_moyenne_par_region': df.groupby('region')['duree_minutes'].mean().round(2).to_dict(),
        'coupures_par_annee': df['annee'].value_counts().sort_index().to_dict(),
        'coupures_par_mois': df['mois'].value_counts().sort_index().to_dict()
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', default='data/final/dataset_coupures_2020_2026.csv'); p.add_argument('--out', default='data/processed/indicateurs.json'); p.add_argument('--real-only', action='store_true'); args=p.parse_args()
    df=pd.read_csv(args.input)
    if args.real_only:
        before=len(df); df=keep_real_data(df); print(f'Donnees reelles conservees: {len(df)}/{before} lignes.')
    indicators=generate(df); out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(indicators, ensure_ascii=False, indent=2), encoding='utf-8'); print(json.dumps(indicators, ensure_ascii=False, indent=2))
if __name__=='__main__': main()
