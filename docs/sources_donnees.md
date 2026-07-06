# Sources de données du projet WattWatcher BF

Le projet combine un dataset structuré existant, des sources web réellement collectées, des données météo/solaires téléchargées par API et les signalements des utilisateurs. Cette distinction est importante pour le rapport : toutes les sources ne sont pas au même niveau de maturité.

## Sources réellement utilisées dans la version actuelle

| Source | Statut | Méthode | Utilisation |
|---|---|---|---|
| `data/final/dataset_coupures_reelles_combine.csv` | Dataset réel combiné opérationnel | CSV local généré | Tests, dashboard, modèle ML, chargement PostgreSQL |
| `data/final/dataset_coupures_2020_2026.csv` | Dataset initial filtrable | CSV local | Base historique, filtrée pour exclure les simulations |
| `data/final/dataset_coupures_reelles_collectees.csv` | Coupures web collectées et enrichies | Scraping + APIs météo/solaire | Complément réel récent |
| Signalements utilisateurs | Fonctionnel | Formulaire Flask | Confirmation communautaire et complément terrain |
| PostgreSQL Docker | Fonctionnel | `ingestion/load_to_postgres.py` | Stockage des coupures, signalements, notifications |
| Articles médias listés dans `data/raw/url_seeds_sonabel_medias.csv` | Collecte opérationnelle | Requests + BeautifulSoup | Extraction de texte et génération d’un CSV structuré |
| Open-Meteo Historical Weather API | Téléchargé | API JSON/CSV | Température maximale et précipitations des coupures collectées |
| NASA POWER Daily API | Téléchargé | API JSON/CSV | Irradiation solaire des coupures collectées |
| Banque mondiale | Téléchargé | API JSON/CSV | Contexte énergétique national |

## Sources prévues ou partiellement intégrées

| Source | URL | Méthode | Niveau actuel |
|---|---|---|---|
| SONABEL Facebook officiel | https://www.facebook.com/sonabelbf/ | API officielle si disponible, veille manuelle, OCR | Prévu, car l’accès automatisé peut être limité |
| SONABEL X | https://x.com/SONABEL2 | API X si autorisée ou veille manuelle | Prévu |
| Wakat Séra | https://www.wakatsera.com/?s=SONABEL+coupure | Scraping BeautifulSoup | Prototype opérationnel |
| Lefaso.net | https://lefaso.net/ | Scraping/recherche manuelle | Prototype |
| Faso Actu | https://faso-actu.info/?s=SONABEL | Scraping BeautifulSoup | Prototype |

## Pipeline de collecte

1. Collecter les pages ou communiqués via `ingestion/scrape_medias.py`.
2. Sauvegarder les textes bruts dans `data/raw/medias/articles_collectes.csv`.
3. Extraire les champs structurés dans `data/raw/medias/coupures_structurees.csv` : date, heures, région, ville, zone, cause, source, niveau de confiance.
4. Télécharger les données météo Open-Meteo, les données solaires NASA POWER et l’indicateur Banque mondiale.
5. Enrichir les coupures collectées avec `processing/enrich_real_coupures.py`.
6. Combiner le dataset réel historique et les coupures collectées avec `processing/merge_real_datasets.py`.
7. Charger `data/final/dataset_coupures_reelles_combine.csv` dans PostgreSQL avec `ingestion/load_to_postgres.py --replace-coupures`.
8. Compléter et valider les données avec les signalements utilisateurs.

## Limites à mentionner dans le rapport

- Les communiqués SONABEL ne sont pas toujours publiés dans un format structuré.
- Certains sites peuvent bloquer le scraping ou modifier leur HTML.
- Le dataset initial contenait des lignes expérimentales, mais le dataset combiné final exclut `source_type=simulation` et n'utilise que des données réelles.
- Les alertes email/SMS/WhatsApp sont simulées dans cette version ; elles peuvent être branchées plus tard sur un fournisseur réel.
