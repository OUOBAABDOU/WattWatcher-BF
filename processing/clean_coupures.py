import argparse
from pathlib import Path
import pandas as pd

def clean(df):
    df=df.copy().drop_duplicates()
    df['date_debut']=pd.to_datetime(df['date_debut'], errors='coerce'); df['date_fin']=pd.to_datetime(df['date_fin'], errors='coerce')
    df['heure_debut']=df['heure_debut'].astype(str).str.slice(0,5); df['heure_fin']=df['heure_fin'].astype(str).str.slice(0,5)
    for col in ['region','ville','zone']:
        df[col]=df[col].astype(str).str.strip().str.title()
    df['annee']=df['date_debut'].dt.year; df['mois']=df['date_debut'].dt.month; df['duree_heures']=df['duree_minutes']/60; df['coupure_longue']=df['duree_minutes']>=240
    return df

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', required=True); p.add_argument('--out', required=True); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); clean(pd.read_csv(args.input)).to_csv(out,index=False); print('Dataset nettoyé:', out)
if __name__=='__main__': main()
