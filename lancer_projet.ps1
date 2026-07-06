# Script pour lancer le projet WattWatcher BF en une seule fois
# Ce script demarre PostgreSQL, charge les donnees reelles et lance l'application

Write-Host "=== Lancement du projet WattWatcher BF ===" -ForegroundColor Green
Write-Host ""

# 1. Demarrer PostgreSQL avec Docker
Write-Host "[1/4] Demarrage de PostgreSQL avec Docker..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "PostgreSQL demarre avec succes" -ForegroundColor Green
} else {
    Write-Host "Erreur lors du demarrage de PostgreSQL" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Attendre que PostgreSQL soit pret
Write-Host "Attente de PostgreSQL (5 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Write-Host ""

# 2. Charger les donnees reelles dans PostgreSQL
Write-Host "[2/4] Chargement des donnees reelles dans PostgreSQL..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures
if ($LASTEXITCODE -eq 0) {
    Write-Host "Donnees chargees avec succes" -ForegroundColor Green
} else {
    Write-Host "Erreur lors du chargement des donnees" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. Lancer l'application Flask
Write-Host "[3/4] Demarrage de l'application Flask..." -ForegroundColor Yellow
Write-Host "Application accessible sur : http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Appuyez sur Ctrl+C pour arreter l'application" -ForegroundColor Cyan
Write-Host ""
.\.venv\Scripts\python.exe backend\app.py
