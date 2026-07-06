REQUIRED_COLUMNS = [
    'date_debut',
    'heure_debut',
    'heure_fin',
    'duree_minutes',
    'region',
    'ville',
    'zone',
    'source_name',
    'source_type',
    'url_source',
]

DEDUP_COLUMNS = ['date_debut', 'heure_debut', 'heure_fin', 'ville', 'zone', 'url_source']
VALID_SOURCE_TYPES = {'officielle', 'media', 'terrain', 'interne', 'simulation'}


def _missing_count(series):
    return int(series.isna().sum() + series.astype(str).str.strip().isin(['', 'nan', 'None']).sum())


def completeness_by_column(df, columns=None):
    columns = columns or [col for col in REQUIRED_COLUMNS if col in df.columns]
    total = len(df)
    if total == 0:
        return {col: 100.0 for col in columns}
    return {
        col: round(100 * (1 - (_missing_count(df[col]) / total)), 2)
        for col in columns
    }


def detect_anomalies(df):
    anomalies = {}
    if 'duree_minutes' in df.columns:
        anomalies['duree_negative_or_zero'] = int((df['duree_minutes'].fillna(0) <= 0).sum())
    if 'date_debut' in df.columns and 'date_fin' in df.columns:
        start = df['date_debut'].astype(str)
        end = df['date_fin'].astype(str)
        anomalies['date_fin_before_date_debut'] = int((end < start).sum())
    if 'source_type' in df.columns:
        source_types = df['source_type'].astype(str).str.strip().str.lower()
        anomalies['source_type_inconnu'] = int((~source_types.isin(VALID_SOURCE_TYPES)).sum())
    return anomalies


def data_quality_report(df):
    total = int(len(df))
    dedup_columns = [col for col in DEDUP_COLUMNS if col in df.columns]
    duplicate_count = int(df.duplicated(subset=dedup_columns).sum()) if dedup_columns else 0
    completeness = completeness_by_column(df)
    anomalies = detect_anomalies(df)
    source_distribution = df['source_type'].fillna('Non renseigne').astype(str).value_counts().to_dict() if 'source_type' in df.columns else {}
    avg_completeness = round(sum(completeness.values()) / len(completeness), 2) if completeness else 100.0
    anomaly_total = int(sum(anomalies.values()))
    quality_score = max(0.0, round(avg_completeness - min(30, duplicate_count * 2) - min(30, anomaly_total * 5), 2))

    return {
        'total_lignes': total,
        'completude_moyenne': avg_completeness,
        'completude_par_colonne': completeness,
        'doublons': duplicate_count,
        'anomalies': anomalies,
        'anomalies_total': anomaly_total,
        'repartition_sources': {str(k): int(v) for k, v in source_distribution.items()},
        'score_qualite': quality_score,
    }
