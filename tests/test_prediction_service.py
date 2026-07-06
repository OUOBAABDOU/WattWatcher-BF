import os
import sys

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
sys.path.insert(0, "backend")

from services.prediction_service import interpret_confidence


def test_interpret_confidence_levels():
    assert interpret_confidence(None)['niveau_confiance'] == 'inconnu'
    assert interpret_confidence(0.44)['niveau_confiance'] == 'faible'
    assert interpret_confidence(0.45)['niveau_confiance'] == 'moyenne'
    assert interpret_confidence(0.65)['niveau_confiance'] == 'élevée'
