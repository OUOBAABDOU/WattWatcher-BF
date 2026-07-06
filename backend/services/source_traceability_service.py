import csv
from pathlib import Path

from config import BASE_DIR


CATALOG_PATH = BASE_DIR / 'data' / 'raw' / 'source_catalog.csv'
SEEDS_PATH = BASE_DIR / 'data' / 'raw' / 'url_seeds_sonabel_medias.csv'
TRACKED_FILES = (
    BASE_DIR / 'data' / 'raw' / 'medias' / 'articles_collectes.csv',
    BASE_DIR / 'data' / 'raw' / 'medias' / 'coupures_structurees.csv',
    BASE_DIR / 'data' / 'final' / 'dataset_coupures_reelles.csv',
    BASE_DIR / 'data' / 'final' / 'dataset_coupures_reelles_collectees.csv',
    BASE_DIR / 'data' / 'final' / 'dataset_coupures_reelles_combine.csv',
    BASE_DIR / 'data' / 'processed' / 'indicateurs_reels.json',
    BASE_DIR / 'data' / 'processed' / 'model_metrics_real.json',
)


def _read_csv_rows(path, limit=None):
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8-sig') as file:
        rows = list(csv.DictReader(file))
    return rows[:limit] if limit else rows


def _count_csv_rows(path):
    return len(_read_csv_rows(path)) if path.exists() and path.suffix.lower() == '.csv' else None


def _summarize_files():
    items = []
    for path in TRACKED_FILES:
        exists = path.exists()
        items.append({
            'path': str(path.relative_to(BASE_DIR)),
            'exists': exists,
            'size_kb': round(path.stat().st_size / 1024, 2) if exists else 0,
            'rows': _count_csv_rows(path) if exists else None,
        })
    return items


def _source_distribution():
    dataset = BASE_DIR / 'data' / 'final' / 'dataset_coupures_reelles_combine.csv'
    rows = _read_csv_rows(dataset)
    distribution = {}
    for row in rows:
        source_type = row.get('source_type') or 'Non renseigné'
        distribution[source_type] = distribution.get(source_type, 0) + 1
    return [
        {'label': label, 'value': value}
        for label, value in sorted(distribution.items(), key=lambda item: item[1], reverse=True)
    ]


def get_source_traceability():
    catalog = _read_csv_rows(CATALOG_PATH)
    seeds = _read_csv_rows(SEEDS_PATH)
    files = _summarize_files()
    combined = next((item for item in files if item['path'].endswith('dataset_coupures_reelles_combine.csv')), {})
    return {
        'catalog': catalog,
        'seeds': seeds,
        'files': files,
        'source_distribution': _source_distribution(),
        'kpis': {
            'catalog_sources': len(catalog),
            'seed_urls': len(seeds),
            'tracked_files': len(files),
            'combined_rows': combined.get('rows') or 0,
        },
    }
