import argparse
from pathlib import Path
import requests, pandas as pd

def download_openmeteo(lat, lon, start, end):
    url='https://archive-api.open-meteo.com/v1/archive'
    params={'latitude':lat,'longitude':lon,'start_date':start,'end_date':end,'daily':'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max','timezone':'Africa/Ouagadougou'}
    r=requests.get(url, params=params, timeout=60); r.raise_for_status(); return pd.DataFrame(r.json()['daily'])

def main():
    p=argparse.ArgumentParser(); p.add_argument('--lat',type=float,required=True); p.add_argument('--lon',type=float,required=True); p.add_argument('--start',required=True); p.add_argument('--end',required=True); p.add_argument('--out',required=True); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); download_openmeteo(args.lat,args.lon,args.start,args.end).to_csv(out,index=False)
if __name__=='__main__': main()
