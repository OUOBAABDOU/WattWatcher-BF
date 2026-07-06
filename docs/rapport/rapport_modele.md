# Rapport de projet tutoré — WattWatcher BF

## Page de garde

**Sujet 21 :** Application de suivi des coupures d’électricité et de gestion énergétique  
**Filière :** Génie logiciel — Licence 3 Analyse de données  
**Projet :** WattWatcher BF

## Résumé

WattWatcher BF est une application web Flask qui centralise les informations sur les coupures d’électricité au Burkina Faso, les stocke dans PostgreSQL, les analyse avec Pandas/Scikit-learn et les présente dans un tableau de bord. Le système propose aussi un suivi par région, des signalements communautaires, des alertes simulées et des recommandations énergétiques.

## 1. Introduction

### Contexte
Les coupures d’électricité perturbent les ménages, entreprises, commerces et services publics. Les informations existent souvent sous forme de communiqués, d’articles ou de signalements dispersés.

### Problématique
Comment collecter, structurer et analyser les informations de coupures afin d’aider les utilisateurs à mieux anticiper et gérer leur consommation énergétique ?

### Objectifs
- Collecter les données de coupures depuis des sources web, CSV et signalements.
- Stocker les informations dans PostgreSQL.
- Produire des indicateurs et visualisations par région, zone et période.
- Suivre les coupures prévues, en cours et terminées.
- Générer des alertes simulées pour les zones suivies.
- Proposer des recommandations énergétiques adaptées aux données.

## 2. Analyse des besoins

Les utilisateurs cibles sont les ménages, commerces, PME, étudiants et services qui veulent planifier leurs activités lors des coupures. Ils ont besoin de connaître les zones touchées, les horaires, la fréquence des coupures et les solutions alternatives possibles.

## 3. Description des données

Le projet utilise exclusivement des données réelles dans sa version de production. Le dataset principal contient 330 coupures réelles collectées depuis plusieurs sources :
- Sources officielles SONABEL (communiqués Facebook)
- Médias burkinabé (Wakat Séra, Lefaso.net, Faso Actu)
- Signalements utilisateurs (terrain)
- Articles web collectés automatiquement via scraping

Les données sont enrichies avec des variables météorologiques (température, précipitation) et solaires (irradiation) provenant des APIs Open-Meteo et NASA POWER. Le dataset exclut toutes les données simulées et ne conserve que les sources réelles : officielle, média et terrain.

Les champs principaux sont : date, heure, durée, région, ville, zone, type de coupure, cause, source, niveau de confiance, température, précipitation et irradiation solaire.

## 4. Préparation et exploration des données

Le script `processing/clean_coupures.py` nettoie les dates, heures, régions, villes et zones. `processing/feature_engineering.py` ajoute les variables d’heure, jour, weekend, classe de durée et risque par zone. `analytics/generate_indicators.py` produit les indicateurs JSON et `analytics/eda.py` génère les graphiques HTML.

## 5. Conception et modélisation

L’architecture suit le flux : sources web/CSV/signalements → ingestion → nettoyage → PostgreSQL → Flask/API → dashboard, recommandations et modèle ML. La base contient les tables `coupures`, `signalements`, `abonnements`, `notifications`, `source_documents` et `recommandations`.

## 6. Implémentation

- Backend : Flask et Flask-SQLAlchemy.
- Base de données : PostgreSQL via Docker.
- Collecte : Requests, BeautifulSoup, pdfplumber/OCR prévus.
- Analyse : Pandas, Plotly.
- Modèle : Scikit-learn avec régression de durée et classification courte/moyenne/longue.
- Alertes : abonnements par région, ville ou zone, notifications simulées web/email/SMS/WhatsApp.

## 7. Résultats

Indicateurs obtenus sur les données réelles combinées : 330 coupures, durée moyenne d’environ 226 minutes, 7 régions suivies et 19 zones suivies. Le modèle entraîné sur ces données obtient une précision de classification d’environ 52 % sur les classes courte, moyenne et longue. La matrice de confusion montre que le modèle prédit surtout la classe moyenne : `[[0, 2, 6], [0, 5, 18], [0, 6, 29]]` pour les classes courte, longue et moyenne. La baseline “classe majoritaire” obtient environ 53 %, ce qui montre que le modèle ML actuel sert surtout de démonstrateur et doit être amélioré avec davantage de données réelles. Un essai avec `class_weight=balanced` baisse aussi l’accuracy à environ 52 %, même s’il améliore légèrement la détection des coupures longues. La régression reste moins fiable avec un R2 négatif et fait moins bien que la prédiction moyenne simple.

## 8. Tests et validation

Les tests automatisés vérifient le nettoyage des données, les pages Flask, les endpoints API, la page de suivi, les recommandations et le mécanisme d’abonnement/notification. Les commandes de validation utilisées sont :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe processing\filter_real_data.py --out data\final\dataset_coupures_reelles.csv
.\.venv\Scripts\python.exe processing\merge_real_datasets.py --base data\final\dataset_coupures_2020_2026.csv --collected data\final\dataset_coupures_reelles_collectees.csv --out data\final\dataset_coupures_reelles_combine.csv
.\.venv\Scripts\python.exe processing\clean_coupures.py --input data\final\dataset_coupures_2020_2026.csv --out data\processed\coupures_clean.csv
.\.venv\Scripts\python.exe ml\train_model.py --input data\final\dataset_coupures_reelles_combine.csv --real-only --out ml\model_real.pkl --metrics-out data\processed\model_metrics_real.json
.\.venv\Scripts\python.exe ml\predict.py
```

## 9. Sécurité et protection des données

Les données personnelles sont limitées aux contacts d’abonnement et signalements. Pour une version de production, il faudra ajouter authentification, chiffrement des secrets, consentement utilisateur, suppression des abonnements et protection contre les injections/formulaires abusifs.

## 10. Limites

Le volume de données réelles reste limité (330 coupures), ce qui affecte les performances du modèle ML. Les alertes sont simulées dans cette version. Le scraping dépend de la disponibilité des sites web. Les métriques comparées aux baselines montrent que le modèle prédictif ne doit pas être présenté comme performant en production ; il démontre surtout la chaîne complète de préparation, entraînement, sauvegarde et prédiction.

## 11. Conclusion et perspectives

Le projet répond au sujet 21 en proposant une application fonctionnelle de suivi, analyse, stockage, alertes et recommandations énergétiques. Les perspectives principales sont : intégration SMS réelle, carte interactive, collecte officielle SONABEL plus robuste, application mobile et amélioration du modèle prédictif.
