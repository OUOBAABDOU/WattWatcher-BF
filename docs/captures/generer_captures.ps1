# Script pour générer les captures d'écran de l'application WattWatcher BF
# Nécessite que l'application Flask soit démarrée sur http://127.0.0.1:5000

$baseUrl = "http://127.0.0.1:5000"
$outputDir = "docs\captures"

# Créer le répertoire de sortie s'il n'existe pas
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Liste des pages à capturer
$pages = @(
    @{Name="dashboard_principal"; Url="/"},
    @{Name="suivi_coupures"; Url="/suivi"},
    @{Name="carte_zones"; Url="/carte"},
    @{Name="modele_ml"; Url="/modele"},
    @{Name="fiche_modele"; Url="/modele/fiche"},
    @{Name="prediction_ml"; Url="/prediction"},
    @{Name="qualite_donnees"; Url="/qualite"},
    @{Name="sources_donnees"; Url="/sources"},
    @{Name="recommandations"; Url="/recommandations"},
    @{Name="notifications"; Url="/notifications"}
)

Write-Host "=== Génération des captures d'écran WattWatcher BF ===" -ForegroundColor Green
Write-Host "Application accessible sur : $baseUrl" -ForegroundColor Yellow
Write-Host ""

foreach ($page in $pages) {
    $url = $baseUrl + $page.Url
    $outputFile = Join-Path $outputDir ($page.Name + ".html")
    
    Write-Host "Téléchargement : $($page.Name)" -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri $url -OutFile $outputFile -ErrorAction Stop
        Write-Host "  ✓ Sauvegardé dans : $outputFile" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ Erreur : $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Téléchargement terminé ===" -ForegroundColor Green
Write-Host ""
Write-Host "Pour les captures d'écran visuelles (PNG) :" -ForegroundColor Yellow
Write-Host "1. Ouvrez le navigateur sur $baseUrl" -ForegroundColor White
Write-Host "2. Naviguez sur chaque page listée dans guide_captures.md" -ForegroundColor White
Write-Host "3. Utilisez Windows + Shift + S pour capturer" -ForegroundColor White
Write-Host "4. Enregistrez dans $outputDir" -ForegroundColor White
