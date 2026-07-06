# Guide complet pour les captures de graphiques

## Graphiques existants dans l'application

### 1. Dashboard principal (http://127.0.0.1:5000)

L'application contient **6 graphiques interactifs** sur le dashboard :

#### Graphique 1 : Coupures par région
- **Type** : Bar chart (histogramme)
- **Données** : Nombre de coupures par région
- **Position** : Panneau en haut à gauche
- **Comment capturer** : 
  1. Ouvrir http://127.0.0.1:5000
  2. Appuyer sur F11 (plein écran)
  3. Zoomer sur le panneau "Coupures par région"
  4. Windows + Shift + S pour capturer
  5. Enregistrer : `graphique_coupures_par_region.png`

#### Graphique 2 : Coupures par mois
- **Type** : Line chart (courbe)
- **Données** : Évolution mensuelle des coupures
- **Position** : Panneau en haut au centre
- **Comment capturer** : 
  1. Zoomer sur le panneau "Coupures par mois"
  2. Windows + Shift + S pour capturer
  3. Enregistrer : `graphique_coupures_par_mois.png`

#### Graphique 3 : Répartition par source
- **Type** : Pie chart (camembert)
- **Données** : Répartition des coupures par source (SONABEL, médias, etc.)
- **Position** : Panneau en haut à droite
- **Comment capturer** : 
  1. Zoomer sur le panneau "Répartition par source"
  2. Windows + Shift + S pour capturer
  3. Enregistrer : `graphique_repartition_source.png`

#### Graphique 4 : Répartition par statut
- **Type** : Bar chart
- **Données** : Coupures par statut (terminée, en cours, prévue)
- **Position** : Panneau en bas à gauche
- **Comment capturer** : 
  1. Zoomer sur le panneau "Répartition par statut"
  2. Windows + Shift + S pour capturer
  3. Enregistrer : `graphique_repartition_statut.png`

#### Graphique 5 : Types de coupure
- **Type** : Bar chart
- **Données** : Coupures par type (planifiée, imprévue, etc.)
- **Position** : Panneau en bas au centre
- **Comment capturer** : 
  1. Zoomer sur le panneau "Types de coupure"
  2. Windows + Shift + S pour capturer
  3. Enregistrer : `graphique_types_coupure.png`

#### Graphique 6 : Carte des zones touchées
- **Type** : Map (carte géographique)
- **Données** : Points géographiques des zones avec taille = nombre de coupures
- **Position** : Panneau en bas à droite (large)
- **Comment capturer** : 
  1. Zoomer sur le panneau "Carte des zones touchées"
  2. Windows + Shift + S pour capturer
  3. Enregistrer : `graphique_carte_zones.png`

---

## Graphiques supplémentaires possibles avec les données

### Données disponibles dans la base de données

Champs de la table `coupures` :
- **Temporelles** : date_debut, date_fin, duree_minutes, annee, mois, jour_semaine, periode_journee
- **Géographiques** : region, province, ville, zone, latitude, longitude
- **Catégorielles** : type_coupure, cause, statut, source_name, source_type
- **Métriques** : niveau_confiance, niveau_impact
- **Environnementales** : temperature_max, precipitation, irradiation_solaire

### Graphiques supplémentaires recommandés

#### 1. Durée moyenne par région
- **Type** : Bar chart
- **Données** : Durée moyenne des coupures par région
- **Intérêt** : Identifier les régions les plus touchées en durée
- **Fichier** : `graphique_duree_moyenne_region.png`

#### 2. Distribution des durées de coupures
- **Type** : Histogramme
- **Données** : Distribution de la durée des coupures (en minutes)
- **Intérêt** : Voir la concentration des durées (courte/moyenne/longue)
- **Fichier** : `graphique_distribution_durees.png`

#### 3. Coupures par jour de la semaine
- **Type** : Bar chart
- **Données** : Nombre de coupures par jour (Lundi, Mardi, etc.)
- **Intérêt** : Identifier les jours les plus critiques
- **Fichier** : `graphique_coupures_jour_semaine.png`

#### 4. Coupures par période de la journée
- **Type** : Bar chart
- **Données** : Coupures par période (matin, après-midi, soir, nuit)
- **Intérêt** : Identifier les heures de pointe des coupures
- **Fichier** : `graphique_coupures_periode_journee.png`

#### 5. Coupures par cause
- **Type** : Bar chart ou Pie chart
- **Données** : Répartition par cause (panne, maintenance, surcharge, etc.)
- **Intérêt** : Comprendre les raisons principales des coupures
- **Fichier** : `graphique_coupures_par_cause.png`

#### 6. Évolution annuelle des coupures
- **Type** : Line chart
- **Données** : Nombre de coupures par année
- **Intérêt** : Tendance sur plusieurs années
- **Fichier** : `graphique_evolution_annuelle.png`

#### 7. Top 10 des villes les plus touchées
- **Type** : Bar chart horizontal
- **Données** : 10 villes avec le plus de coupures
- **Intérêt** : Focus sur les zones urbaines critiques
- **Fichier** : `graphique_top10_villes.png`

#### 8. Heatmap des coupures par région et mois
- **Type** : Heatmap
- **Données** : Matrice région x mois
- **Intérêt** : Visualiser les patterns spatio-temporels
- **Fichier** : `graphique_heatmap_region_mois.png`

#### 9. Box plot des durées par type de coupure
- **Type** : Box plot
- **Données** : Distribution des durées par type
- **Intérêt** : Comparer la variabilité des durées selon le type
- **Fichier** : `graphique_boxplot_duree_type.png`

#### 10. Scatter plot : Durée vs Température
- **Type** : Scatter plot
- **Données** : Durée en fonction de la température max
- **Intérêt** : Corrélation entre température et durée des coupures
- **Fichier** : `graphique_scatter_duree_temperature.png`

---

## Procédure de capture des graphiques

### Méthode 1 : Capture depuis l'application web

1. **Lancer l'application**
   ```powershell
   .\lancer_projet.ps1
   ```

2. **Naviguer sur le dashboard**
   - Ouvrir : http://127.0.0.1:5000
   - Attendre que tous les graphiques se chargent

3. **Capturer chaque graphique**
   - Appuyer sur F11 (plein écran)
   - Utiliser Ctrl + Molette pour zoomer sur un graphique spécifique
   - Windows + Shift + S pour capturer
   - Enregistrer dans `docs/captures/` avec le nom approprié

### Méthode 2 : Capture avec Python (automatisée)

Si vous souhaitez automatiser les captures, voici un script Python avec Selenium :

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Configuration
options = Options()
options.add_argument("--headless")  # Sans interface graphique
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

# Créer le dossier de captures
os.makedirs("docs/captures", exist_ok=True)

# Ouvrir l'application
driver.get("http://127.0.0.1:5000")
time.sleep(3)  # Attendre le chargement

# Capturer le dashboard complet
driver.save_screenshot("docs/captures/graphique_dashboard_complet.png")

# Capturer chaque graphique individuellement
charts = [
    ("chart-region", "graphique_coupures_par_region.png"),
    ("chart-month", "graphique_coupures_par_mois.png"),
    ("chart-source", "graphique_repartition_source.png"),
    ("chart-status", "graphique_repartition_statut.png"),
    ("chart-type", "graphique_types_coupure.png"),
    ("chart-map", "graphique_carte_zones.png"),
]

for chart_id, filename in charts:
    element = driver.find_element(By.ID, chart_id)
    element.screenshot(f"docs/captures/{filename}")

driver.quit()
```

### Méthode 3 : Capture avec Plotly (export direct)

Les graphiques sont créés avec Plotly.js. Vous pouvez les exporter directement depuis le navigateur :
1. Clic droit sur un graphique
2. "Download plot as a png"
3. Enregistrer dans `docs/captures/`

---

## Organisation des captures de graphiques

### Structure recommandée

```
docs/captures/
├── graphiques_dashboard/
│   ├── 01_coupures_par_region.png
│   ├── 02_coupures_par_mois.png
│   ├── 03_repartition_source.png
│   ├── 04_repartition_statut.png
│   ├── 05_types_coupure.png
│   └── 06_carte_zones.png
├── graphiques_analyse/
│   ├── 07_duree_moyenne_region.png
│   ├── 08_distribution_durees.png
│   ├── 09_coupures_jour_semaine.png
│   └── ...
└── graphiques_ml/
    ├── modele_metrics.png
    ├── feature_importance.png
    └── confusion_matrix.png
```

---

## Intégration dans le rapport

### Légendes descriptives

Pour chaque graphique dans le rapport, ajoutez :
1. **Titre clair** : Exemple "Figure 1 : Répartition des coupures par région"
2. **Description** : Ce que montre le graphique
3. **Analyse** : Principales observations
4. **Source** : Données réelles (330 coupures)

### Exemple de légende

```
**Figure 1 : Répartition des coupures par région**

Ce graphique à barres présente la distribution des 330 coupures d'électricité
enregistrées par région administrative du Burkina Faso. La région du Centre
concentre le plus grand nombre de coupures avec XX occurrences, suivie de
la région du Hauts-Bassins avec XX coupures. Cette distribution reflète la
densité de population et l'activité économique dans ces zones urbaines.

*Source : Données réelles collectées (330 coupures)*
```

---

## Conseils pour des captures de qualité

1. **Résolution** : 1920x1080 minimum
2. **Format** : PNG (pas de compression)
3. **Zoom** : 100% (Ctrl + 0)
4. **Nettoyage** : Fermer les onglets inutiles
5. **Consistance** : Même navigateur et résolution pour toutes les captures
6. **Légende** : Ajouter une légende descriptive dans le rapport
