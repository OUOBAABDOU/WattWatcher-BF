from sqlalchemy import func

from extensions import db
from models import Coupure


def generate_recommendations(duree_moyenne_minutes, nb_coupures_zone, irradiation_moyenne=None):
    recommandations = []
    if duree_moyenne_minutes >= 240:
        recommandations.append({'titre': 'Prévoir une solution de secours longue durée', 'description': 'La durée moyenne dépasse 4 heures. Une batterie, un onduleur hybride ou une installation solaire est recommandé.', 'type': 'solaire/batterie'})
    elif duree_moyenne_minutes >= 120:
        recommandations.append({'titre': 'Sécuriser les équipements sensibles', 'description': 'Les coupures durent souvent plus de 2 heures. Un onduleur est utile pour ordinateurs, routeurs et équipements médicaux.', 'type': 'onduleur'})
    if nb_coupures_zone >= 10:
        recommandations.append({'titre': 'Planifier les activités énergivores', 'description': 'Cette zone présente une fréquence élevée de coupures. Programmer froid, pompage, soudure ou recharge hors périodes critiques.', 'type': 'organisation'})
    if irradiation_moyenne and irradiation_moyenne >= 5:
        recommandations.append({'titre': 'Étudier une solution solaire', 'description': 'L’irradiation solaire moyenne est favorable. Un kit solaire avec batteries peut couvrir l’éclairage, la recharge et les usages prioritaires.', 'type': 'solaire'})
    if not recommandations:
        recommandations.append({'titre': 'Suivi régulier conseillé', 'description': 'Le niveau de risque est modéré. Le tableau de bord aide à anticiper les prochaines coupures.', 'type': 'prévention'})
    return recommandations


def build_zone_recommendations(region=None, zone=None):
    query = Coupure.query
    if region:
        query = query.filter(Coupure.region.ilike(f'%{region}%'))
    if zone:
        query = query.filter(Coupure.zone.ilike(f'%{zone}%'))

    total = query.count()
    avg_duration = query.with_entities(func.avg(Coupure.duree_minutes)).scalar() or 0
    avg_irradiation = query.with_entities(func.avg(Coupure.irradiation_solaire)).scalar()

    return {
        'region': region,
        'zone': zone,
        'nb_coupures': int(total),
        'duree_moyenne': round(float(avg_duration), 2),
        'irradiation_moyenne': round(float(avg_irradiation), 2) if avg_irradiation is not None else None,
        'items': generate_recommendations(float(avg_duration), int(total), float(avg_irradiation) if avg_irradiation is not None else None),
    }
