# Rapport de projet tutoré — WattWatcher BF

## Page de garde

**Sujet 21 :** Application de suivi des coupures d'électricité et de gestion énergétique  
**Filière :** Génie logiciel — Licence 3 Analyse de données  
**Projet :** WattWatcher BF  
**Date :** Juillet 2026

---

## Résumé

WattWatcher BF est une application web Flask qui centralise les informations sur les coupures d'électricité au Burkina Faso, les stocke dans PostgreSQL, les analyse avec Pandas/Scikit-learn et les présente dans un tableau de bord interactif. Le système propose un suivi par région, des signalements communautaires, des alertes simulées et des recommandations énergétiques. Le projet utilise exclusivement des données réelles collectées depuis les sources officielles SONABEL, les médias burkinabé et les signalements utilisateurs.

---

## 1. Introduction

### 1.1 Contexte

Les coupures d'électricité perturbent les activités des ménages, entreprises, commerces et services publics au Burkina Faso. Les informations existent souvent sous forme de communiqués officiels, d'articles de presse ou de signalements dispersés, rendant difficile leur exploitation pour une planification énergétique efficace.

### 1.2 Problématique

Comment collecter, structurer et analyser les informations de coupures d'électricité afin d'aider les utilisateurs à mieux anticiper et gérer leur consommation énergétique ?

### 1.3 Objectifs

- Collecter les données de coupures depuis des sources web, CSV et signalements
- Stocker les informations dans PostgreSQL
- Produire des indicateurs et visualisations par région, zone et période
- Suivre les coupures prévues, en cours et terminées
- Générer des alertes simulées pour les zones suivies
- Proposer des recommandations énergétiques adaptées aux données
- Développer un modèle de prédiction de durée des coupures

---

## 2. Analyse des besoins

### 2.1 Utilisateurs cibles

Les utilisateurs cibles sont les ménages, commerces, PME, étudiants et services publics qui souhaitent planifier leurs activités lors des coupures. Ils ont besoin de connaître les zones touchées, les horaires, la fréquence des coupures et les solutions alternatives possibles.

### 2.2 Besoins fonctionnels

- Consultation des coupures par région, ville et zone
- Suivi en temps réel des coupures actives
- Visualisation des tendances et statistiques
- Réception d'alertes pour les zones suivies
- Accès à des recommandations énergétiques personnalisées
- Possibilité de signaler une coupure

### 2.3 Besoins non fonctionnels

- Performance : Temps de réponse < 2 secondes
- Disponibilité : Application accessible 24/7
- Sécurité : Protection des données personnelles
- Scalabilité : Capacité à gérer un volume croissant de données

---

## 3. Description des données

### 3.1 Sources de données

Le projet utilise exclusivement des données réelles dans sa version de production. Le dataset principal contient **330 coupures réelles** collectées depuis plusieurs sources :

- **Sources officielles SONABEL** (communiqués Facebook) : ~40%
- **Médias burkinabé** (Wakat Séra, Lefaso.net, Faso Actu) : ~50%
- **Signalements utilisateurs** (terrain) : ~10%

### 3.2 Enrichissement des données

Les données sont enrichies avec des variables météorologiques et solaires provenant d'APIs externes :
- **Open-Meteo Historical Weather API** : Température maximale et précipitations
- **NASA POWER Daily API** : Irradiation solaire
- **Banque mondiale** : Indicateur d'accès à l'électricité

### 3.3 Variables disponibles

| Catégorie | Variables |
|-----------|-----------|
| Temporelles | date, heure, durée, année, mois, jour de semaine |
| Géographiques | région, province, ville, zone, latitude, longitude |
| Techniques | type de coupure, cause, statut |
| Enrichissement | température, précipitation, irradiation solaire |
| Qualité | source, niveau de confiance, niveau d'impact |

### 3.4 Statistiques des données

- **Total coupures réelles** : 330
- **Période couverte** : 2020-2026
- **Régions suivies** : 7 (Centre, Hauts-Bassins, Nord, Est, Sud-Ouest, Centre-Ouest, Boucle du Mouhoun)
- **Zones suivies** : 19
- **Durée moyenne** : 226 minutes
- **Durée médiane** : 240 minutes

---

## 4. Préparation et exploration des données

### 4.1 Nettoyage des données

Le script `processing/clean_coupures.py` effectue les opérations suivantes :
- Normalisation des dates et heures
- Standardisation des noms de régions, villes et zones
- Calcul des durées en minutes
- Gestion des valeurs manquantes

### 4.2 Feature engineering

Le script `processing/feature_engineering.py` ajoute des variables dérivées :
- Variables temporelles : heure_num, jour_num, weekend
- Classe de durée : courte (< 120 min), moyenne (120-240 min), longue (> 240 min)
- Risque par zone basé sur la fréquence des coupures

### 4.3 Filtrage des données réelles

Le script `processing/filter_real_data.py` exclut les données simulées et ne conserve que les sources réelles (officielle, média, terrain).

### 4.4 Indicateurs et visualisations

- `analytics/generate_indicators.py` : Produit les indicateurs JSON
- `analytics/eda.py` : Génère les graphiques HTML avec Plotly

---

## 5. Conception et modélisation

### 5.1 Architecture technique

L'architecture suit le flux suivant :

```
Sources web/CSV/signalements → Ingestion → Nettoyage → PostgreSQL → Flask/API → Dashboard, Recommandations, Modèle ML
```

### 5.2 Schéma de base de données

La base de données PostgreSQL contient 7 tables :

1. **coupures** : Stockage des coupures d'électricité
2. **signalements** : Signalements utilisateurs
3. **abonnements** : Abonnements aux alertes
4. **notifications** : Historique des notifications
5. **source_documents** : Traçabilité des sources
6. **recommandations** : Recommandations énergétiques
7. **pipeline_runs** : Journal des exécutions du pipeline

### 5.3 API REST

L'application expose 10 endpoints API pour l'accès aux données et aux fonctionnalités ML.

---

## 6. Implémentation

### 6.1 Stack technologique

- **Backend** : Flask 3.0.3, Flask-SQLAlchemy 3.1.1
- **Base de données** : PostgreSQL 16 (Docker)
- **Data processing** : Pandas 2.2.2, NumPy 1.26.4
- **Machine Learning** : Scikit-learn 1.5.1
- **Web scraping** : Requests 2.32.3, BeautifulSoup 4.12.3
- **Visualisation** : Plotly 5.22.0
- **OCR/PDF** : pytesseract 0.3.13, pdfplumber 0.11.4

### 6.2 Structure du projet

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

### 6.3 Fonctionnalités implémentées

#### 6.3.1 Collecte de données
- Scraping web automatisé des médias burkinabé
- Téléchargement des données météo et solaires via APIs
- Formulaire de signalement utilisateur
- Extraction PDF et OCR (disponible)

#### 6.3.2 Tableau de bord
- Dashboard principal avec KPIs et graphiques
- Suivi temps réel par région et zone
- Carte géographique interactive des zones touchées
- Page de qualité des données
- Page de traçabilité des sources

#### 6.3.3 Machine Learning
- Modèle Random Forest pour la prédiction de durée
- Classification des coupures (courte/moyenne/longue)
- Interface de prédiction interactive
- Fiche modèle générée automatiquement
- Analyse des erreurs de prédiction

#### 6.3.4 Alertes et recommandations
- Système d'abonnements par région, ville ou zone
- Génération de notifications simulées
- Recommandations énergétiques personnalisées

### 6.3.5 Scripts et architecture technique

Le projet comprend plusieurs scripts clés qui illustrent l'implémentation technique :

- **backend/app.py** : Application Flask principale avec routes et connexion à PostgreSQL
- **ingestion/scrape_medias.py** : Script de scraping web pour collecter les données des médias
- **processing/clean_coupures.py** : Script de nettoyage et normalisation des données
- **ml/train_model.py** : Script d'entraînement du modèle Random Forest
- **database/schema.sql** : Schéma de base de données avec 7 tables

Ces scripts démontrent la chaîne complète de traitement des données : collecte → nettoyage → stockage → analyse → prédiction.

---

## 7. Résultats

### 7.1 Indicateurs obtenus

Sur les données réelles combinées (330 coupures) :
- Durée moyenne : 226 minutes
- Durée médiane : 240 minutes
- 7 régions suivies
- 19 zones suivies
- Sources principalement officielles et médias

### 7.2 Résultats Machine Learning

#### Métriques du modèle

- **Données d'entraînement** : 264 lignes
- **Données de test** : 66 lignes
- **MAE (Mean Absolute Error)** : 117.72 minutes
- **RMSE** : 139.4 minutes
- **R²** : -0.135 (régression moins performante que la moyenne)
- **Accuracy classification** : 51.5%
- **Baseline (classe majoritaire)** : 53%

#### Distribution des classes

- **Courte** (< 120 min) : 39 lignes (11.8%)
- **Moyenne** (120-240 min) : 174 lignes (52.7%)
- **Longue** (> 240 min) : 117 lignes (35.5%)

#### Variables les plus importantes

1. Température maximale : 21.53%
2. Irradiation solaire : 20.8%
3. Mois : 11.4%
4. Précipitation : 10.1%
5. Heure : 9.84%

### 7.3 Analyse des résultats

Le modèle ML actuel sert principalement de démonstrateur technique. L'accuracy de classification (51.5%) est légèrement inférieure à la baseline (53%), ce qui indique que le volume de données réelles reste limité pour un apprentissage robuste. La régression avec un R² négatif montre que le modèle fait moins bien que la prédiction moyenne simple.

Cependant, le projet démontre la chaîne complète de préparation, entraînement, sauvegarde et prédiction, ce qui constitue une base solide pour des améliorations futures avec plus de données.

---

## 8. Tests et validation

### 8.1 Tests automatisés

Les tests automatisés vérifient :
- Le nettoyage des données
- Les pages Flask
- Les endpoints API
- La page de suivi
- Les recommandations
- Le mécanisme d'abonnement/notification
- Le modèle ML

### 8.2 Résultats des tests

- **Total tests** : 39
- **Statut** : 39/39 passés (100%)
- **Couverture** : Fonctionnelle complète

### 8.3 Commandes de validation

```powershell
python -m pytest -q
python processing/filter_real_data.py --out data/final/dataset_coupures_reelles.csv
python processing/merge_real_datasets.py --base data/final/dataset_coupures_2020_2026.csv --collected data/final/dataset_coupures_reelles_collectees.csv --out data/final/dataset_coupures_reelles_combine.csv
python processing/clean_coupures.py --input data/final/dataset_coupures_2020_2026.csv --out data/processed/coupures_clean.csv
python ml/train_model.py --input data/final/dataset_coupures_reelles_combine.csv --real-only --out ml/model_real.pkl --metrics-out data/processed/model_metrics_real.json
python ml/predict.py
```

---

## 9. Sécurité et protection des données

### 9.1 Données personnelles

Les données personnelles sont limitées aux contacts d'abonnement et signalements (nom, téléphone, email).

### 9.2 Mesures de sécurité actuelles

- Variables d'environnement pour les secrets
- Chiffrement des mots de passe en base de données
- Validation des entrées utilisateur

### 9.3 Améliorations pour la production

Pour une version de production, il faudra ajouter :
- Authentification utilisateur
- Chiffrement des secrets
- Consentement utilisateur explicite
- Possibilité de suppression des abonnements
- Protection contre les injections et formulaires abusifs
- HTTPS obligatoire

---

## 10. Limites

### 10.1 Volume de données

Le volume de données réelles reste limité (330 coupures), ce qui affecte les performances du modèle ML. Plus de données réelles sont nécessaires pour améliorer la précision des prédictions.

### 10.2 Alertes

Les alertes email/SMS/WhatsApp sont simulées dans cette version. Une intégration avec un fournisseur réel (Twilio, etc.) serait nécessaire pour la production.

### 10.3 Scraping

Le scraping dépend de la disponibilité des sites web et de la stabilité de leur structure HTML. Des modifications du site peuvent casser le scraping.

### 10.4 Modèle prédictif

Les métriques comparées aux baselines montrent que le modèle prédictif ne doit pas être présenté comme performant en production ; il démontre surtout la chaîne complète de préparation, entraînement, sauvegarde et prédiction.

---

## 11. Conclusion et perspectives

### 11.1 Conclusion

Le projet WattWatcher BF répond au sujet 21 en proposant une application fonctionnelle de suivi, analyse, stockage, alertes et recommandations énergétiques. Toutes les fonctionnalités requises par le cahier des charges ont été implémentées et testées avec succès. Le projet utilise exclusivement des données réelles collectées depuis des sources officielles et médiatiques.

### 11.2 Perspectives principales

- **Intégration SMS réelle** : Branchement sur un fournisseur de SMS pour des alertes opérationnelles
- **Collecte officielle SONABEL** : Intégration API officielle si disponible pour des données plus robustes
- **Application mobile** : Développement d'une application mobile pour une meilleure accessibilité
- **Amélioration du modèle prédictif** : Collecte de plus de données réelles et features avancés
- **Carte interactive avancée** : Amélioration de l'interactivité et des filtres géographiques
- **Sécurité renforcée** : Implémentation complète de l'authentification et du chiffrement

### 11.3 Conformité

**Conformité au cahier des charges** : ✅ 100%  
**Qualité des données** : ✅ 100% réelles  
**Tests automatisés** : ✅ 39/39 passés  
**Application** : ✅ Fonctionnelle

---

## Annexes

### Annexe A : Structure du projet

[Structure détaillée du projet avec description des répertoires]

### Annexe B : Spécification API

[Liste complète des endpoints API avec paramètres et réponses]

### Annexe C : Dictionnaire de données

[Description complète des tables et champs de la base de données]

### Annexe D : Fiche modèle ML

[Fiche technique détaillée du modèle de machine learning]

### Annexe E : Captures d'écran

### Section 1 - Pages principales (10 captures)

1. **Tableau de bord des coupures d'électricité** - KPIs et graphiques interactifs
2. **Coupures par région** - Liste des coupures avec filtres
3. **Carte des zones touchées** - Visualisation géographique
4. **Gestion des coupures** - Interface CRUD
5. **Répartition par source** - Formulaire et liste
6. **Répartition par statut** - Système d'alertes
7. **Recommandations énergétiques** - Conseils énergétiques
8. **Qualité des données** - Rapport qualité
9. **Traçabilité des sources** - Traçabilité
10. **Zones cartographiées** - Journal d'exécution

### Section 2 - Machine Learning (5 captures)

11. **Modèle prédictif ML** - Métriques d'entraînement
12. **Fiche modèle** - Documentation technique
13. **Erreurs ML** - Analyse des erreurs
14. **Prédiction de durée (avant)** - Interface vide
15. **Prédiction de durée (après)** - Exemple de prédiction

### Section 3 - Détails et démonstration (5 captures)

16. **Navigation** - Menu et structure
17. **Dashboard KPIs** - Zoom sur indicateurs
18. **Dashboard graphiques** - Zoom sur visualisations
19. **Coupures actives** - Section actives
20. **Vue d'ensemble** - Interface complète

### Section 4 - Scripts et code (5 captures)

21. **backend/app.py** - Application Flask principale
22. **ingestion/scrape_medias.py** - Script de scraping
23. **processing/clean_coupures.py** - Script de nettoyage
24. **ml/train_model.py** - Script d'entraînement ML
25. **database/schema.sql** - Schéma de base de données

**Note** : Les captures d'écran sont disponibles dans le dossier `docs/captures/` et illustrent toutes les fonctionnalités du projet avec des données réelles (330 coupures).

---

**Fin du rapport**
