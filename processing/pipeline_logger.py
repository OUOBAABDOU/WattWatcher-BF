from datetime import datetime
import argparse
import os
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


def get_engine():
    return create_engine(os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5433/wattwatcher_db'))


def ensure_pipeline_schema(engine):
    statement = """
    CREATE TABLE IF NOT EXISTS pipeline_runs (
        id_run SERIAL PRIMARY KEY,
        pipeline_name VARCHAR(120) NOT NULL,
        date_start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        date_end TIMESTAMP,
        status VARCHAR(40) NOT NULL DEFAULT 'running',
        records_read INT DEFAULT 0,
        records_inserted INT DEFAULT 0,
        records_rejected INT DEFAULT 0,
        error_message TEXT
    )
    """
    with engine.begin() as conn:
        conn.execute(text(statement))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_pipeline_runs_date ON pipeline_runs(date_start)"))


def start_run(pipeline_name):
    engine = get_engine()
    ensure_pipeline_schema(engine)
    with engine.begin() as conn:
        run_id = conn.execute(
            text("INSERT INTO pipeline_runs (pipeline_name, status) VALUES (:name, 'running') RETURNING id_run"),
            {'name': pipeline_name},
        ).scalar()
    return int(run_id)


def finish_run(run_id, status='success', records_read=0, records_inserted=0, records_rejected=0, error_message=None):
    engine = get_engine()
    ensure_pipeline_schema(engine)
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE pipeline_runs
                SET date_end = :date_end,
                    status = :status,
                    records_read = :records_read,
                    records_inserted = :records_inserted,
                    records_rejected = :records_rejected,
                    error_message = :error_message
                WHERE id_run = :run_id
            """),
            {
                'date_end': datetime.utcnow(),
                'status': status,
                'records_read': records_read,
                'records_inserted': records_inserted,
                'records_rejected': records_rejected,
                'error_message': error_message,
                'run_id': run_id,
            },
        )


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    start = sub.add_parser('start')
    start.add_argument('--name', required=True)
    finish = sub.add_parser('finish')
    finish.add_argument('--run-id', type=int, required=True)
    finish.add_argument('--status', default='success')
    finish.add_argument('--records-read', type=int, default=0)
    finish.add_argument('--records-inserted', type=int, default=0)
    finish.add_argument('--records-rejected', type=int, default=0)
    finish.add_argument('--error-message', default=None)
    args = parser.parse_args()

    if args.command == 'start':
        print(start_run(args.name))
    else:
        finish_run(args.run_id, args.status, args.records_read, args.records_inserted, args.records_rejected, args.error_message)
        print(args.run_id)


if __name__ == '__main__':
    main()
