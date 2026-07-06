# Guide d’installation

## Prérequis

- Python 3.10 ou 3.11 recommandé
- Docker Desktop
- Git
- Tesseract OCR si vous voulez tester l’OCR image

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Vérifier que `.env` pointe vers PostgreSQL Docker :

```text
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/wattwatcher_db
```

## Lancer PostgreSQL

```powershell
docker compose up -d
```

## Charger les données

```powershell
python ingestion/load_to_postgres.py --csv data/final/dataset_coupures_2020_2026.csv
```

## Lancer l’application

```powershell
python backend/app.py
```

Ouvrir : http://127.0.0.1:5000

## Scraping média

```powershell
python ingestion/scrape_medias.py
python ingestion/scrape_medias.py --load-db
```

## Analyse et modèle

```powershell
python analytics/generate_indicators.py
python analytics/eda.py
python ml/train_model.py
python ml/predict.py
```

## Tests

```powershell
python -m pytest -q
```
