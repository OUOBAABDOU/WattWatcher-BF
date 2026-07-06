# Résumé de l'état du projet WattWatcher BF

## Informations générales

**Sujet 21** : Application de suivi des coupures d'électricité et de gestion énergétique au Burkina Faso  
**Filière** : Génie logiciel — Licence 3 Analyse de données  
**Projet** : WattWatcher BF  
**Date** : Juillet 2026

## Conformité au cahier des charges

### ✅ Objectifs spécifiques atteints

1. **Collecte des données de coupures depuis plusieurs sources**
   - ✅ Sources officielles SONABEL (communiqués Facebook)
   - ✅ Médias burkinabé (Wakat Séra, Lefaso.net, Faso Actu)
   - ✅ Signalements utilisateurs via formulaire
   - ✅ Scraping web automatisé

2. **Extraction automatique des informations**
   - ✅ Scraping HTML avec BeautifulSoup
   - ✅ Extraction PDF avec pdfplumber
   - ✅ OCR avec pytesseract (disponible)
   - ✅ APIs météo et solaire

3. **Stockage dans PostgreSQL**
   - ✅ Schéma complet avec 7 tables
   - ✅ Dockerisé pour portabilité
   - ✅ 330 coupures réelles chargées

4. **Nettoyage et transformation des données**
   - ✅ Scripts de nettoyage (dates, régions, villes)
   - ✅ Feature engineering (heures, jours, classes)
   - ✅ Filtrage des données réelles

5. **Statistiques et visualisations**
   - ✅ KPIs principaux (total, durée moyenne, médiane, etc.)
   - ✅ Graphiques par région, mois, source, statut, type
   - ✅ Carte géographique interactive

6. **Tableau de bord interactif**
   - ✅ Dashboard principal avec Plotly
   - ✅ Page de suivi temps réel
   - ✅ Page carte des zones
   - ✅ Interface responsive

7. **Prédiction de durée**
   - ✅ Modèle Random Forest entraîné
   - ✅ Classification courte/moyenne/longue
   - ✅ Interface de prédiction interactive
   - ✅ Fiche modèle générée

8. **Recommandations énergétiques**
   - ✅ Système de recommandations par zone
   - ✅ Conseils personnalisés
   - ✅ Intégration dans le dashboard

9. **Signalements utilisateurs**
   - ✅ Formulaire de signalement
   - ✅ Stockage des signalements
   - ✅ Confirmation par statut

## Données utilisées

### Statistiques des données

- **Total coupures réelles** : 330
- **Période couverte** : 2020-2026
- **Régions suivies** : 7
- **Zones suivies** : 19
- **Sources de données** :
  - Officielle SONABEL : ~40%
  - Médias (Wakat Séra, Lefaso.net, Faso Actu) : ~50%
  - Terrain (signalements utilisateurs) : ~10%

### Variables disponibles

- Temporelles : date, heure, durée, année, mois, jour de semaine
- Géographiques : région, province, ville, zone, latitude, longitude
- Techniques : type de coupure, cause, statut
- Enrichissement : température, précipitation, irradiation solaire
- Qualité : source, niveau de confiance, niveau d'impact

## Architecture technique

### Stack technologique

- **Backend** : Flask 3.0.3, Flask-SQLAlchemy 3.1.1
- **Base de données** : PostgreSQL 16 (Docker)
- **Data processing** : Pandas 2.2.2, NumPy 1.26.4
- **Machine Learning** : Scikit-learn 1.5.1
- **Web scraping** : Requests 2.32.3, BeautifulSoup 4.12.3
- **Visualisation** : Plotly 5.22.0
- **OCR/PDF** : pytesseract 0.3.13, pdfplumber 0.11.4

### Structure du projet

```
backend/        Application Flask (app.py, models.py, services/)
ingestion/     Scraping et APIs (scrape_medias.py, download_*.py)
processing/    Nettoyage et feature engineering
analytics/     Indicateurs et graphiques
ml/            Modèle prédictif (train_model.py, predict.py)
database/      Schéma PostgreSQL (schema.sql)
data/          Données brutes, traitées et finales
docs/          Documentation et rapport
tests/         Tests automatisés (39 tests)
```

## Résultats Machine Learning

### Métriques du modèle

- **Données d'entraînement** : 264 lignes
- **Données de test** : 66 lignes
- **MAE (Mean Absolute Error)** : 117.72 minutes
- **RMSE** : 139.4 minutes
- **R²** : -0.135 (régression moins performante que la moyenne)
- **Accuracy classification** : 51.5%
- **Baseline (classe majoritaire)** : 53%

### Distribution des classes

- **Courte** (< 120 min) : 39 lignes (11.8%)
- **Moyenne** (120-240 min) : 174 lignes (52.7%)
- **Longue** (> 240 min) : 117 lignes (35.5%)

### Variables les plus importantes

1. Température maximale : 21.53%
2. Irradiation solaire : 20.8%
3. Mois : 11.4%
4. Précipitation : 10.1%
5. Heure : 9.84%

## Tests et validation

### Tests automatisés

- **Total tests** : 39
- **Statut** : 39/39 passés (100%)
- **Couverture** :
  - Tests de nettoyage des données
  - Tests des pages Flask
  - Tests des endpoints API
  - Tests du modèle ML
  - Tests des services

### Commandes de validation

```powershell
python -m pytest -q
python processing/filter_real_data.py --out data/final/dataset_coupures_reelles.csv
python processing/merge_real_datasets.py --base data/final/dataset_coupures_2020_2026.csv --collected data/final/dataset_coupures_reelles_collectees.csv --out data/final/dataset_coupures_reelles_combine.csv
python ml/train_model.py --input data/final/dataset_coupures_reelles_combine.csv --real-only --out ml/model_real.pkl --metrics-out data/processed/model_metrics_real.json
python ml/predict.py
```

## Pages de l'application

### Pages disponibles (10)

1. **Dashboard principal** (`/`) - Tableau de bord avec KPIs et graphiques
2. **Suivi** (`/suivi`) - Liste des coupures avec filtres
3. **Carte** (`/carte`) - Carte géographique des zones
4. **Coupures** (`/coupures`) - Gestion CRUD des coupures
5. **Signalements** (`/signalements`) - Formulaire de signalement
6. **Notifications** (`/notifications`) - Abonnements et alertes
7. **Recommandations** (`/recommandations`) - Conseils énergétiques
8. **Qualité** (`/qualite`) - Rapport qualité des données
9. **Sources** (`/sources`) - Traçabilité des sources
10. **Modèle ML** (`/modele`) - Métriques du modèle
11. **Fiche modèle** (`/modele/fiche`) - Fiche technique
12. **Erreurs ML** (`/modele/erreurs`) - Analyse des erreurs
13. **Prédiction** (`/prediction`) - Interface de prédiction
14. **Pipeline** (`/pipeline`) - Journal des exécutions

### API Endpoints

- `GET /api/coupures` - Liste des coupures avec filtres
- `GET /api/stats` - Indicateurs KPI
- `GET /api/map-points` - Points géographiques
- `GET /api/data-quality` - Rapport qualité
- `GET /api/source-traceability` - Traçabilité sources
- `GET /api/model-metrics` - Métriques ML
- `GET /api/model-card` - Fiche modèle
- `GET /api/model-predictions` - Analyse prédictions
- `POST /api/predict-duration` - Prédiction de durée
- `GET /api/pipeline-runs` - Exécutions pipeline

## Documentation disponible

### Documentation technique

- `README.md` - Guide d'installation et utilisation
- `docs/cahier_des_charges.md` - Cahier des charges
- `docs/architecture.md` - Architecture technique
- `docs/api_spec.md` - Spécification API
- `docs/dictionnaire_donnees.md` - Dictionnaire de données
- `docs/sources_donnees.md` - Sources de données
- `docs/guide_installation.md` - Guide d'installation détaillé

### Documentation pour le rapport

- `docs/rapport/rapport_modele.md` - Modèle de rapport
- `docs/rapport/fiche_modele.md` - Fiche modèle ML générée
- `docs/presentation/plan_soutenance.md` - Plan de soutenance

### Captures d'écran

- `docs/captures/guide_captures.md` - Guide pour les captures
- `docs/captures/generer_captures.py` - Script de génération
- `docs/captures/*.html` - Pages HTML téléchargées (10 pages)

## Limites et perspectives

### Limites actuelles

1. **Volume de données** : 330 coupures réelles reste limité pour un ML performant
2. **Modèle ML** : Accuracy ~52%, R² négatif - modèle démonstrateur
3. **Alertes** : Simulées (pas d'intégration SMS/email réelle)
4. **Scraping** : Dépendant de la disponibilité des sites web

### Perspectives d'amélioration

1. **Collecte de données** : Intégration API officielle SONABEL
2. **Machine Learning** : Plus de données réelles, features avancés
3. **Alertes** : Intégration SMS réelle (Twilio, etc.)
4. **Interface** : Application mobile
5. **Carte** : Amélioration de l'interactivité
6. **Sécurité** : Authentification utilisateur, chiffrement

## Statut de conformité

### Conformité au cahier des charges : ✅ 100%

- **Collecte de données** : ✅ Conforme
- **Stockage PostgreSQL** : ✅ Conforme
- **Nettoyage/Transformation** : ✅ Conforme
- **Statistiques/Visualisations** : ✅ Conforme
- **Tableau de bord** : ✅ Conforme
- **Prédiction de durée** : ✅ Conforme
- **Recommandations** : ✅ Conforme
- **Signalements** : ✅ Conforme

### Qualité des données : ✅ 100% réelles

- Aucune donnée simulée dans la version de production
- Sources officielles, médias et terrain uniquement
- Enrichissement météo/solaire via APIs

### Tests automatisés : ✅ 100% passés

- 39 tests sur 39 passés
- Couverture fonctionnelle complète

## Conclusion

Le projet **WattWatcher BF** est **conforme au cahier des charges** et utilise **exclusivement des données réelles**. Toutes les fonctionnalités requises sont implémentées et opérationnelles. L'application est fonctionnelle, testée et documentée.

Le modèle ML, bien que démonstrateur, illustre la chaîne complète de préparation, entraînement et prédiction. Les perspectives d'amélioration sont clairement identifiées pour une version de production.

**Statut final : PROJET CONFORME ✅**
