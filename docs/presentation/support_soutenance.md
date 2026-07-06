# Support de soutenance — WattWatcher BF

## Diapositive 1 : Titre

**WattWatcher BF**  
Application de suivi des coupures d'électricité et de gestion énergétique au Burkina Faso

**Sujet 21**  
Filière : Génie logiciel — Licence 3 Analyse de données  
Présenté par : [Votre nom]  
Juillet 2026

---

## Diapositive 2 : Contexte énergétique

### Situation au Burkina Faso

- **Défis énergétiques** : Coupures fréquentes impactant ménages et entreprises
- **Sources d'information dispersées** :
  - Communiqués officiels SONABEL
  - Articles de presse (Wakat Séra, Lefaso.net, Faso Actu)
  - Signalements communautaires
- **Besoin de centralisation** : Aucun système unifié de suivi et d'analyse

### Impact des coupures

- Perturbation des activités économiques
- Difficultés pour la planification
- Manque de visibilité sur les tendances

---

## Diapositive 3 : Problématique

**Comment collecter, structurer et analyser les informations de coupures d'électricité afin d'aider les utilisateurs à mieux anticiper et gérer leur consommation énergétique ?**

### Questions sous-jacentes

- Comment centraliser les informations dispersées ?
- Comment extraire automatiquement les données utiles ?
- Comment stocker et traiter ces données efficacement ?
- Comment fournir des visualisations et prédictions utiles ?

---

## Diapositive 4 : Objectifs

### Objectif général

Développer une application web qui collecte, stocke, analyse et visualise les données relatives aux coupures d'électricité.

### Objectifs spécifiques

1. ✅ Collecter les données depuis plusieurs sources (web, CSV, signalements)
2. ✅ Extraire automatiquement les informations (texte, PDF, image)
3. ✅ Stocker dans PostgreSQL
4. ✅ Nettoyer et transformer avec Python/Pandas
5. ✅ Produire statistiques et visualisations
6. ✅ Mettre en place un tableau de bord interactif
7. ✅ Proposer une prédiction de durée
8. ✅ Générer des recommandations énergétiques
9. ✅ Permettre aux utilisateurs de signaler une coupure

---

## Diapositive 5 : Sources de données

### Sources réelles utilisées (330 coupures)

| Source | Type | Pourcentage | Méthode |
|--------|------|-------------|---------|
| SONABEL | Officielle | 40% | Communiqués Facebook |
| Wakat Séra | Média | 25% | Scraping web |
| Lefaso.net | Média | 15% | Scraping web |
| Faso Actu | Média | 10% | Scraping web |
| Signalements | Terrain | 10% | Formulaire utilisateur |

### Enrichissement des données

- **Open-Meteo API** : Température et précipitations
- **NASA POWER API** : Irradiation solaire
- **Banque mondiale** : Contexte énergétique national

### Période couverte

2020-2026 (330 coupures réelles)

---

## Diapositive 6 : Architecture

### Flux de données

```
Sources (SONABEL, Médias, Signalements)
    ↓
Ingestion (Scraping, APIs, Formulaire)
    ↓
Nettoyage (Pandas, Feature engineering)
    ↓
PostgreSQL (Stockage)
    ↓
Flask API (Backend)
    ↓
Dashboard + ML + Recommandations
```

### Stack technologique

- **Backend** : Flask, Flask-SQLAlchemy
- **Base de données** : PostgreSQL (Docker)
- **Data processing** : Pandas, NumPy
- **Machine Learning** : Scikit-learn
- **Scraping** : Requests, BeautifulSoup
- **Visualisation** : Plotly

---

## Diapositive 7 : Base de données

### Schéma PostgreSQL (7 tables)

1. **coupures** : Stockage des coupures (330 enregistrements)
2. **signalements** : Signalements utilisateurs
3. **abonnements** : Abonnements aux alertes
4. **notifications** : Historique des notifications
5. **source_documents** : Traçabilité des sources
6. **recommandations** : Recommandations énergétiques
7. **pipeline_runs** : Journal des exécutions

### Variables principales

- Temporelles : date, heure, durée, année, mois
- Géographiques : région, province, ville, zone, lat/lon
- Techniques : type, cause, statut
- Enrichissement : température, précipitation, irradiation

---

## Diapositive 8 : Tableau de bord

### Fonctionnalités

- **Dashboard principal** : KPIs et graphiques interactifs
- **Suivi temps réel** : Coupures par région/zone avec filtres
- **Carte géographique** : Visualisation des zones touchées
- **Qualité des données** : Rapport de complétude et anomalies
- **Traçabilité des sources** : Historique des collectes

### KPIs affichés

- Total coupures : 330
- Durée moyenne : 226 min
- Durée médiane : 240 min
- Zones suivies : 19
- Coupures actives : [variable]

### Captures d'écran du projet

**Section 1 - Pages principales (10 captures)**
- Capture 01 : Dashboard principal avec KPIs et graphiques
- Capture 02 : Suivi des coupures en temps réel
- Capture 03 : Carte géographique des zones
- Capture 04 : Liste des coupures (CRUD)
- Capture 05 : Signalements utilisateurs
- Capture 06 : Système d'alertes et notifications
- Capture 07 : Recommandations énergétiques
- Capture 08 : Rapport qualité des données
- Capture 09 : Traçabilité des sources
- Capture 10 : Pipeline d'exécution

**Section 2 - Machine Learning (5 captures)**
- Capture 11 : Métriques du modèle ML
- Capture 12 : Fiche technique du modèle
- Capture 13 : Analyse des erreurs
- Capture 14 : Formulaire de prédiction
- Capture 15 : Résultat de prédiction

**Section 3 - Détails et démonstration (5 captures)**
- Capture 16 : Navigation et menu
- Capture 17 : Zoom sur les KPIs
- Capture 18 : Zoom sur les graphiques
- Capture 19 : Coupures actives
- Capture 20 : Vue d'ensemble complète

**Section 4 - Scripts et code (5 captures)**
- Capture 21 : Application principale (backend/app.py)
- Capture 22 : Script de scraping (ingestion/scrape_medias.py)
- Capture 23 : Script de nettoyage (processing/clean_coupures.py)
- Capture 24 : Script ML (ml/train_model.py)
- Capture 25 : Schéma de base de données (database/schema.sql)

---

## Diapositive 9 : Machine Learning

### Modèle implémenté

- **Algorithme** : Random Forest Regressor
- **Tâches** :
  - Régression de durée (en minutes)
  - Classification (courte/moyenne/longue)
- **Données** : 264 entraînement / 66 test

### Métriques

| Métrique | Valeur |
|----------|--------|
| MAE | 117.72 min |
| RMSE | 139.4 min |
| R² | -0.135 |
| Accuracy | 51.5% |
| Baseline | 53% |

### Variables importantes

1. Température max (21.5%)
2. Irradiation solaire (20.8%)
3. Mois (11.4%)
4. Précipitation (10.1%)

### [Capture d'écran de la page modèle]

---

## Diapositive 10 : Résultats

### Conformité au cahier des charges

- ✅ Collecte multi-sources
- ✅ Extraction automatique
- ✅ Stockage PostgreSQL
- ✅ Nettoyage et transformation
- ✅ Statistiques et visualisations
- ✅ Tableau de bord interactif
- ✅ Prédiction de durée
- ✅ Recommandations énergétiques
- ✅ Signalements utilisateurs

### Tests automatisés

- **Total tests** : 39
- **Résultat** : 39/39 passés (100%)
- **Couverture** : Fonctionnelle complète

### Données

- **100% réelles** : Aucune donnée simulée en production
- **Sources variées** : Officielles, médias, terrain
- **Enrichissement** : Météo et solaire

---

## Diapositive 11 : Recommandations

### Recommandations énergétiques

- Conseils personnalisés par zone
- Adaptés au contexte local
- Basés sur les données historiques

### Système d'alertes

- Abonnements par région, ville, zone
- Notifications simulées (web/email/SMS)
- Génération automatique pour les nouvelles coupures

### Exemples de recommandations

- "Investir dans un générateur pour les zones à forte fréquence"
- "Planifier les activités sensibles en dehors des pics horaires"
- "Utiliser des solutions solaires pour les zones à longue durée"

### [Capture d'écran de la page recommandations]

---

## Diapositive 12 : Conclusion et perspectives

### Conclusion

Le projet WattWatcher BF répond au sujet 21 en proposant :

- ✅ Application fonctionnelle et testée
- ✅ Données 100% réelles (330 coupures)
- ✅ Toutes les fonctionnalités requises
- ✅ Architecture scalable et documentée
- ✅ Base solide pour améliorations futures

### Perspectives

1. **Intégration SMS réelle** : Alertes opérationnelles
2. **Plus de données réelles** : Amélioration du modèle ML
3. **API SONABEL officielle** : Collecte robuste
4. **Application mobile** : Accessibilité accrue
5. **Sécurité renforcée** : Authentification et chiffrement
6. **Carte avancée** : Interactivité améliorée

### Remerciements

Merci de votre attention.

---

## Notes pour le présentateur

### Durée estimée

- Introduction (diapos 1-4) : 5 minutes
- Implémentation (diapos 5-8) : 7 minutes
- Résultats (diapos 9-11) : 5 minutes
- Conclusion (diapos 12) : 3 minutes
- **Total** : 20 minutes

### Points clés à souligner

- **Données réelles** : Insister sur le fait que toutes les données sont réelles
- **Conformité** : Mettre en avant la conformité 100% au cahier des charges
- **Tests** : Mentionner les 39 tests passés
- **Limites** : Être honnête sur les limites du modèle ML
- **Perspectives** : Présenter les améliorations futures de manière réaliste

### Questions anticipées

**Q : Pourquoi le modèle ML a-t-il une accuracy faible ?**  
R : Le volume de données réelles (330) est limité. Le modèle sert de démonstrateur technique.

**Q : Les alertes sont-elles réelles ?**  
R : Simulées dans cette version. Intégration SMS prévue pour la production.

**Q : Comment les données sont-elles collectées ?**  
R : Scraping web automatique, APIs météo/solaire, et formulaire utilisateur.

**Q : Le projet est-il scalable ?**  
R : Oui, architecture modulaire avec PostgreSQL et Flask, prête pour plus de données.

### Matériel à emporter

- Ordinateur avec application démarrée
- Captures d'écran des pages principales
- Rapport imprimé ou sur tablette
- Fiche modèle ML

### Démonstration (optionnelle)

Si le temps le permet, une démonstration live de l'application peut être faite :
1. Montrer le dashboard principal
2. Naviguer sur la carte
3. Montrer la page de suivi
4. Faire une prédiction ML
5. Montrer les recommandations
