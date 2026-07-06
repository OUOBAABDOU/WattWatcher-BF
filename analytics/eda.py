import argparse
from pathlib import Path
import pandas as pd
import plotly.express as px

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', default='data/final/dataset_coupures_2020_2026.csv'); p.add_argument('--outdir', default='data/processed/charts'); args=p.parse_args()
    df=pd.read_csv(args.input); outdir=Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    px.bar(df.groupby('region').size().reset_index(name='nb_coupures'), x='region', y='nb_coupures', title='Nombre de coupures par région').write_html(outdir/'coupures_par_region.html')
    px.line(df.groupby('annee').size().reset_index(name='nb_coupures'), x='annee', y='nb_coupures', markers=True, title='Évolution annuelle').write_html(outdir/'evolution_annuelle.html')
    px.bar(df.groupby('region')['duree_minutes'].mean().reset_index(), x='region', y='duree_minutes', title='Durée moyenne par région').write_html(outdir/'duree_moyenne_region.html')
    print('Graphiques générés dans', outdir)
if __name__=='__main__': main()
