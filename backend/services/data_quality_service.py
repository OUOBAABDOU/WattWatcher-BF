import pandas as pd

from models import Coupure
from processing.data_quality import data_quality_report


def coupures_to_dataframe():
    rows = []
    for c in Coupure.query.all():
        rows.append({
            'date_debut': c.date_debut.isoformat() if c.date_debut else None,
            'heure_debut': c.heure_debut.strftime('%H:%M') if c.heure_debut else None,
            'date_fin': c.date_fin.isoformat() if c.date_fin else None,
            'heure_fin': c.heure_fin.strftime('%H:%M') if c.heure_fin else None,
            'duree_minutes': c.duree_minutes,
            'region': c.region,
            'ville': c.ville,
            'zone': c.zone,
            'source_name': c.source_name,
            'source_type': c.source_type,
            'url_source': c.url_source,
        })
    return pd.DataFrame(rows)


def get_data_quality_report():
    return data_quality_report(coupures_to_dataframe())
