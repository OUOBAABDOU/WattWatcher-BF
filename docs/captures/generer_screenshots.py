import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:5000"
CAPTURES_DIR = Path(__file__).parent

# Pages to capture
PAGES = [
    ("01_tableau_bord_coupures.png", "/"),
    ("02_coupures_par_region.png", "/suivi"),
    ("03_carte_zones_touchees.png", "/carte"),
    ("04_gestion_coupures.png", "/coupures"),
    ("05_repartition_source.png", "/"),  # Dashboard shows source distribution
    ("06_repartition_statut.png", "/"),  # Dashboard shows status distribution
    ("07_recommandations_energetiques.png", "/recommandations"),
    ("08_qualite_donnees.png", "/qualite"),
    ("09_tracabilite_sources.png", "/sources"),
    ("10_zones_cartographiees.png", "/pipeline"),
    ("11_modele_predictif_ml.png", "/modele"),
    ("12_fiche_modele.png", "/modele/fiche"),
    ("13_erreurs_modele.png", "/modele/erreurs"),
    ("14_prediction_duree_avant.png", "/prediction"),
    ("15_prediction_duree_apres.png", "/prediction"),  # Will need to fill form
    ("16_navigation_menu.png", "/"),
    ("17_dashboard_kpis.png", "/"),
    ("18_dashboard_graphiques.png", "/"),
    ("19_suivi_actives.png", "/suivi"),
    ("20_accueil_complet.png", "/"),
]

def capture_page(driver, filename, url, fill_form=False):
    """Capture a screenshot of a page"""
    try:
        driver.get(f"{BASE_URL}{url}")
        
        # Wait for page to fully load
        time.sleep(2)
        
        # If this is the prediction page, fill the form
        if fill_form and "prediction" in url:
            try:
                driver.find_element(By.NAME, "region").send_keys("Centre")
                driver.find_element(By.NAME, "ville").send_keys("Ouagadougou")
                driver.find_element(By.NAME, "type_coupure").send_keys("planifiée")
                driver.find_element(By.NAME, "cause").send_keys("maintenance")
                driver.find_element(By.NAME, "temperature_max").send_keys("35")
                driver.find_element(By.NAME, "precipitation").send_keys("0")
                driver.find_element(By.NAME, "irradiation_solaire").send_keys("250")
                driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
                time.sleep(2)
            except Exception as e:
                print(f"  [AVERTISSEMENT] Impossible de remplir le formulaire: {e}")
        
        # Take full page screenshot
        output_path = CAPTURES_DIR / filename
        driver.save_screenshot(str(output_path))
        print(f"  [OK] {filename}")
    except Exception as e:
        print(f"  [ERREUR] {filename}: {e}")

def main():
    """Main function to capture all screenshots"""
    print("=== Génération des captures d'écran avec Selenium ===")
    print(f"Application accessible sur : {BASE_URL}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for filename, url in PAGES:
            fill_form = "apres" in filename
            capture_page(driver, filename, url, fill_form)
    finally:
        driver.quit()
    
    print("\n=== Génération terminée ===")
    print(f"Captures sauvegardées dans : {CAPTURES_DIR}")

if __name__ == "__main__":
    main()
