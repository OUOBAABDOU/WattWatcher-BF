import argparse
from pathlib import Path
import requests, pandas as pd

def download_nasa_power(lat, lon, start, end):
    url='https://power.larc.nasa.gov/api/temporal/daily/point'
    params={'parameters':'ALLSKY_SFC_SW_DWN,T2M,WS10M,PRECTOTCORR','community':'RE','longitude':lon,'latitude':lat,'start':start,'end':end,'format':'JSON'}
    r=requests.get(url, params=params, timeout=60); r.raise_for_status(); data=r.json()['properties']['parameter']; df=pd.DataFrame(data); df.index.name='date'; return df.reset_index()

def main():
    p=argparse.ArgumentParser(); p.add_argument('--lat',type=float,required=True); p.add_argument('--lon',type=float,required=True); p.add_argument('--start',required=True); p.add_argument('--end',required=True); p.add_argument('--out',required=True); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); download_nasa_power(args.lat,args.lon,args.start,args.end).to_csv(out,index=False)
if __name__=='__main__': main()
