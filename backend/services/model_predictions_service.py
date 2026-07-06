import csv

from config import BASE_DIR


PREDICTIONS_PATH = BASE_DIR / 'data' / 'processed' / 'model_predictions_real.csv'


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_predictions():
    if not PREDICTIONS_PATH.exists():
        return []
    with PREDICTIONS_PATH.open(newline='', encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))


def _confidence_label(level):
    return {
        'faible': 'faible',
        'moyenne': 'moyenne',
        'elevee': 'élevée',
        'inconnu': 'inconnu',
    }.get(level or 'inconnu', level or 'inconnu')


def _format_row(row):
    level = row.get('confidence_level') or 'inconnu'
    return {
        'region': row.get('region'),
        'ville': row.get('ville'),
        'zone': row.get('zone'),
        'type_coupure': row.get('type_coupure'),
        'actual_duration': _to_float(row.get('actual_duration')),
        'predicted_duration': _to_float(row.get('predicted_duration')),
        'absolute_error': _to_float(row.get('absolute_error')),
        'actual_class': row.get('actual_class'),
        'predicted_class': row.get('predicted_class'),
        'classification_correct': str(row.get('classification_correct')).lower() == 'true',
        'predicted_class_confidence': _to_float(row.get('predicted_class_confidence')),
        'confidence_level': level,
        'confidence_level_label': _confidence_label(level),
        'proba_courte': _to_float(row.get('proba_courte')),
        'proba_longue': _to_float(row.get('proba_longue')),
        'proba_moyenne': _to_float(row.get('proba_moyenne')),
    }


def _confidence_summary(rows):
    levels = ['faible', 'moyenne', 'elevee', 'inconnu']
    summary = []
    for level in levels:
        level_rows = [row for row in rows if row['confidence_level'] == level]
        if not level_rows:
            continue
        correct = [row for row in level_rows if row['classification_correct']]
        avg_confidence = sum(row['predicted_class_confidence'] for row in level_rows) / len(level_rows)
        summary.append({
            'level': level,
            'level_label': _confidence_label(level),
            'rows': len(level_rows),
            'correct_rows': len(correct),
            'accuracy': round(len(correct) / len(level_rows), 3),
            'avg_confidence': round(avg_confidence, 3),
        })
    return summary


def get_model_predictions_report(limit=12):
    rows = [_format_row(row) for row in _read_predictions()]
    if not rows:
        return {
            'available': False,
            'path': str(PREDICTIONS_PATH.relative_to(BASE_DIR)),
            'summary': {'rows': 0},
            'confidence_summary': [],
            'worst_errors': [],
            'misclassified': [],
        }

    correct = [row for row in rows if row['classification_correct']]
    errors = sorted(rows, key=lambda row: row['absolute_error'], reverse=True)
    misclassified = [row for row in errors if not row['classification_correct']]
    avg_error = sum(row['absolute_error'] for row in rows) / len(rows)

    return {
        'available': True,
        'path': str(PREDICTIONS_PATH.relative_to(BASE_DIR)),
        'summary': {
            'rows': len(rows),
            'mae_from_predictions': round(avg_error, 2),
            'classification_accuracy': round(len(correct) / len(rows), 3),
            'misclassified_rows': len(misclassified),
        },
        'confidence_summary': _confidence_summary(rows),
        'worst_errors': errors[:limit],
        'misclassified': misclassified[:limit],
    }
