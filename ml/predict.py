from pathlib import Path

import joblib
import pandas as pd


DEFAULT_MODEL_PATHS = (
    Path('ml/model_real.pkl'),
    Path('ml/model.pkl'),
)


def resolve_model_path(model_path=None):
    if model_path:
        return Path(model_path)

    for path in DEFAULT_MODEL_PATHS:
        if path.exists():
            return path

    return DEFAULT_MODEL_PATHS[-1]


def predict_duration(model_path=None, **kwargs):
    bundle = joblib.load(resolve_model_path(model_path))
    row = pd.DataFrame([{f: kwargs.get(f) for f in bundle['features']}])
    duration = float(bundle['model'].predict(row)[0])
    classifier = bundle.get('classifier')
    classe = classifier.predict(row)[0] if classifier else None
    probabilities = {}
    confidence = None
    if classifier and hasattr(classifier, 'predict_proba'):
        classes = classifier.classes_
        proba = classifier.predict_proba(row)[0]
        probabilities = {str(label): float(value) for label, value in zip(classes, proba)}
        confidence = probabilities.get(str(classe))
    return {
        'duree_minutes': duration,
        'classe_duree': classe,
        'classe_proba': probabilities,
        'classe_confiance': confidence,
    }


if __name__ == '__main__':
    print(predict_duration(region='Centre', ville='Ouagadougou', zone='Tanghin', type_coupure='prévue', mois=3, heure_num=8, jour_num=5, temperature_max=38, precipitation=0, irradiation_solaire=5.8))
