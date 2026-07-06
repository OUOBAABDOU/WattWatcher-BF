import json
from pathlib import Path

import joblib

from config import BASE_DIR


METRICS_PATHS = (
    BASE_DIR / 'data' / 'processed' / 'model_metrics_real.json',
    BASE_DIR / 'data' / 'processed' / 'model_metrics_real_balanced.json',
)
MODEL_PATHS = (
    BASE_DIR / 'ml' / 'model_real.pkl',
    BASE_DIR / 'ml' / 'model.pkl',
)
MODEL_VARIANTS = (
    ('standard', BASE_DIR / 'data' / 'processed' / 'model_metrics_real.json'),
    ('balanced', BASE_DIR / 'data' / 'processed' / 'model_metrics_real_balanced.json'),
)


def _round_metric(value, digits=3):
    return round(float(value), digits) if value is not None else None


def _base_feature_name(encoded_name):
    name = encoded_name.split('__', 1)[-1]
    for feature in ('temperature_max', 'irradiation_solaire', 'precipitation', 'type_coupure', 'heure_num', 'jour_num', 'region', 'ville', 'zone', 'mois'):
        if name == feature or name.startswith(f'{feature}_'):
            return feature
    return name


def _extract_feature_importance(pipeline, estimator_step):
    preprocessor = pipeline.named_steps.get('preprocessor')
    estimator = pipeline.named_steps.get(estimator_step)
    if not preprocessor or not estimator or not hasattr(estimator, 'feature_importances_'):
        return []

    encoded_names = preprocessor.get_feature_names_out()
    grouped = {}
    for encoded_name, importance in zip(encoded_names, estimator.feature_importances_):
        feature = _base_feature_name(str(encoded_name))
        grouped[feature] = grouped.get(feature, 0.0) + float(importance)

    return [
        {'feature': feature, 'importance': round(value, 4)}
        for feature, value in sorted(grouped.items(), key=lambda item: item[1], reverse=True)
    ]


def load_feature_importance():
    selected_model = next((path for path in MODEL_PATHS if path.exists()), None)
    if not selected_model:
        return {'available': False, 'model_path': None, 'regression': [], 'classification': []}

    bundle = joblib.load(selected_model)
    return {
        'available': True,
        'model_path': str(selected_model.relative_to(BASE_DIR)),
        'regression': _extract_feature_importance(bundle['model'], 'regressor'),
        'classification': _extract_feature_importance(bundle.get('classifier'), 'classifier') if bundle.get('classifier') else [],
    }


def normalize_feature_importance(data):
    feature_importance = data.get('feature_importance') or {}
    if feature_importance.get('regression') or feature_importance.get('classification'):
        return {
            'available': True,
            'model_path': None,
            'regression': feature_importance.get('regression', []),
            'classification': feature_importance.get('classification', []),
        }
    return load_feature_importance()


def summarize_metrics_variant(label, path):
    if not path.exists():
        return {
            'label': label,
            'available': False,
            'path': str(path.relative_to(BASE_DIR)),
        }

    data = json.loads(path.read_text(encoding='utf-8'))
    regression = data.get('regression', {})
    classification = data.get('classification', {})
    baseline_reg = regression.get('baseline_mean_duration', {})
    baseline_cls = classification.get('baseline_majority_class', {})
    params = data.get('model_params', {})
    return {
        'label': label,
        'available': True,
        'path': str(path.relative_to(BASE_DIR)),
        'class_weight': params.get('class_weight'),
        'usable_rows': data.get('dataset', {}).get('usable_rows'),
        'test_rows': data.get('dataset', {}).get('test_rows'),
        'mae': _round_metric(regression.get('MAE'), 2),
        'baseline_mae': _round_metric(baseline_reg.get('MAE'), 2),
        'accuracy': _round_metric(classification.get('accuracy'), 3),
        'baseline_accuracy': _round_metric(baseline_cls.get('accuracy'), 3),
        'macro_f1': _round_metric(classification.get('report', {}).get('macro avg', {}).get('f1-score'), 3),
        'weighted_f1': _round_metric(classification.get('report', {}).get('weighted avg', {}).get('f1-score'), 3),
    }


def load_model_comparison():
    variants = [summarize_metrics_variant(label, path) for label, path in MODEL_VARIANTS]
    available = [variant for variant in variants if variant.get('available')]
    best_by_macro_f1 = max(available, key=lambda item: item.get('macro_f1') or 0, default=None)
    best_by_mae = min(available, key=lambda item: item.get('mae') or float('inf'), default=None)
    return {
        'variants': variants,
        'best_by_macro_f1': best_by_macro_f1.get('label') if best_by_macro_f1 else None,
        'best_by_mae': best_by_mae.get('label') if best_by_mae else None,
    }


def load_model_metrics():
    selected_path = next((path for path in METRICS_PATHS if path.exists()), None)
    if not selected_path:
        return {
            'available': False,
            'path': None,
            'message': 'Aucun fichier de métriques ML disponible.',
        }

    data = json.loads(selected_path.read_text(encoding='utf-8'))
    regression = data.get('regression', {})
    classification = data.get('classification', {})
    baseline_reg = regression.get('baseline_mean_duration', {})
    baseline_cls = classification.get('baseline_majority_class', {})

    return {
        'available': True,
        'path': str(selected_path.relative_to(BASE_DIR)),
        'dataset': data.get('dataset', {}),
        'model_params': data.get('model_params', {}),
        'regression': {
            'mae': _round_metric(regression.get('MAE'), 2),
            'rmse': _round_metric(regression.get('RMSE'), 2),
            'r2': _round_metric(regression.get('R2'), 3),
            'baseline_mae': _round_metric(baseline_reg.get('MAE'), 2),
            'baseline_rmse': _round_metric(baseline_reg.get('RMSE'), 2),
            'baseline_prediction_minutes': _round_metric(baseline_reg.get('prediction_minutes'), 2),
        },
        'classification': {
            'accuracy': _round_metric(classification.get('accuracy'), 3),
            'classes': classification.get('classes', []),
            'confusion_matrix': classification.get('confusion_matrix', []),
            'baseline_class': baseline_cls.get('class'),
            'baseline_accuracy': _round_metric(baseline_cls.get('accuracy'), 3),
            'report': classification.get('report', {}),
        },
        'feature_importance': normalize_feature_importance(data),
        'comparison': load_model_comparison(),
        'interpretation': data.get('interpretation'),
    }
