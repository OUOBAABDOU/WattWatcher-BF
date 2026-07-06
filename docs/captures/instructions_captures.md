# Instructions détaillées pour les captures d'écran

## Pré-requis

✅ Application Flask démarrée sur http://127.0.0.1:5000  
✅ PostgreSQL connecté avec 330 coupures réelles  
✅ Navigateur web (Chrome, Firefox, Edge)

## Procédure pas à pas

### 1. Ouvrir l'application

1. Ouvrez votre navigateur web
2. Naviguez vers : http://127.0.0.1:5000
3. Vérifiez que le dashboard s'affiche correctement

### 2. Capturer chaque page

Utilisez **Windows + Shift + S** pour ouvrir l'outil de capture d'écran Windows

---

## SECTION 1 : Pages principales (10 captures)

#### Capture 01 : Dashboard principal
- **URL** : http://127.0.0.1:5000
- **Nom du fichier** : `01_dashboard_principal.png`
- **Ce qu'il faut montrer** :
  - Les 7 cartes KPI en haut (Total coupures, Durée moyenne, etc.)
  - Les graphiques par région, mois, source, statut, type
  - La carte géographique en bas
- **Conseil** : Capturez en mode plein écran (F11) pour une meilleure qualité

#### Capture 02 : Suivi des coupures
- **URL** : http://127.0.0.1:5000/suivi
- **Nom du fichier** : `02_suivi_coupures.png`
- **Ce qu'il faut montrer** :
  - Le tableau des coupures récentes
  - La section "Coupures actives" en haut
  - Les filtres si disponibles

#### Capture 03 : Carte des zones
- **URL** : http://127.0.0.1:5000/carte
- **Nom du fichier** : `03_carte_zones.png`
- **Ce qu'il faut montrer** :
  - La carte interactive centrée sur le Burkina Faso
  - Les points représentant les zones
  - Le tableau des zones cartographiées en dessous

#### Capture 04 : Liste des coupures (CRUD)
- **URL** : http://127.0.0.1:5000/coupures
- **Nom du fichier** : `04_liste_coupures.png`
- **Ce qu'il faut montrer** :
  - La liste complète des coupures
  - Les boutons d'action (modifier, supprimer)
  - La pagination si disponible

#### Capture 05 : Signalements utilisateurs
- **URL** : http://127.0.0.1:5000/signalements
- **Nom du fichier** : `05_signalements.png`
- **Ce qu'il faut montrer** :
  - Le formulaire de signalement
  - La liste des signalements existants
  - Les statuts des signalements

#### Capture 06 : Notifications / Alertes
- **URL** : http://127.0.0.1:5000/notifications
- **Nom du fichier** : `06_notifications.png`
- **Ce qu'il faut montrer** :
  - Le formulaire d'abonnement
  - La liste des abonnements
  - L'historique des notifications

#### Capture 07 : Recommandations énergétiques
- **URL** : http://127.0.0.1:5000/recommandations
- **Nom du fichier** : `07_recommandations.png`
- **Ce qu'il faut montrer** :
  - Les conseils personnalisés par zone
  - Les KPIs contextuels

#### Capture 08 : Qualité des données
- **URL** : http://127.0.0.1:5000/qualite
- **Nom du fichier** : `08_qualite_donnees.png`
- **Ce qu'il faut montrer** :
  - Le score de qualité global
  - La complétude par colonne
  - La répartition des sources
  - Les anomalies détectées

#### Capture 09 : Sources de données
- **URL** : http://127.0.0.1:5000/sources
- **Nom du fichier** : `09_sources_donnees.png`
- **Ce qu'il faut montrer** :
  - Le catalogue des sources
  - Les URLs collectées
  - Les fichiers produits
  - La répartition par type de source

#### Capture 10 : Pipeline d'exécution
- **URL** : http://127.0.0.1:5000/pipeline
- **Nom du fichier** : `10_pipeline.png`
- **Ce qu'il faut montrer** :
  - Le journal des exécutions du pipeline
  - Les dates et statuts des runs
  - Les erreurs éventuelles

---

## SECTION 2 : Machine Learning (5 captures)

#### Capture 11 : Modèle ML - Métriques
- **URL** : http://127.0.0.1:5000/modele
- **Nom du fichier** : `11_modele_ml.png`
- **Ce qu'il faut montrer** :
  - Les métriques d'entraînement (MAE, RMSE, R², Accuracy)
  - La distribution des classes
  - La matrice de confusion
  - L'importance des variables
  - La comparaison standard/balanced

#### Capture 12 : Fiche modèle ML
- **URL** : http://127.0.0.1:5000/modele/fiche
- **Nom du fichier** : `12_fiche_modele.png`
- **Ce qu'il faut montrer** :
  - Le résumé du modèle
  - Les données utilisées
  - Les résultats et limites
  - Les recommandations

#### Capture 13 : Erreurs du modèle ML
- **URL** : http://127.0.0.1:5000/modele/erreurs
- **Nom du fichier** : `13_erreurs_modele.png`
- **Ce qu'il faut montrer** :
  - Les pires écarts de prédiction
  - Les erreurs de classification
  - L'analyse des cas problématiques

#### Capture 14 : Prédiction ML - Formulaire vide
- **URL** : http://127.0.0.1:5000/prediction
- **Nom du fichier** : `14_prediction_formulaire.png`
- **Ce qu'il faut montrer** :
  - Le formulaire de saisie des paramètres vide
  - Les champs disponibles (région, ville, type, cause, etc.)

#### Capture 15 : Prédiction ML - Résultat
- **URL** : http://127.0.0.1:5000/prediction
- **Nom du fichier** : `15_prediction_resultat.png`
- **Ce qu'il faut montrer** :
  - Le formulaire rempli avec des valeurs par défaut
  - Le résultat de prédiction (durée estimée, classe, confiance)
- **Conseil** : Remplissez le formulaire avant de capturer

---

## SECTION 3 : Détails et démonstration (5 captures)

#### Capture 16 : Navigation et menu
- **URL** : http://127.0.0.1:5000
- **Nom du fichier** : `16_navigation_menu.png`
- **Ce qu'il faut montrer** :
  - La barre de navigation complète
  - Le logo WattWatcher BF
  - Tous les liens du menu

#### Capture 17 : Dashboard - Zoom sur KPIs
- **URL** : http://127.0.0.1:5000
- **Nom du fichier** : `17_dashboard_kpis.png`
- **Ce qu'il faut montrer** :
  - Un zoom sur les cartes KPI uniquement
  - Les chiffres clés mis en évidence

#### Capture 18 : Dashboard - Zoom sur graphiques
- **URL** : http://127.0.0.1:5000
- **Nom du fichier** : `18_dashboard_graphiques.png`
- **Ce qu'il faut montrer** :
  - Un zoom sur les graphiques uniquement
  - Les visualisations interactives

#### Capture 19 : Suivi - Coupures actives
- **URL** : http://127.0.0.1:5000/suivi
- **Nom du fichier** : `19_suivi_actives.png`
- **Ce qu'il faut montrer** :
  - Un zoom sur la section "Coupures actives"
  - Les statuts (prévue, en cours)

#### Capture 20 : Page d'accueil complète
- **URL** : http://127.0.0.1:5000
- **Nom du fichier** : `20_accueil_complet.png`
- **Ce qu'il faut montrer** :
  - Une vue d'ensemble de l'application
  - L'interface utilisateur complète

---

## SECTION 4 : Scripts et code (5 captures)

#### Capture 21 : Application principale (backend/app.py)
- **Fichier** : `backend/app.py`
- **Nom du fichier** : `21_app_principal.png`
- **Ce qu'il faut montrer** :
  - L'importation des modules
  - La configuration de l'application Flask
  - Les routes principales
  - La connexion à la base de données
- **Conseil** : Capturez les 50-100 premières lignes pour montrer la structure

#### Capture 22 : Script de scraping (ingestion/scrape_medias.py)
- **Fichier** : `ingestion/scrape_medias.py`
- **Nom du fichier** : `22_scrape_medias.png`
- **Ce qu'il faut montrer** :
  - La fonction de scraping
  - L'extraction des données
  - La sauvegarde en CSV
- **Conseil** : Montrez la fonction principale d'extraction

#### Capture 23 : Script de nettoyage (processing/clean_coupures.py)
- **Fichier** : `processing/clean_coupures.py`
- **Nom du fichier** : `23_clean_coupures.png`
- **Ce qu'il faut montrer** :
  - Les fonctions de nettoyage
  - La normalisation des dates et régions
  - Le calcul des durées
- **Conseil** : Capturez les fonctions clés de nettoyage

#### Capture 24 : Script ML (ml/train_model.py)
- **Fichier** : `ml/train_model.py`
- **Nom du fichier** : `24_train_model.png`
- **Ce qu'il faut montrer** :
  - Le chargement des données
  - La préparation des features
  - L'entraînement du modèle Random Forest
  - Le calcul des métriques
- **Conseil** : Capturez la partie entraînement et évaluation

#### Capture 25 : Schéma de base de données (database/schema.sql)
- **Fichier** : `database/schema.sql`
- **Nom du fichier** : `25_schema_sql.png`
- **Ce qu'il faut montrer** :
  - La création des tables principales
  - Les définitions des colonnes
  - Les index et contraintes
- **Conseil** : Capturez les tables coupures et signalements

### 3. Enregistrer les captures

1. Après chaque capture, enregistrez dans : `docs/captures/`
2. Utilisez les noms de fichiers indiqués ci-dessus
3. Format : PNG (recommandé pour la qualité)
4. Résolution : 1920x1080 minimum

### 4. Vérification

À la fin, vous devriez avoir **25 fichiers PNG** dans `docs/captures/` :

**Section 1 - Pages principales (10 captures) :**
- 01_dashboard_principal.png
- 02_suivi_coupures.png
- 03_carte_zones.png
- 04_liste_coupures.png
- 05_signalements.png
- 06_notifications.png
- 07_recommandations.png
- 08_qualite_donnees.png
- 09_sources_donnees.png
- 10_pipeline.png

**Section 2 - Machine Learning (5 captures) :**
- 11_modele_ml.png
- 12_fiche_modele.png
- 13_erreurs_modele.png
- 14_prediction_formulaire.png
- 15_prediction_resultat.png

**Section 3 - Détails et démonstration (5 captures) :**
- 16_navigation_menu.png
- 17_dashboard_kpis.png
- 18_dashboard_graphiques.png
- 19_suivi_actives.png
- 20_accueil_complet.png

**Section 4 - Scripts et code (5 captures) :**
- 21_app_principal.png
- 22_scrape_medias.png
- 23_clean_coupures.png
- 24_train_model.png
- 25_schema_sql.png

## Conseils pour de bonnes captures

- **Mode plein écran** : Appuyez sur F11 avant de capturer
- **Zoom** : Utilisez Ctrl + 0 pour réinitialiser le zoom à 100%
- **Nettoyage** : Fermez les onglets inutiles et les barres latérales
- **Consistance** : Utilisez le même navigateur et la même résolution pour toutes les captures
- **Qualité** : Préférez le format PNG pour éviter la compression

## Intégration dans le rapport

Une fois les captures effectuées :
1. Insérez-les dans le rapport aux sections appropriées
2. Ajoutez des légendes descriptives
3. Référencez-les dans le texte du rapport

## Alternative : Outil de capture automatique

Si vous souhaitez automatiser les captures, vous pouvez utiliser :
- **Selenium** : Pour capturer automatiquement avec Python
- **Playwright** : Alternative plus moderne
- **Puppeteer** : Solution Node.js

Contactez-moi si vous souhaitez mettre en place une solution automatisée.
