from models import PipelineRun


def list_pipeline_runs(limit=20):
    runs = PipelineRun.query.order_by(PipelineRun.date_start.desc()).limit(limit).all()
    return [
        {
            'id_run': run.id_run,
            'pipeline_name': run.pipeline_name,
            'date_start': run.date_start.isoformat() if run.date_start else None,
            'date_end': run.date_end.isoformat() if run.date_end else None,
            'status': run.status,
            'records_read': run.records_read or 0,
            'records_inserted': run.records_inserted or 0,
            'records_rejected': run.records_rejected or 0,
            'error_message': run.error_message,
        }
        for run in runs
    ]
