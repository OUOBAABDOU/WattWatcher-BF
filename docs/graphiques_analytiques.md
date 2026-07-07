# Graphiques Analytiques du Projet WattWatcher BF

## Vue d'ensemble

Cette section présente les graphiques analytiques générés automatiquement à partir des données réelles de coupures d'électricité (330 enregistrements). Ces visualisations permettent d'analyser les patterns temporels, géographiques et causaux des coupures au Burkina Faso.

## Génération des graphiques

Les graphiques sont générés automatiquement avec le script Python :

```bash
.\.venv\Scripts\python.exe analytics\generate_graphiques.py
```

**Dépendances** : matplotlib, pandas, seaborn

## Liste des graphiques

### 1. Durée moyenne par région
- **Fichier** : `graphique_duree_moyenne_region.png`
- **Type** : Bar chart
- **Description** : Durée moyenne des coupures par région administrative
- **Objectif** : Identifier les régions les plus touchées en termes de durée
- **Insights** : Permet de voir quelles régions subissent les coupures les plus longues en moyenne

### 2. Distribution des durées
- **Fichier** : `graphique_distribution_durees.png`
- **Type** : Histogramme
- **Description** : Distribution de la durée des coupures avec moyenne et médiane
- **Objectif** : Comprendre la concentration des durées (courte/moyenne/longue)
- **Insights** : Montre si les coupures sont généralement courtes ou longues, avec les indicateurs de tendance centrale

### 3. Coupures par jour de semaine
- **Fichier** : `graphique_coupures_jour_semaine.png`
- **Type** : Bar chart
- **Description** : Répartition des coupures selon les jours de la semaine
- **Objectif** : Identifier les jours les plus critiques
- **Insights** : Permet de détecter des patterns hebdomadaires (ex: plus de coupures en début de semaine)

### 4. Coupures par période de journée
- **Fichier** : `graphique_coupures_periode_journee.png`
- **Type** : Bar chart
- **Description** : Répartition selon les périodes de la journée (matin, après-midi, soir, nuit)
- **Objectif** : Identifier les heures de pointe des coupures
- **Insights** : Montre quels moments de la journée sont les plus susceptibles d'avoir des coupures

### 5. Coupures par cause
- **Fichier** : `graphique_coupures_par_cause.png`
- **Type** : Bar chart horizontal
- **Description** : Top 10 des causes principales des coupures
- **Objectif** : Comprendre les raisons principales des coupures
- **Insights** : Identifie les causes les plus fréquentes (panne, maintenance, surcharge, etc.)

### 6. Évolution annuelle
- **Fichier** : `graphique_evolution_annuelle.png`
- **Type** : Line chart (double)
- **Description** : Évolution du nombre de coupures et de la durée moyenne par année
- **Objectif** : Analyser les tendances sur plusieurs années
- **Insights** : Permet de voir si la situation s'améliore ou se dégrade dans le temps

### 7. Top 10 villes
- **Fichier** : `graphique_top10_villes.png`
- **Type** : Bar chart horizontal
- **Description** : Les 10 villes les plus touchées par les coupures
- **Objectif** : Focus sur les zones urbaines critiques
- **Insights** : Identifie les villes nécessitant une attention particulière

### 8. Boxplot durée par type
- **Fichier** : `graphique_boxplot_duree_type.png`
- **Type** : Box plot
- **Description** : Distribution des durées selon le type de coupure
- **Objectif** : Comparer la variabilité des durées selon le type
- **Insights** : Montre quels types de coupures ont les durées les plus variables

### 9. Heatmap région x mois
- **Fichier** : `graphique_heatmap_region_mois.png`
- **Type** : Heatmap
- **Description** : Matrice chaleur des coupures par région et mois
- **Objectif** : Visualiser les patterns spatio-temporels
- **Insights** : Identifie les régions et mois critiques (ex: saisonnalité)

### 10. Coupures par province
- **Fichier** : `graphique_coupures_par_province.png`
- **Type** : Bar chart horizontal
- **Description** : Top 15 des provinces les plus touchées
- **Objectif** : Analyse plus fine au niveau provincial
- **Insights** : Complète l'analyse régionale avec une granularité plus fine

## Utilisation des graphiques

### Dans le rapport

Ces graphiques peuvent être intégrés dans le rapport final pour :

- **Section Analyse des données** : Présentation des patterns identifiés
- **Section Résultats** : Illustration des findings principaux
- **Annexe Graphiques** : Référence complète des visualisations

### Dans la présentation

Pour la soutenance, les graphiques les plus pertinents sont :

1. **Durée moyenne par région** - Pour montrer l'impact géographique
2. **Coupures par cause** - Pour expliquer les raisons
3. **Évolution annuelle** - Pour montrer les tendances
4. **Heatmap région x mois** - Pour visualiser la saisonnalité

### Légendes descriptives

Exemple de légende pour le rapport :

```
**Figure X : Durée moyenne des coupures par région**

Ce graphique à barres présente la durée moyenne des coupures d'électricité
par région administrative du Burkina Faso. La région de [X] affiche la durée
moyenne la plus élevée avec [Y] minutes, suivie de [Z]. Cette analyse permet
d'identifier les régions nécessitant une attention particulière pour améliorer
la continuité du service électrique.

*Source : Données réelles collectées (330 coupures)*
```

## Données utilisées

- **Source** : Base de données PostgreSQL
- **Table** : `coupures`
- **Nombre d'enregistrements** : 330 coupures réelles
- **Période** : [Année de début] - [Année de fin]
- **Couverture géographique** : 13 régions du Burkina Faso

## Technologies utilisées

- **Python** : Langage de programmation
- **Pandas** : Manipulation des données
- **Matplotlib** : Création des graphiques
- **Seaborn** : Visualisations avancées (heatmap)
- **SQLAlchemy** : Connexion à la base de données

## Personnalisation

Le script `analytics/generate_graphiques.py` peut être personnalisé pour :

- Ajouter de nouveaux graphiques
- Modifier les couleurs et styles
- Changer les filtres de données
- Ajuster les dimensions et résolution
- Ajouter des annotations spécifiques

## Mise à jour

Pour régénérer les graphiques après mise à jour des données :

```bash
# 1. Relancer le chargement des données
.\.venv\Scripts\python.exe ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures

# 2. Régénérer les graphiques
.\.venv\Scripts\python.exe analytics\generate_graphiques.py
```

## Emplacement

Tous les graphiques sont sauvegardés dans : `docs/captures/`

## Références

- Guide complet : `docs/captures/guide_graphiques.md`
- Script de génération : `analytics/generate_graphiques.py`
- Instructions de captures : `docs/captures/instructions_captures.md`
