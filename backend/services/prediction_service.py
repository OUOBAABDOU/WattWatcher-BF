from datetime import date

from ml.predict import predict_duration, resolve_model_path


MODEL_VARIANTS = {
    'standard': 'ml/model_real.pkl',
    'balanced': 'ml/model_real_balanced.pkl',
}
DEFAULT_INPUT = {
    'region': 'Centre',
    'ville': 'Ouagadougou',
    'zone': 'Tanghin',
    'type_coupure': 'prévue',
    'mois': 3,
    'heure_num': 8,
    'jour_num': 1,
    'temperature_max': 38.0,
    'precipitation': 0.0,
    'irradiation_solaire': 5.8,
    'model_variant': 'balanced',
}


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_prediction_input(values):
    today = date.today()
    data = {
        **DEFAULT_INPUT,
        'mois': today.month,
        'jour_num': today.weekday(),
    }
    for field in ('region', 'ville', 'zone', 'type_coupure', 'model_variant'):
        value = values.get(field)
        if value:
            data[field] = str(value).strip()

    data['mois'] = _to_int(values.get('mois'), data['mois'])
    data['heure_num'] = _to_int(values.get('heure_num'), data['heure_num'])
    data['jour_num'] = _to_int(values.get('jour_num'), data['jour_num'])
    data['temperature_max'] = _to_float(values.get('temperature_max'), data['temperature_max'])
    data['precipitation'] = _to_float(values.get('precipitation'), data['precipitation'])
    data['irradiation_solaire'] = _to_float(values.get('irradiation_solaire'), data['irradiation_solaire'])
    return data


def resolve_prediction_model_path(model_variant):
    return MODEL_VARIANTS.get(model_variant, MODEL_VARIANTS['balanced'])


def interpret_confidence(confidence):
    if confidence is None:
        return {
            'niveau_confiance': 'inconnu',
            'message_decision': 'Le modèle ne fournit pas de probabilité pour cette prédiction.',
        }
    if confidence < 0.45:
        return {
            'niveau_confiance': 'faible',
            'message_decision': 'Prédiction prudente : les classes sont proches, vérifier avec les données terrain.',
        }
    if confidence < 0.65:
        return {
            'niveau_confiance': 'moyenne',
            'message_decision': 'Prédiction exploitable comme indication, à confirmer par suivi local.',
        }
    return {
        'niveau_confiance': 'élevée',
        'message_decision': 'Prédiction plus stable : le modèle distingue clairement la classe dominante.',
    }


def run_prediction(values):
    features = normalize_prediction_input(values)
    model_variant = features.pop('model_variant')
    model_path = resolve_prediction_model_path(model_variant)
    prediction = predict_duration(model_path=model_path, **features)
    confidence = round(float(prediction['classe_confiance']), 3) if prediction.get('classe_confiance') is not None else None
    interpretation = interpret_confidence(confidence)
    return {
        'available': True,
        'model_variant': model_variant if model_variant in MODEL_VARIANTS else 'balanced',
        'model_path': str(resolve_model_path(model_path)),
        'features': features,
        'prediction': {
            'duree_minutes': round(float(prediction['duree_minutes']), 2),
            'classe_duree': prediction.get('classe_duree'),
            'classe_confiance': confidence,
            'classe_proba': {
                label: round(float(value), 3)
                for label, value in prediction.get('classe_proba', {}).items()
            },
            **interpretation,
        },
    }
