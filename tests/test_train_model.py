import joblib
import pandas as pd

from ml.train_model import FEATURES, base_feature_name, build_metrics, build_model_card_markdown, build_models, build_test_predictions, confidence_level, dataset_profile, duration_class, prepare_dataset, save_outputs, summarize_test_predictions


class DummyModel:
    pass


class PredictingRegressor:
    def predict(self, X):
        return [100 for _ in range(len(X))]


class PredictingClassifier:
    classes_ = ['courte', 'moyenne']

    def predict(self, X):
        return ['moyenne' for _ in range(len(X))]

    def predict_proba(self, X):
        return [[0.25, 0.75] for _ in range(len(X))]


def _row(source_type, source_name, duration):
    return {
        'date_debut': '2026-01-03',
        'heure_debut': '08:30',
        'duree_minutes': duration,
        'mois': 1,
        'region': 'Centre',
        'ville': 'Ouagadougou',
        'zone': 'Tanghin',
        'type_coupure': 'prevue',
        'temperature_max': 38.0,
        'precipitation': 0.0,
        'irradiation_solaire': 5.8,
        'source_type': source_type,
        'source_name': source_name,
    }


def test_duration_class_boundaries():
    assert duration_class(60) == 'courte'
    assert duration_class(61) == 'moyenne'
    assert duration_class(240) == 'moyenne'
    assert duration_class(241) == 'longue'


def test_confidence_level_boundaries():
    assert confidence_level(0.44) == 'faible'
    assert confidence_level(0.45) == 'moyenne'
    assert confidence_level(0.65) == 'elevee'


def test_prepare_dataset_adds_features_and_filters_real_rows():
    df = pd.DataFrame([
        _row('officielle', 'SONABEL', 60),
        _row('simulation', 'Donnee experimentale', 300),
    ])

    prepared, dataset_info = prepare_dataset(df, real_only=True)

    assert dataset_info == {'source_rows': 2, 'usable_rows': 1}
    assert prepared.iloc[0]['classe_duree'] == 'courte'
    assert prepared.iloc[0]['heure_num'] == 8
    assert prepared.iloc[0]['jour_num'] == 5
    assert set(FEATURES).issubset(prepared.columns)


def test_dataset_profile_summarizes_classes_and_durations():
    df = pd.DataFrame({
        'classe_duree': ['courte', 'moyenne', 'moyenne'],
        'duree_minutes': [30, 120, 240],
    })

    profile = dataset_profile(df)

    assert profile['class_distribution'] == {'courte': 1, 'moyenne': 2}
    assert profile['class_balance'] == {
        'majority_class': 'moyenne',
        'majority_count': 2,
        'minority_class': 'courte',
        'minority_count': 1,
        'imbalance_ratio': 2.0,
    }
    assert profile['duration_stats']['median'] == 120.0
    assert profile['duration_stats']['mean'] == 130.0


def test_build_models_uses_configurable_random_forest_params():
    regressor, classifier = build_models(n_estimators=7, random_state=13, class_weight='balanced')

    assert regressor.named_steps['regressor'].n_estimators == 7
    assert regressor.named_steps['regressor'].random_state == 13
    assert classifier.named_steps['classifier'].n_estimators == 7
    assert classifier.named_steps['classifier'].random_state == 13
    assert classifier.named_steps['classifier'].class_weight == 'balanced'


def test_build_metrics_includes_model_params():
    df = pd.DataFrame({'classe_duree': ['courte', 'moyenne'], 'duree_minutes': [60, 120]})

    class ConstantRegressor:
        def predict(self, X):
            return [60, 120]

    class ConstantClassifier:
        def predict(self, X):
            return ['courte', 'moyenne']

    training = {
        'regressor': ConstantRegressor(),
        'classifier': ConstantClassifier(),
        'X_train': pd.DataFrame([{}]),
        'X_test': pd.DataFrame([{}, {}]),
        'y_reg_train': pd.Series([90]),
        'y_reg_test': pd.Series([60, 120]),
        'y_cls_train': pd.Series(['moyenne']),
        'y_cls_test': pd.Series(['courte', 'moyenne']),
    }
    params = {'n_estimators': 7, 'test_size': 0.25, 'random_state': 13}

    metrics = build_metrics(training, df, {'source_rows': 2, 'usable_rows': 2}, 'input.csv', True, model_params=params)

    assert metrics['model_params'] == params
    assert metrics['classification']['accuracy'] == 1.0
    assert metrics['classification']['report']['courte']['precision'] == 1.0
    assert metrics['classification']['confusion_matrix'] == [[1, 0], [0, 1]]
    assert metrics['classification']['baseline_majority_class']['class'] == 'moyenne'
    assert metrics['classification']['baseline_majority_class']['accuracy'] == 0.5
    assert metrics['regression']['baseline_mean_duration']['prediction_minutes'] == 90.0
    assert metrics['feature_importance'] == {'regression': [], 'classification': []}
    assert metrics['dataset']['class_distribution'] == {'courte': 1, 'moyenne': 1}
    assert metrics['dataset']['class_balance']['imbalance_ratio'] == 1.0


def test_base_feature_name_groups_encoded_columns():
    assert base_feature_name('cat__region_Centre') == 'region'
    assert base_feature_name('cat__type_coupure_prévue') == 'type_coupure'
    assert base_feature_name('num__temperature_max') == 'temperature_max'
def test_build_model_card_markdown_contains_report_sections():
    metrics = {
        'regression': {'MAE': 10.2, 'RMSE': 12.5, 'R2': 0.1},
        'classification': {
            'accuracy': 0.7,
            'baseline_majority_class': {'class': 'moyenne', 'accuracy': 0.5},
        },
        'dataset': {
            'input': 'data.csv',
            'real_only': True,
            'usable_rows': 20,
            'train_rows': 16,
            'test_rows': 4,
            'class_distribution': {'courte': 4, 'moyenne': 16},
            'class_balance': {
                'majority_class': 'moyenne',
                'majority_count': 16,
                'minority_class': 'courte',
                'minority_count': 4,
                'imbalance_ratio': 4.0,
            },
            'duration_stats': {'min': 30, 'median': 120, 'mean': 130, 'max': 300},
        },
        'feature_importance': {'regression': [{'feature': 'temperature_max', 'importance': 0.4}]},
    }

    markdown = build_model_card_markdown(metrics)

    assert '# Fiche modele ML' in markdown
    assert '## Resultats principaux' in markdown
    assert '## Distribution des classes' in markdown
    assert '## Desequilibre des classes' in markdown
    assert 'temperature_max' in markdown


def test_build_model_card_markdown_can_include_prediction_errors():
    metrics = {
        'regression': {'MAE': 10.2, 'RMSE': 12.5, 'R2': 0.1},
        'classification': {
            'accuracy': 0.7,
            'baseline_majority_class': {'class': 'moyenne', 'accuracy': 0.5},
        },
        'dataset': {
            'input': 'data.csv',
            'real_only': True,
            'usable_rows': 20,
            'train_rows': 16,
            'test_rows': 4,
        },
        'feature_importance': {'regression': []},
    }
    predictions = pd.DataFrame([
        {
            'region': 'Centre',
            'ville': 'Ouagadougou',
            'zone': 'Tanghin',
            'actual_duration': 90,
            'predicted_duration': 100,
            'absolute_error': 10,
            'actual_class': 'moyenne',
            'predicted_class': 'moyenne',
            'classification_correct': True,
        },
        {
            'region': 'Nord',
            'ville': 'Ouahigouya',
            'zone': 'Secteur 2',
            'actual_duration': 300,
            'predicted_duration': 100,
            'absolute_error': 200,
            'actual_class': 'longue',
            'predicted_class': 'moyenne',
            'classification_correct': False,
        },
    ])

    markdown = build_model_card_markdown(metrics, predictions=predictions)

    assert '## Analyse des erreurs de test' in markdown
    assert '2 lignes de test analysees' in markdown
    assert 'Nord / Ouahigouya / Secteur 2' in markdown


def test_summarize_test_predictions_returns_error_summary():
    predictions = pd.DataFrame([
        {'absolute_error': 10, 'classification_correct': True},
        {'absolute_error': 30, 'classification_correct': False},
    ])

    summary = summarize_test_predictions(predictions)

    assert summary['rows'] == 2
    assert summary['mae_from_predictions'] == 20.0
    assert summary['classification_accuracy'] == 0.5
    assert summary['misclassified_rows'] == 1


def test_save_outputs_can_write_model_card(tmp_path):
    metrics = {
        'regression': {'MAE': 10.2, 'RMSE': 12.5, 'R2': 0.1},
        'classification': {
            'accuracy': 0.7,
            'baseline_majority_class': {'class': 'moyenne', 'accuracy': 0.5},
        },
        'dataset': {
            'input': 'data.csv',
            'real_only': True,
            'usable_rows': 20,
            'train_rows': 16,
            'test_rows': 4,
        },
        'feature_importance': {'regression': []},
    }
    model_path = tmp_path / 'model.pkl'
    metrics_path = tmp_path / 'metrics.json'
    card_path = tmp_path / 'fiche.md'

    save_outputs(model_path, metrics_path, card_path, None, DummyModel(), DummyModel(), metrics)

    assert joblib.load(model_path)['metrics'] == metrics
    assert metrics_path.exists()
    assert '# Fiche modele ML' in card_path.read_text(encoding='utf-8')


def test_build_test_predictions_includes_errors_and_probabilities():
    training = {
        'regressor': PredictingRegressor(),
        'classifier': PredictingClassifier(),
        'X_test': pd.DataFrame([{'region': 'Centre'}, {'region': 'Nord'}]),
        'y_reg_test': pd.Series([90, 130]),
        'y_cls_test': pd.Series(['moyenne', 'courte']),
    }

    rows = build_test_predictions(training)

    assert list(rows['predicted_duration']) == [100.0, 100.0]
    assert list(rows['absolute_error']) == [10.0, 30.0]
    assert 'proba_courte' in rows.columns
    assert 'proba_moyenne' in rows.columns
    assert list(rows['predicted_class_confidence']) == [0.75, 0.75]
    assert list(rows['confidence_level']) == ['elevee', 'elevee']


def test_save_outputs_can_write_test_predictions(tmp_path):
    metrics = {
        'regression': {'MAE': 10.2, 'RMSE': 12.5, 'R2': 0.1},
        'classification': {
            'accuracy': 0.7,
            'baseline_majority_class': {'class': 'moyenne', 'accuracy': 0.5},
        },
        'dataset': {
            'input': 'data.csv',
            'real_only': True,
            'usable_rows': 20,
            'train_rows': 16,
            'test_rows': 4,
        },
        'feature_importance': {'regression': []},
    }
    training = {
        'regressor': PredictingRegressor(),
        'classifier': PredictingClassifier(),
        'X_test': pd.DataFrame([{'region': 'Centre'}]),
        'y_reg_test': pd.Series([90]),
        'y_cls_test': pd.Series(['moyenne']),
    }
    predictions_path = tmp_path / 'predictions.csv'

    save_outputs(tmp_path / 'model.pkl', None, None, predictions_path, DummyModel(), DummyModel(), metrics, training=training)

    predictions = pd.read_csv(predictions_path)
    assert predictions.iloc[0]['predicted_class'] == 'moyenne'
    assert predictions.iloc[0]['absolute_error'] == 10.0
    assert predictions.iloc[0]['predicted_class_confidence'] == 0.75


def test_save_outputs_model_card_includes_prediction_errors_when_training_is_available(tmp_path):
    metrics = {
        'regression': {'MAE': 10.2, 'RMSE': 12.5, 'R2': 0.1},
        'classification': {
            'accuracy': 0.7,
            'baseline_majority_class': {'class': 'moyenne', 'accuracy': 0.5},
        },
        'dataset': {
            'input': 'data.csv',
            'real_only': True,
            'usable_rows': 20,
            'train_rows': 16,
            'test_rows': 4,
        },
        'feature_importance': {'regression': []},
    }
    training = {
        'regressor': PredictingRegressor(),
        'classifier': PredictingClassifier(),
        'X_test': pd.DataFrame([{'region': 'Centre', 'ville': 'Ouagadougou', 'zone': 'Tanghin'}]),
        'y_reg_test': pd.Series([90]),
        'y_cls_test': pd.Series(['moyenne']),
    }
    card_path = tmp_path / 'fiche.md'

    save_outputs(tmp_path / 'model.pkl', None, card_path, None, DummyModel(), DummyModel(), metrics, training=training)

    assert '## Analyse des erreurs de test' in card_path.read_text(encoding='utf-8')
