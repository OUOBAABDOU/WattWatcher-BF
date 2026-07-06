from pathlib import Path

import joblib

from ml import predict


class DummyRegressor:
    def predict(self, row):
        return [180]


class DummyClassifier:
    classes_ = ['courte', 'longue']

    def predict(self, row):
        return ['longue']

    def predict_proba(self, row):
        return [[0.25, 0.75]]


def test_resolve_model_path_prefers_real_model(tmp_path, monkeypatch):
    real_model = tmp_path / 'model_real.pkl'
    fallback_model = tmp_path / 'model.pkl'
    real_model.write_text('real')
    fallback_model.write_text('fallback')
    monkeypatch.setattr(predict, 'DEFAULT_MODEL_PATHS', (real_model, fallback_model))

    assert predict.resolve_model_path() == real_model


def test_resolve_model_path_uses_explicit_path(tmp_path):
    explicit_model = tmp_path / 'custom.pkl'

    assert predict.resolve_model_path(explicit_model) == explicit_model


def test_resolve_model_path_falls_back_to_standard_model(tmp_path, monkeypatch):
    real_model = tmp_path / 'model_real.pkl'
    fallback_model = tmp_path / 'model.pkl'
    monkeypatch.setattr(predict, 'DEFAULT_MODEL_PATHS', (real_model, fallback_model))

    assert predict.resolve_model_path() == fallback_model


def test_predict_duration_returns_class_probabilities(tmp_path):
    model_path = tmp_path / 'model.pkl'
    joblib.dump({
        'model': DummyRegressor(),
        'classifier': DummyClassifier(),
        'features': ['region'],
    }, model_path)

    result = predict.predict_duration(model_path=model_path, region='Centre')

    assert result['classe_duree'] == 'longue'
    assert result['classe_confiance'] == 0.75
    assert result['classe_proba'] == {'courte': 0.25, 'longue': 0.75}
