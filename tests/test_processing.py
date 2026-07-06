import pandas as pd
from processing.clean_coupures import clean

def test_clean_adds_year_month():
    df=pd.DataFrame({'date_debut':['2026-01-01'], 'date_fin':['2026-01-01'], 'heure_debut':['08:00'], 'heure_fin':['10:00'], 'region':[' centre '], 'ville':[' ouagadougou '], 'zone':[' tanghin '], 'duree_minutes':[120]})
    out=clean(df)
    assert out.loc[0,'annee']==2026
    assert out.loc[0,'region']=='Centre'
