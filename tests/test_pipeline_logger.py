from processing.pipeline_logger import finish_run, start_run


def test_pipeline_logger_creates_and_finishes_run(monkeypatch):
    calls = []

    class FakeResult:
        def scalar(self):
            return 42

    class FakeConnection:
        def execute(self, statement, params=None):
            calls.append((str(statement), params))
            return FakeResult()

    class FakeTransaction:
        def __enter__(self):
            return FakeConnection()

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeEngine:
        def begin(self):
            return FakeTransaction()

    monkeypatch.setattr('processing.pipeline_logger.get_engine', lambda: FakeEngine())

    run_id = start_run('test_pipeline')
    finish_run(run_id, status='success', records_read=2, records_inserted=1, records_rejected=1)

    assert run_id == 42
    assert any('INSERT INTO pipeline_runs' in call[0] for call in calls)
    assert any('UPDATE pipeline_runs' in call[0] for call in calls)
