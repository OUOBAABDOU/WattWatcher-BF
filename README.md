# WattWatcher BF

Application web de suivi des coupures d'électricité et de gestion énergétique au Burkina Faso.

**Sujet 21** : Application de suivi des coupures d'électricité et de gestion énergétique  
**Filière** : Génie logiciel — Licence 3 Analyse de données  
**Date** : Juillet 2026

---

## 📋 Description

WattWatcher BF est une application web Flask qui centralise les informations sur les coupures d'électricité au Burkina Faso, les stocke dans PostgreSQL, les analyse avec Pandas/Scikit-learn et les présente dans un tableau de bord interactif. Le système propose un suivi par région, des signalements communautaires, des alertes simulées et des recommandations énergétiques.

### Caractéristiques principales

- ✅ **Collecte multi-sources** : Scraping web, APIs météo/solaire, signalements utilisateurs
- ✅ **Données 100% réelles** : 330 coupures réelles collectées depuis SONABEL et médias burkinabé
- ✅ **Tableau de bord interactif** : KPIs, graphiques, carte géographique
- ✅ **Machine Learning** : Modèle Random Forest pour prédiction de durée
- ✅ **Alertes et recommandations** : Système d'abonnements et conseils énergétiques
- ✅ **Tests automatisés** : 39/39 tests passés (100%)

---

## 🚀 Installation rapide

### Pré-requis

- Python 3.10 ou 3.11
- Docker et Docker Compose
- Git
- Tesseract OCR (optionnel pour OCR)

### Étapes d'installation

```powershell
# Cloner le dépôt
git clone https://github.com/OUOBAABDOU/WattWatcher-BF.git
cd WattWatcher-BF

# Créer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
copy .env.example .env
# Éditez .env si nécessaire

# Démarrer PostgreSQL avec Docker
docker compose up -d
```

### Charger les données réelles

```powershell
# Charger uniquement les données réelles disponibles
.\.venv\Scripts\python.exe ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures
```

### Lancer l'application

```powershell
.\.venv\Scripts\python.exe backend\app.py
```

Ouvrez votre navigateur sur : **http://127.0.0.1:5000**

---

## 🔒 Accès HTTPS (Docker + Nginx)

Après avoir configuré les services Docker avec Nginx, ouvre ton navigateur sur : **https://localhost** ou **https://127.0.0.1**

> Le certificat est auto-signé, donc le navigateur affichera un avertissement de sécurité. Accepte le certificat pour continuer.

### Dépannage certificat

- Si le navigateur dit « connexion non privée » ou « certificat invalide », choisis l’option pour continuer malgré l’avertissement.
- Sur Chrome/Edge : clique sur « Avancé », puis « Continuer vers localhost (non sécurisé) ».
- Sur Firefox : clique sur « Avancé », puis « Ajouter une exception… », et confirme.
- Si la page ne s’affiche toujours pas, redémarre les conteneurs Docker :

```powershell
docker compose down
Docker compose up --build
```

- Vérifie que le service `nginx` est bien démarré :

```powershell
docker compose ps
```

---

## 📊 Données

### Sources de données

Le projet utilise exclusivement des données réelles :

- **Sources officielles SONABEL** (communiqués Facebook) : ~40%
- **Médias burkinabé** (Wakat Séra, Lefaso.net, Faso Actu) : ~50%
- **Signalements utilisateurs** (terrain) : ~10%

### Statistiques

- **Total coupures réelles** : 330
- **Période couverte** : 2020-2026
- **Régions suivies** : 7
- **Zones suivies** : 19
- **Durée moyenne** : 226 minutes
- **Durée médiane** : 240 minutes

### Enrichissement des données

- **Open-Meteo Historical Weather API** : Température et précipitations
- **NASA POWER Daily API** : Irradiation solaire
- **Banque mondiale** : Contexte énergétique national

---

## 🏗️ Architecture

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

### Flux de données

```
Sources web/CSV/signalements → Ingestion → Nettoyage → PostgreSQL → Flask/API → Dashboard, Recommandations, Modèle ML
```

---

## 🎯 Fonctionnalités

### Pages de l'application

1. **Dashboard principal** (`/`) - KPIs et graphiques interactifs
2. **Suivi des coupures** (`/suivi`) - Liste des coupures avec filtres
3. **Carte des zones** (`/carte`) - Visualisation géographique
4. **Liste des coupures** (`/coupures`) - Interface CRUD
5. **Signalements** (`/signalements`) - Formulaire de signalement
6. **Notifications** (`/notifications`) - Système d'alertes
7. **Recommandations** (`/recommandations`) - Conseils énergétiques
8. **Qualité des données** (`/qualite`) - Rapport qualité
9. **Sources** (`/sources`) - Traçabilité des sources
10. **Pipeline** (`/pipeline`) - Journal d'exécution
11. **Modèle ML** (`/modele`) - Métriques du modèle
12. **Fiche modèle** (`/modele/fiche`) - Documentation technique
13. **Erreurs ML** (`/modele/erreurs`) - Analyse des erreurs
14. **Prédiction** (`/prediction`) - Interface de prédiction

### Machine Learning

- **Algorithme** : Random Forest Regressor
- **Tâches** : Régression de durée + Classification (courte/moyenne/longue)
- **Métriques** : MAE 117.72 min, RMSE 139.4 min, Accuracy 51.5%
- **Variables importantes** : Température (21.5%), Irradiation solaire (20.8%), Mois (11.4%)

---

## 🧪 Tests

### Exécuter les tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

### Résultats

- **Total tests** : 39
- **Statut** : 39/39 passés (100%)
- **Couverture** : Fonctionnelle complète

### Commandes de validation

```powershell
python -m pytest -q
python processing/filter_real_data.py --out data/final/dataset_coupures_reelles.csv
python processing/merge_real_datasets.py --base data/final/dataset_coupures_2020_2026.csv --collected data/final/dataset_coupures_reelles_collectees.csv --out data/final/dataset_coupures_reelles_combine.csv
python processing/clean_coupures.py --input data/final/dataset_coupures_2020_2026.csv --out data/processed/coupures_clean.csv
python ml/train_model.py --input data/final/dataset_coupures_reelles_combine.csv --real-only --out ml/model_real.pkl --metrics-out data/processed/model_metrics_real.json
python ml/predict.py
```

---

## 📚 Documentation

### Documentation technique

- `docs/cahier_des_charges.md` - Cahier des charges
- `docs/architecture.md` - Architecture technique
- `docs/api_spec.md` - Spécification API
- `docs/dictionnaire_donnees.md` - Dictionnaire de données
- `docs/sources_donnees.md` - Sources de données
- `docs/guide_installation.md` - Guide d'installation détaillé

### Documentation pour le rapport

- `docs/rapport/rapport_final.md` - Rapport complet
- `docs/rapport/resume_projet.md` - Résumé détaillé du projet
- `docs/rapport/fiche_modele.md` - Fiche modèle ML

### Présentation

- `docs/presentation/support_soutenance.md` - Support de soutenance
- `docs/presentation/plan_soutenance.md` - Plan de soutenance

### Captures d'écran

- `docs/captures/instructions_captures.md` - Instructions pour les captures
- `docs/captures/guide_captures.md` - Guide de référence

---

## 🔧 Scripts clés

### Scripts d'ingestion

- `ingestion/scrape_medias.py` - Scraping web des médias
- `ingestion/download_openmeteo.py` - Téléchargement données météo
- `ingestion/download_nasa_power.py` - Téléchargement données solaires
- `ingestion/download_worldbank.py` - Téléchargement données Banque mondiale
- `ingestion/load_to_postgres.py` - Chargement dans PostgreSQL

### Scripts de traitement

- `processing/clean_coupures.py` - Nettoyage des données
- `processing/feature_engineering.py` - Feature engineering
- `processing/filter_real_data.py` - Filtrage des données réelles
- `processing/merge_real_datasets.py` - Fusion des datasets

### Scripts ML

- `ml/train_model.py` - Entraînement du modèle
- `ml/predict.py` - Prédiction

---

## 🌐 API Endpoints

L'application expose les endpoints suivants :

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

---

## ⚙️ Configuration

### Variables d'environnement

```env
FLASK_ENV=development
SECRET_KEY=votre_secret_key_ici
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/wattwatcher_db
APP_TIMEZONE=Africa/Ouagadougou
```

### Base de données

Le projet utilise PostgreSQL via Docker sur le port hôte `5433` pour éviter les conflits avec un PostgreSQL local.

---

## 📈 Résultats

### Conformité

- **Conformité au cahier des charges** : ✅ 100%
- **Qualité des données** : ✅ 100% réelles
- **Tests automatisés** : ✅ 39/39 passés
- **Application** : ✅ Fonctionnelle

### Limites

- Volume de données réelles limité (330 coupures)
- Modèle ML démonstrateur (accuracy ~52%)
- Alertes simulées (pas d'intégration SMS réelle)
- Scraping dépendant de la disponibilité des sites

---

## 🔮 Perspectives

- Intégration SMS réelle pour les alertes
- Collecte officielle SONABEL via API
- Application mobile
- Amélioration du modèle ML avec plus de données
- Carte interactive avancée
- Sécurité renforcée (authentification, chiffrement)

---

## 👥 Auteurs

**Nom** : OUOBA Abdou Rasmané
**Téléphone** : +226 54516665  
**WhatsApp** : +226 54516665  
**Email** : aouoba9@gmail.com  

Projet réalisé dans le cadre du Sujet 21 - Filière Génie logiciel — Licence 3 Analyse de données.

---

## 📄 Licence

Ce projet est à usage académique.

---

## 🤝 Contribution

Ce projet est un projet académique. Pour toute question ou suggestion, veuillez contacter l'auteur.

---

**Dépôt GitHub** : https://github.com/OUOBAABDOU/WattWatcher-BF
