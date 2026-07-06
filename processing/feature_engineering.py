import argparse
from pathlib import Path
import pandas as pd

def add_features(df):
    df=df.copy(); df['debut_datetime']=pd.to_datetime(df['date_debut'].astype(str)+' '+df['heure_debut'].astype(str), errors='coerce')
    df['heure_num']=df['debut_datetime'].dt.hour; df['jour_num']=df['debut_datetime'].dt.dayofweek; df['weekend']=df['jour_num'].isin([5,6])
    df['classe_duree']=pd.cut(df['duree_minutes'], bins=[0,60,240,10000], labels=['courte','moyenne','longue'])
    df['risque_zone']=df.groupby('zone')['id_coupure'].transform('count')
    return df

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', default='data/processed/coupures_clean.csv'); p.add_argument('--out', default='data/processed/coupures_features.csv'); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); add_features(pd.read_csv(args.input)).to_csv(out,index=False)
if __name__=='__main__': main()
