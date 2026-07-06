import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from processing.real_data import keep_real_data


DEDUP_COLUMNS = ['date_debut', 'heure_debut', 'heure_fin', 'ville', 'zone', 'url_source']


def merge_real_datasets(base, collected):
    base_real = keep_real_data(base)
    merged = pd.concat([base_real, collected], ignore_index=True, sort=False)
    merged = merged.drop(columns=['id_coupure', 'id_source'], errors='ignore')
    available_dedup_columns = [col for col in DEDUP_COLUMNS if col in merged.columns]
    return merged.drop_duplicates(subset=available_dedup_columns, keep='last')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='data/final/dataset_coupures_2020_2026.csv')
    parser.add_argument('--collected', default='data/final/dataset_coupures_reelles_collectees.csv')
    parser.add_argument('--out', default='data/final/dataset_coupures_reelles_combine.csv')
    args = parser.parse_args()

    merged = merge_real_datasets(pd.read_csv(args.base), pd.read_csv(args.collected))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out, index=False)
    print(f'{len(merged)} coupure(s) reelles combinees -> {out}')


if __name__ == '__main__':
    main()
