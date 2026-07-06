import argparse
from pathlib import Path
import requests, pandas as pd

def download_worldbank(indicator, country='BF'):
    url=f'https://api.worldbank.org/v2/country/{country}/indicator/{indicator}'
    r=requests.get(url, params={'format':'json','per_page':200}, timeout=60); r.raise_for_status(); payload=r.json(); data=payload[1] if len(payload)>1 else []
    return pd.DataFrame([{'annee':x.get('date'), 'valeur':x.get('value'), 'indicator':indicator, 'country':country} for x in data])

def main():
    p=argparse.ArgumentParser(); p.add_argument('--indicator', required=True); p.add_argument('--country', default='BF'); p.add_argument('--out', required=True); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); download_worldbank(args.indicator,args.country).to_csv(out,index=False)
if __name__=='__main__': main()
