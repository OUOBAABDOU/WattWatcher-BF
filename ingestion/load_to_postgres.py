import argparse
import os
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from processing.real_data import keep_real_data

load_dotenv()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--real-only', action='store_true', help='Load only real sources and exclude simulations.')
    parser.add_argument('--replace-coupures', action='store_true', help='Delete existing coupures before loading the CSV.')
    args = parser.parse_args()

    engine = create_engine(os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/wattwatcher_db'))
    with open('database/schema.sql', encoding='utf-8-sig') as file:
        schema = file.read()
    with engine.begin() as conn:
        conn.execute(text(schema))
        if args.replace_coupures:
            conn.execute(text('TRUNCATE TABLE coupures RESTART IDENTITY CASCADE'))

    df = pd.read_csv(args.csv)
    if args.real_only:
        before = len(df)
        df = keep_real_data(df)
        print(f'Donnees reelles conservees: {len(df)}/{before} lignes.')
    df = df.drop(columns=['id_coupure', 'id_source'], errors='ignore')

    df.to_sql('coupures', engine, if_exists='append', index=False, method='multi')
    print(f'{len(df)} lignes chargees dans PostgreSQL.')


if __name__ == '__main__':
    main()
