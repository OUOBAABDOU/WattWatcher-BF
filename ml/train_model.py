import argparse
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from processing.real_data import keep_real_data


FEATURES = ['region', 'ville', 'zone', 'type_coupure', 'mois', 'heure_num', 'jour_num', 'temperature_max', 'precipitation', 'irradiation_solaire']
TARGET = 'duree_minutes'
CAT_FEATURES = ['region', 'ville', 'zone', 'type_coupure']
NUM_FEATURES = ['mois', 'heure_num', 'jour_num', 'temperature_max', 'precipitation', 'irradiation_solaire']
FEATURE_IMPORTANCE_ORDER = ['temperature_max', 'irradiation_solaire', 'precipitation', 'type_coupure', 'heure_num', 'jour_num', 'region', 'ville', 'zone', 'mois']


def duration_class(minutes):
    if minutes <= 60:
        return 'courte'
    if minutes <= 240:
        return 'moyenne'
    return 'longue'


def confidence_level(confidence):
    if confidence < 0.45:
        return 'faible'
    if confidence < 0.65:
        return 'moyenne'
    return 'elevee'


def prepare_dataset(df, real_only=False):
    source_rows = len(df)
    if real_only:
        df = keep_real_data(df)

    df = df.copy()
    df['date_debut'] = pd.to_datetime(df['date_debut'])
    df['heure_num'] = pd.to_datetime(df['heure_debut'], format='%H:%M', errors='coerce').dt.hour
    df['jour_num'] = df['date_debut'].dt.dayofweek
    df['classe_duree'] = df[TARGET].apply(duration_class)
    df = df.dropna(subset=FEATURES + [TARGET, 'classe_duree'])

    if df.empty:
        raise ValueError('Aucune ligne exploitable apres filtrage/nettoyage.')

    dataset_info = {
        'source_rows': int(source_rows),
        'usable_rows': int(len(df)),
    }
    return df, dataset_info


def build_preprocessor():
    return ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), CAT_FEATURES),
        ('num', 'passthrough', NUM_FEATURES),
    ])


def build_models(n_estimators=160, random_state=42, class_weight=None):
    preprocessor = build_preprocessor()
    regressor = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=n_estimators, min_samples_leaf=3, random_state=random_state)),
    ])
    classifier = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=n_estimators, min_samples_leaf=3, random_state=random_state, class_weight=class_weight)),
    ])
    return regressor, classifier


def train_models(df, n_estimators=160, test_size=0.2, random_state=42, class_weight=None):
    X = df[FEATURES]
    y_reg = df[TARGET]
    y_cls = df['classe_duree']
    split = train_test_split(X, y_reg, y_cls, test_size=test_size, random_state=random_state, stratify=y_cls)
    X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = split

    regressor, classifier = build_models(n_estimators=n_estimators, random_state=random_state, class_weight=class_weight)
    regressor.fit(X_train, y_reg_train)
    classifier.fit(X_train, y_cls_train)

    return {
        'regressor': regressor,
        'classifier': classifier,
        'X_train': X_train,
        'X_test': X_test,
        'y_reg_train': y_reg_train,
        'y_reg_test': y_reg_test,
        'y_cls_train': y_cls_train,
        'y_cls_test': y_cls_test,
    }


def base_feature_name(encoded_name):
    name = encoded_name.split('__', 1)[-1]
    for feature in FEATURE_IMPORTANCE_ORDER:
        if name == feature or name.startswith(f'{feature}_'):
            return feature
    return name


def extract_feature_importance(pipeline, estimator_step):
    if not hasattr(pipeline, 'named_steps'):
        return []

    preprocessor = pipeline.named_steps.get('preprocessor')
    estimator = pipeline.named_steps.get(estimator_step)
    if not preprocessor or not estimator or not hasattr(estimator, 'feature_importances_'):
        return []

    grouped = {}
    encoded_names = preprocessor.get_feature_names_out()
    for encoded_name, importance in zip(encoded_names, estimator.feature_importances_):
        feature = base_feature_name(str(encoded_name))
        grouped[feature] = grouped.get(feature, 0.0) + float(importance)

    return [
        {'feature': feature, 'importance': round(value, 4)}
        for feature, value in sorted(grouped.items(), key=lambda item: item[1], reverse=True)
    ]


def dataset_profile(df):
    class_counts = df['classe_duree'].value_counts().sort_index()
    class_distribution = {str(label): int(value) for label, value in class_counts.items()}
    majority_class = max(class_distribution, key=class_distribution.get) if class_distribution else None
    minority_class = min(class_distribution, key=class_distribution.get) if class_distribution else None
    majority_count = class_distribution.get(majority_class, 0) if majority_class else 0
    minority_count = class_distribution.get(minority_class, 0) if minority_class else 0
    durations = df[TARGET]
    return {
        'class_distribution': class_distribution,
        'class_balance': {
            'majority_class': majority_class,
            'majority_count': majority_count,
            'minority_class': minority_class,
            'minority_count': minority_count,
            'imbalance_ratio': round(majority_count / minority_count, 2) if minority_count else None,
        },
        'duration_stats': {
            'min': round(float(durations.min()), 2),
            'median': round(float(durations.median()), 2),
            'mean': round(float(durations.mean()), 2),
            'max': round(float(durations.max()), 2),
        },
    }


def build_metrics(training, df, dataset_info, input_path, real_only, model_params=None):
    pred_reg = training['regressor'].predict(training['X_test'])
    pred_cls = training['classifier'].predict(training['X_test'])
    classes = sorted(df['classe_duree'].unique().tolist())
    baseline_duration = float(training['y_reg_train'].mean())
    baseline_reg = [baseline_duration] * len(training['y_reg_test'])
    baseline_class = training['y_cls_train'].mode().iloc[0]
    baseline_cls = [baseline_class] * len(training['y_cls_test'])

    return {
        'regression': {
            'MAE': float(mean_absolute_error(training['y_reg_test'], pred_reg)),
            'RMSE': float(mean_squared_error(training['y_reg_test'], pred_reg) ** 0.5),
            'R2': float(r2_score(training['y_reg_test'], pred_reg)),
            'baseline_mean_duration': {
                'prediction_minutes': baseline_duration,
                'MAE': float(mean_absolute_error(training['y_reg_test'], baseline_reg)),
                'RMSE': float(mean_squared_error(training['y_reg_test'], baseline_reg) ** 0.5),
            },
        },
        'classification': {
            'accuracy': float(accuracy_score(training['y_cls_test'], pred_cls)),
            'classes': classes,
            'report': classification_report(training['y_cls_test'], pred_cls, labels=classes, output_dict=True, zero_division=0),
            'confusion_matrix': confusion_matrix(training['y_cls_test'], pred_cls, labels=classes).tolist(),
            'baseline_majority_class': {
                'class': baseline_class,
                'accuracy': float(accuracy_score(training['y_cls_test'], baseline_cls)),
            },
        },
        'dataset': {
            'input': str(input_path),
            'real_only': bool(real_only),
            **dataset_info,
            'train_rows': int(len(training['X_train'])),
            'test_rows': int(len(training['X_test'])),
            **dataset_profile(df),
        },
        'feature_importance': {
            'regression': extract_feature_importance(training['regressor'], 'regressor'),
            'classification': extract_feature_importance(training['classifier'], 'classifier'),
        },
        'model_params': model_params or {},
        'interpretation': 'La classification courte/moyenne/longue reste le resultat principal si la regression est instable sur les donnees disponibles.',
    }


def markdown_table(headers, rows):
    header_line = '| ' + ' | '.join(headers) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(headers)) + ' |'
    row_lines = ['| ' + ' | '.join(str(value) for value in row) + ' |' for row in rows]
    return '\n'.join([header_line, separator, *row_lines])


def summarize_test_predictions(predictions):
    if predictions is None or predictions.empty:
        return None

    misclassified = predictions[predictions['classification_correct'] == False]
    worst_errors = predictions.sort_values('absolute_error', ascending=False).head(3)
    return {
        'rows': int(len(predictions)),
        'mae_from_predictions': round(float(predictions['absolute_error'].mean()), 2),
        'classification_accuracy': round(float(predictions['classification_correct'].mean()), 3),
        'misclassified_rows': int(len(misclassified)),
        'worst_errors': worst_errors,
    }


def build_model_card_markdown(metrics, predictions=None):
    regression = metrics['regression']
    classification = metrics['classification']
    dataset = metrics['dataset']
    baseline = classification['baseline_majority_class']
    importances = metrics.get('feature_importance', {}).get('regression', [])[:8]
    importance_rows = [[item['feature'], item['importance']] for item in importances]
    class_rows = [[label, value] for label, value in dataset.get('class_distribution', {}).items()]
    class_balance = dataset.get('class_balance', {})
    duration_stats = dataset.get('duration_stats', {})
    prediction_summary = summarize_test_predictions(predictions)

    prediction_section = ''
    if prediction_summary:
        worst_rows = [
            [
                ' / '.join(str(value) for value in [getattr(row, 'region', ''), getattr(row, 'ville', ''), getattr(row, 'zone', '')] if value),
                row.actual_duration,
                row.predicted_duration,
                row.absolute_error,
                row.actual_class,
                row.predicted_class,
            ]
            for row in prediction_summary['worst_errors'].itertuples(index=False)
        ]
        prediction_section = '\n\n'.join([
            '## Analyse des erreurs de test',
            f"{prediction_summary['rows']} lignes de test analysees, MAE observee {prediction_summary['mae_from_predictions']} min, {prediction_summary['misclassified_rows']} erreurs de classification.",
            markdown_table(['Lieu', 'Duree reelle', 'Duree predite', 'Erreur', 'Classe reelle', 'Classe predite'], worst_rows),
        ])

    sections = [
        '# Fiche modele ML - WattWatcher BF',
        f"**Jeu de donnees :** `{dataset['input']}`",
        f"**Donnees reelles uniquement :** {dataset['real_only']}",
        '## Usage prevu\nEstimer la duree probable d une coupure et classer la duree en courte, moyenne ou longue.',
        f"## Donnees utilisees\n{dataset['usable_rows']} lignes exploitables, {dataset['train_rows']} lignes d entrainement et {dataset['test_rows']} lignes de test.",
        '## Distribution des classes\n' + markdown_table(['Classe', 'Lignes'], class_rows),
        '## Desequilibre des classes\n' + markdown_table(
            ['Classe majoritaire', 'Lignes', 'Classe minoritaire', 'Lignes', 'Ratio'],
            [[
                class_balance.get('majority_class'),
                class_balance.get('majority_count'),
                class_balance.get('minority_class'),
                class_balance.get('minority_count'),
                class_balance.get('imbalance_ratio'),
            ]],
        ),
        '## Statistiques de duree\n' + markdown_table(
            ['Min', 'Mediane', 'Moyenne', 'Max'],
            [[duration_stats.get('min'), duration_stats.get('median'), duration_stats.get('mean'), duration_stats.get('max')]],
        ),
        '## Resultats principaux\n' + markdown_table(
            ['Metrique', 'Valeur'],
            [
                ['MAE regression', f"{round(regression['MAE'], 2)} min"],
                ['RMSE regression', f"{round(regression['RMSE'], 2)} min"],
                ['R2 regression', round(regression['R2'], 3)],
                ['Accuracy classification', round(classification['accuracy'], 3)],
                ['Classe baseline', baseline['class']],
                ['Accuracy baseline', round(baseline['accuracy'], 3)],
            ],
        ),
        '## Variables importantes\n' + markdown_table(['Variable', 'Importance'], importance_rows),
    ]
    if prediction_section:
        sections.append(prediction_section)
    sections.extend([
        '## Limites\nLe volume de donnees reelles reste limite. Les predictions exactes en minutes doivent rester indicatives et etre confirmees par les sources terrain.',
        '## Recommandation\nUtiliser la classification courte/moyenne/longue comme aide a la decision, avec affichage de la confiance lorsque le modele est utilise dans l application.',
    ])
    return '\n\n'.join(sections)


def build_test_predictions(training):
    rows = training['X_test'].copy().reset_index(drop=True)
    actual_duration = training['y_reg_test'].reset_index(drop=True)
    actual_class = training['y_cls_test'].reset_index(drop=True)
    pred_duration = training['regressor'].predict(training['X_test'])
    pred_class = training['classifier'].predict(training['X_test'])

    rows['actual_duration'] = actual_duration
    rows['predicted_duration'] = [round(float(value), 2) for value in pred_duration]
    rows['absolute_error'] = (rows['actual_duration'] - rows['predicted_duration']).abs().round(2)
    rows['actual_class'] = actual_class
    rows['predicted_class'] = pred_class
    rows['classification_correct'] = rows['actual_class'] == rows['predicted_class']

    if hasattr(training['classifier'], 'predict_proba'):
        probabilities = pd.DataFrame(training['classifier'].predict_proba(training['X_test']))
        for index, class_name in enumerate(training['classifier'].classes_):
            values = probabilities.iloc[:, index]
            rows[f'proba_{class_name}'] = [round(float(value), 4) for value in values]
        confidence_values = []
        for row_index, predicted in enumerate(rows['predicted_class']):
            class_index = list(training['classifier'].classes_).index(predicted)
            confidence_values.append(round(float(probabilities.iloc[row_index, class_index]), 4))
        rows['predicted_class_confidence'] = confidence_values
        rows['confidence_level'] = [confidence_level(value) for value in confidence_values]

    return rows


def save_outputs(out_path, metrics_out_path, model_card_out_path, predictions_out_path, regressor, classifier, metrics, training=None):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({'model': regressor, 'classifier': classifier, 'features': FEATURES, 'metrics': metrics}, out)

    if metrics_out_path:
        metrics_out = Path(metrics_out_path)
        metrics_out.parent.mkdir(parents=True, exist_ok=True)
        metrics_out.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

    predictions = build_test_predictions(training) if training else None
    if predictions_out_path and training:
        predictions_out = Path(predictions_out_path)
        predictions_out.parent.mkdir(parents=True, exist_ok=True)
        predictions.to_csv(predictions_out, index=False, encoding='utf-8')

    if model_card_out_path:
        model_card_out = Path(model_card_out_path)
        model_card_out.parent.mkdir(parents=True, exist_ok=True)
        model_card_out.write_text(build_model_card_markdown(metrics, predictions=predictions), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/final/dataset_coupures_2020_2026.csv')
    parser.add_argument('--out', default='ml/model.pkl')
    parser.add_argument('--metrics-out', default=None)
    parser.add_argument('--model-card-out', default=None)
    parser.add_argument('--predictions-out', default=None)
    parser.add_argument('--n-estimators', type=int, default=160)
    parser.add_argument('--test-size', type=float, default=0.2)
    parser.add_argument('--random-state', type=int, default=42)
    parser.add_argument('--class-weight', choices=['none', 'balanced'], default='none')
    parser.add_argument('--real-only', action='store_true', help='Exclude simulation rows and train on official/media/field sources.')
    args = parser.parse_args()

    df, dataset_info = prepare_dataset(pd.read_csv(args.input), real_only=args.real_only)
    if args.real_only:
        print(f"Donnees reelles conservees: {dataset_info['usable_rows']}/{dataset_info['source_rows']} lignes.")

    model_params = {
        'n_estimators': args.n_estimators,
        'test_size': args.test_size,
        'random_state': args.random_state,
        'class_weight': None if args.class_weight == 'none' else args.class_weight,
    }
    training = train_models(df, **model_params)
    metrics = build_metrics(training, df, dataset_info, args.input, args.real_only, model_params=model_params)
    save_outputs(args.out, args.metrics_out, args.model_card_out, args.predictions_out, training['regressor'], training['classifier'], metrics, training=training)
    print(metrics)


if __name__ == '__main__':
    main()
