from services.model_metrics_service import load_model_metrics
from services.model_predictions_service import get_model_predictions_report


def _format_table(headers, rows):
    header_line = '| ' + ' | '.join(headers) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
    row_lines = ['| ' + ' | '.join(str(value) for value in row) + ' |' for row in rows]
    return '\n'.join([header_line, separator, *row_lines])


def build_model_card():
    metrics = load_model_metrics()
    if not metrics.get('available'):
        return {
            'available': False,
            'title': 'Fiche modèle ML',
            'markdown': '# Fiche modèle ML\n\nAucune métrique disponible.',
        }

    dataset = metrics['dataset']
    regression = metrics['regression']
    classification = metrics['classification']
    comparison = metrics['comparison']
    importances = metrics['feature_importance']['regression'][:8]
    predictions = get_model_predictions_report(limit=3)

    variant_rows = [
        [
            variant['label'],
            variant.get('class_weight') or 'none',
            variant.get('mae'),
            variant.get('accuracy'),
            variant.get('macro_f1'),
            variant.get('weighted_f1'),
        ]
        for variant in comparison['variants']
        if variant.get('available')
    ]
    importance_rows = [[item['feature'], item['importance']] for item in importances]
    class_rows = [[label, value] for label, value in dataset.get('class_distribution', {}).items()]
    class_balance = dataset.get('class_balance', {})
    duration_stats = dataset.get('duration_stats', {})
    prediction_summary = predictions.get('summary', {})
    confidence_rows = [
        [
            item['level_label'],
            item['rows'],
            item['correct_rows'],
            item['accuracy'],
            item['avg_confidence'],
        ]
        for item in predictions.get('confidence_summary', [])
    ]
    worst_error_rows = [
        [
            f"{row['region']} / {row['ville']} / {row['zone']}",
            row['actual_duration'],
            row['predicted_duration'],
            row['absolute_error'],
            row['actual_class'],
            row['predicted_class'],
        ]
        for row in predictions.get('worst_errors', [])
    ]

    sections = {
        'usage': 'Estimer la durée probable d’une coupure et classer le risque en courte, moyenne ou longue.',
        'data': f"{dataset.get('usable_rows')} lignes réelles exploitables, dont {dataset.get('test_rows')} lignes de test.",
        'limits': 'Le volume de données réelles reste limité. Les prédictions exactes en minutes doivent rester indicatives et être confirmées par les sources terrain.',
        'recommendation': f"Variante recommandée pour la classification : {comparison.get('best_by_macro_f1')}. Variante avec la meilleure MAE : {comparison.get('best_by_mae')}.",
        'errors': f"{prediction_summary.get('rows', 0)} lignes de test analysées, MAE observée {prediction_summary.get('mae_from_predictions')} min, {prediction_summary.get('misclassified_rows')} erreurs de classification.",
    }

    markdown = '\n\n'.join([
        '# Fiche modèle ML — WattWatcher BF',
        f"**Fichier métriques :** `{metrics['path']}`",
        '## Usage prévu\n' + sections['usage'],
        '## Données utilisées\n' + sections['data'],
        '## Distribution des classes\n' + _format_table(['Classe', 'Lignes'], class_rows),
        '## Déséquilibre des classes\n' + _format_table(
            ['Classe majoritaire', 'Lignes', 'Classe minoritaire', 'Lignes', 'Ratio'],
            [[
                class_balance.get('majority_class'),
                class_balance.get('majority_count'),
                class_balance.get('minority_class'),
                class_balance.get('minority_count'),
                class_balance.get('imbalance_ratio'),
            ]],
        ),
        '## Statistiques de durée\n' + _format_table(
            ['Min', 'Médiane', 'Moyenne', 'Max'],
            [[duration_stats.get('min'), duration_stats.get('median'), duration_stats.get('mean'), duration_stats.get('max')]],
        ),
        '## Résultats principaux\n' + _format_table(
            ['Métrique', 'Valeur'],
            [
                ['MAE régression', f"{regression['mae']} min"],
                ['RMSE régression', f"{regression['rmse']} min"],
                ['R2 régression', regression['r2']],
                ['Accuracy classification', classification['accuracy']],
                ['Accuracy baseline', classification['baseline_accuracy']],
            ],
        ),
        '## Comparaison des variantes\n' + _format_table(
            ['Variante', 'Class weight', 'MAE', 'Accuracy', 'Macro-F1', 'Weighted-F1'],
            variant_rows,
        ),
        '## Variables les plus importantes\n' + _format_table(['Variable', 'Importance'], importance_rows),
        '## Analyse des erreurs de test\n' + sections['errors'],
        '### Fiabilite par niveau de confiance\n' + _format_table(['Niveau', 'Lignes', 'Correctes', 'Accuracy', 'Confiance moyenne'], confidence_rows),
        _format_table(['Lieu', 'Durée réelle', 'Durée prédite', 'Erreur', 'Classe réelle', 'Classe prédite'], worst_error_rows),
        '## Limites\n' + sections['limits'],
        '## Recommandation\n' + sections['recommendation'],
    ])

    return {
        'available': True,
        'title': 'Fiche modèle ML',
        'sections': sections,
        'summary': {
            'usable_rows': dataset.get('usable_rows'),
            'test_rows': dataset.get('test_rows'),
            'mae': regression['mae'],
            'accuracy': classification['accuracy'],
            'best_by_macro_f1': comparison.get('best_by_macro_f1'),
            'best_by_mae': comparison.get('best_by_mae'),
            'prediction_mae': prediction_summary.get('mae_from_predictions'),
            'misclassified_rows': prediction_summary.get('misclassified_rows'),
            'class_distribution': dataset.get('class_distribution', {}),
            'class_balance': class_balance,
            'duration_stats': duration_stats,
        },
        'error_analysis': {
            'summary': prediction_summary,
            'confidence_summary': predictions.get('confidence_summary', []),
            'worst_errors': predictions.get('worst_errors', []),
        },
        'markdown': markdown,
    }
