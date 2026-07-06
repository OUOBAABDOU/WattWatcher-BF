# Architecture technique

```mermaid
flowchart TD
    A[Sources SONABEL, médias, PDF, images, API météo, API solaire] --> B[Ingestion]
    B --> C[Stockage brut]
    C --> D[Nettoyage et normalisation Pandas]
    D --> E[PostgreSQL]
    E --> F[API Flask]
    E --> G[Analyse et indicateurs]
    G --> H[Dashboard Plotly]
    D --> I[Modèle ML Scikit-learn]
    I --> J[Prédiction de durée]
    H --> K[Recommandations énergétiques]
```

## Modules

1. **Ingestion** : scraping HTML, PDF, OCR, API météo, API solaire, API Banque mondiale.
2. **Processing** : nettoyage, normalisation des zones, calcul des durées, feature engineering.
3. **Database** : PostgreSQL pour stocker coupures, sources, signalements, notifications.
4. **Backend** : Flask pour l’application web et les endpoints API.
5. **Analytics** : indicateurs, graphiques et exports.
6. **ML** : Random Forest Regressor pour prédire la durée probable d’une coupure.
