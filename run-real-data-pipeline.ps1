param(
    [switch]$SkipNetwork,
    [switch]$LoadDb
)

$ErrorActionPreference = "Stop"
$Python = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

$RunId = (& $Python processing\pipeline_logger.py start --name real_data_pipeline).Trim()

try {
    if (-not $SkipNetwork) {
        & $Python ingestion\scrape_medias.py --out data\raw\medias\articles_collectes.csv --structured-out data\raw\medias\coupures_structurees.csv
        & $Python ingestion\download_openmeteo.py --lat 12.3714 --lon -1.5197 --start 2025-12-27 --end 2026-03-07 --out data\raw\weather\openmeteo_ouagadougou_2025-12-27_2026-03-07.csv
        & $Python ingestion\download_nasa_power.py --lat 12.3714 --lon -1.5197 --start 20251227 --end 20260307 --out data\raw\solar\nasa_power_ouagadougou_2025-12-27_2026-03-07.csv
        & $Python ingestion\download_worldbank.py --indicator EG.ELC.ACCS.ZS --country BF --out data\raw\worldbank\electricity_access_bf.csv
    }

    & $Python processing\enrich_real_coupures.py --coupures data\raw\medias\coupures_structurees.csv --weather data\raw\weather\openmeteo_ouagadougou_2025-12-27_2026-03-07.csv --solar data\raw\solar\nasa_power_ouagadougou_2025-12-27_2026-03-07.csv --out data\final\dataset_coupures_reelles_collectees.csv
    & $Python processing\merge_real_datasets.py --base data\final\dataset_coupures_2020_2026.csv --collected data\final\dataset_coupures_reelles_collectees.csv --out data\final\dataset_coupures_reelles_combine.csv
    & $Python analytics\generate_indicators.py --input data\final\dataset_coupures_reelles_combine.csv --real-only --out data\processed\indicateurs_reels.json
    & $Python ml\train_model.py --input data\final\dataset_coupures_reelles_combine.csv --real-only --out ml\model_real.pkl --metrics-out data\processed\model_metrics_real.json --n-estimators 160 --test-size 0.2 --random-state 42 --class-weight none

    if ($LoadDb) {
        docker compose up -d
        & $Python ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures
    }

    & $Python -m pytest -q
    $Records = ((Import-Csv data\final\dataset_coupures_reelles_combine.csv) | Measure-Object).Count
    & $Python processing\pipeline_logger.py finish --run-id $RunId --status success --records-read $Records --records-inserted $Records --records-rejected 0
}
catch {
    $Message = $_.Exception.Message
    & $Python processing\pipeline_logger.py finish --run-id $RunId --status failed --error-message $Message
    throw
}
