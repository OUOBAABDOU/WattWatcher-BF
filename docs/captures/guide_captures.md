# Guide de captures d'écran - WattWatcher BF

## Application fonctionnant sur http://127.0.0.1:5000

### Pages à capturer pour le rapport

#### 1. Tableau de bord principal (http://127.0.0.1:5000)
- **Nom de fichier**: `dashboard_principal.png`
- **Description**: Page d'accueil avec les KPIs principaux et graphiques
- **Éléments à montrer**:
  - Cartes KPI (Total coupures, Durée moyenne, Durée médiane, etc.)
  - Graphique par région
  - Graphique par mois
  - Répartition par source
  - Carte géographique des zones touchées

#### 2. Page de suivi (http://127.0.0.1:5000/suivi)
- **Nom de fichier**: `suivi_coupures.png`
- **Description**: Liste des coupures avec filtres et coupures actives
- **Éléments à montrer**:
  - Tableau des coupures récentes
  - Section des coupures actives (prévue/en cours)
  - Filtres par région, ville, zone, statut

#### 3. Page carte (http://127.0.0.1:5000/carte)
- **Nom de fichier**: `carte_zones.png`
- **Description**: Carte interactive des zones touchées
- **Éléments à montrer**:
  - Carte géographique centrée sur le Burkina Faso
  - Points représentant les zones avec coupures
  - Tableau des zones cartographiées

#### 4. Page modèle ML (http://127.0.0.1:5000/modele)
- **Nom de fichier**: `modele_ml.png`
- **Description**: Métriques du modèle de machine learning
- **Éléments à montrer**:
  - Statistiques d'entraînement
  - Distribution des classes
  - Matrice de confusion
  - Importance des variables
  - Comparaison standard/balanced

#### 5. Page fiche modèle (http://127.0.0.1:5000/modele/fiche)
- **Nom de fichier**: `fiche_modele.png`
- **Description**: Fiche technique du modèle pour le rapport
- **Éléments à montrer**:
  - Résumé du modèle
  - Données utilisées
  - Résultats et limites
  - Recommandations

#### 6. Page prédiction (http://127.0.0.1:5000/prediction)
- **Nom de fichier**: `prediction_ml.png`
- **Description**: Interface de prédiction de durée
- **Éléments à montrer**:
  - Formulaire de saisie des paramètres
  - Résultat de prédiction (exemple avec valeurs par défaut)

#### 7. Page qualité des données (http://127.0.0.1:5000/qualite)
- **Nom de fichier**: `qualite_donnees.png`
- **Description**: Rapport de qualité des données
- **Éléments à montrer**:
  - Score de qualité global
  - Complétude par colonne
  - Répartition des sources
  - Anomalies détectées

#### 8. Page sources (http://127.0.0.1:5000/sources)
- **Nom de fichier**: `sources_donnees.png`
- **Description**: Traçabilité des sources de données
- **Éléments à montrer**:
  - Catalogue des sources
  - URLs collectées
  - Fichiers produits
  - Répartition par type de source

#### 9. Page recommandations (http://127.0.0.1:5000/recommandations)
- **Nom de fichier**: `recommandations.png`
- **Description**: Recommandations énergétiques
- **Éléments à montrer**:
  - Conseils personnalisés par zone
  - KPIs contextuels

#### 10. Page notifications (http://127.0.0.1:5000/notifications)
- **Nom de fichier**: `notifications.png`
- **Description**: Système d'abonnements et alertes
- **Éléments à montrer**:
  - Formulaire d'abonnement
  - Liste des abonnements
  - Historique des notifications

## Instructions pour les captures

1. **Ouvrir le navigateur** sur http://127.0.0.1:5000
2. **Mode plein écran**: F11 pour une meilleure qualité
3. **Capturer chaque page** avec l'outil de capture d'écran (Windows + Shift + S)
4. **Enregistrer** dans le dossier `docs/captures/` avec les noms indiqués
5. **Format**: PNG de préférence pour la qualité
6. **Résolution**: 1920x1080 minimum recommandé

## Données utilisées

Toutes les captures montrent des **données réelles** :
- 330 coupures réelles collectées
- Sources officielles SONABEL
- Médias burkinabé (Wakat Séra, Lefaso.net, Faso Actu)
- Signalements utilisateurs
- Enrichissement météo/solaire via APIs

## Statut de l'application

- ✅ Application Flask démarrée et fonctionnelle
- ✅ PostgreSQL connecté avec données réelles
- ✅ Toutes les pages accessibles
- ✅ Modèle ML entraîné sur données réelles
- ✅ Tests automatisés : 39/39 passés
