import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from processing.real_data import keep_real_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/final/dataset_coupures_2020_2026.csv')
    parser.add_argument('--out', default='data/final/dataset_coupures_reelles.csv')
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    before = len(df)
    real_df = keep_real_data(df)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    real_df.to_csv(out, index=False)
    print(f'Donnees reelles exportees: {len(real_df)}/{before} lignes -> {out}')


if __name__ == '__main__':
    main()
