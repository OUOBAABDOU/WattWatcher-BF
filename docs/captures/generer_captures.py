"""Script pour télécharger les pages HTML de l'application WattWatcher BF"""
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"
OUTPUT_DIR = Path("docs/captures")

# Créer le répertoire de sortie
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Liste des pages à télécharger (20 captures)
pages = [
    # Section 1 - Pages principales
    ("01_dashboard_principal", "/"),
    ("02_suivi_coupures", "/suivi"),
    ("03_carte_zones", "/carte"),
    ("04_liste_coupures", "/coupures"),
    ("05_signalements", "/signalements"),
    ("06_notifications", "/notifications"),
    ("07_recommandations", "/recommandations"),
    ("08_qualite_donnees", "/qualite"),
    ("09_sources_donnees", "/sources"),
    ("10_pipeline", "/pipeline"),
    # Section 2 - Machine Learning
    ("11_modele_ml", "/modele"),
    ("12_fiche_modele", "/modele/fiche"),
    ("13_erreurs_modele", "/modele/erreurs"),
    ("14_prediction_formulaire", "/prediction"),
    ("15_prediction_resultat", "/prediction"),
]

print("=== Téléchargement des pages WattWatcher BF ===")
print(f"Application accessible sur : {BASE_URL}")
print()

for name, path in pages:
    url = BASE_URL + path
    output_file = OUTPUT_DIR / f"{name}.html"
    
    print(f"Telechargement : {name}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        output_file.write_text(response.text, encoding='utf-8')
        print(f"  [OK] Sauvegarde dans : {output_file}")
    except Exception as e:
        print(f"  [ERREUR] : {e}")

print()
print("=== Téléchargement terminé ===")
print()
print("Pour les captures d'écran visuelles (PNG) :")
print("1. Ouvrez le navigateur sur http://127.0.0.1:5000")
print("2. Naviguez sur chaque page listée dans guide_captures.md")
print("3. Utilisez Windows + Shift + S pour capturer")
print("4. Enregistrez dans docs/captures/")
