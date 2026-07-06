# Commandes utiles - WattWatcher BF

Commandes PowerShell a executer depuis la racine du projet.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Verifier que `.env` pointe vers PostgreSQL Docker :

```text
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/wattwatcher_db
```

## Demarrer PostgreSQL

```powershell
docker compose up -d
docker compose ps
```

## Charger les donnees reelles

Pipeline complet avec chargement DB :

```powershell
.\run-real-data-pipeline.ps1 -LoadDb
```

Recharger seulement la base PostgreSQL avec le dataset reel combine :

```powershell
.\.venv\Scripts\python.exe ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures
```

Verifier le nombre de lignes PostgreSQL :

```powershell
.\.venv\Scripts\python.exe -c "import psycopg2; conn=psycopg2.connect(host='localhost', port=5433, dbname='wattwatcher_db', user='postgres', password='postgres'); cur=conn.cursor(); cur.execute('select count(*) from coupures'); print(cur.fetchone()[0]); conn.close()"
```

## Entrainer les modeles ML

Modele standard :

```powershell
.\.venv\Scripts\python.exe ml\train_model.py --input data\final\dataset_coupures_reelles_combine.csv --real-only --out ml\model_real.pkl --metrics-out data\processed\model_metrics_real.json --model-card-out docs\rapport\fiche_modele.md --predictions-out data\processed\model_predictions_real.csv --n-estimators 160 --test-size 0.2 --random-state 42 --class-weight none
```

Modele balanced :

```powershell
.\.venv\Scripts\python.exe ml\train_model.py --input data\final\dataset_coupures_reelles_combine.csv --real-only --out ml\model_real_balanced.pkl --metrics-out data\processed\model_metrics_real_balanced.json --n-estimators 160 --test-size 0.2 --random-state 42 --class-weight balanced
```

## Lancer l'application

Avec PostgreSQL :

```powershell
.\.venv\Scripts\python.exe run_flask_postgres.py
```

Mode local SQLite de secours pour une demo rapide :

```powershell
.\run-flask-local.ps1
```

Ouvrir :

```text
http://127.0.0.1:5000
```

Pages importantes :

```text
http://127.0.0.1:5000/suivi
http://127.0.0.1:5000/carte
http://127.0.0.1:5000/sources
http://127.0.0.1:5000/qualite
http://127.0.0.1:5000/modele
http://127.0.0.1:5000/modele/fiche
http://127.0.0.1:5000/modele/erreurs
http://127.0.0.1:5000/prediction
http://127.0.0.1:5000/pipeline
```

## Checklist demo manuelle

1. Ouvrir `http://127.0.0.1:5000` et verifier les KPI globaux.
2. Ouvrir `/suivi` pour montrer les coupures recentes et actives.
3. Ouvrir `/carte` pour montrer les zones geolocalisees.
4. Ouvrir `/sources` pour expliquer les fichiers et sources collectees.
5. Ouvrir `/qualite` pour montrer la qualite des donnees.
6. Ouvrir `/modele` pour presenter les scores ML, la matrice de confusion et le desequilibre des classes.
7. Ouvrir `/modele/fiche` pour montrer la fiche modele prete pour le rapport.
8. Ouvrir `/modele/erreurs` pour expliquer les erreurs de prediction.
9. Ouvrir `/prediction` et tester un scenario avec le modele `standard`, puis `balanced`.
10. Ouvrir `/notifications`, creer un abonnement, puis ajouter une coupure dans la meme zone depuis `/coupures` pour verifier l'alerte.

Apres un test d'ajout de coupure, les compteurs de la base locale peuvent augmenter. Pour une demo propre avec PostgreSQL, recharger le CSV reel combine avec `--replace-coupures`.

## Ordre conseille pour la soutenance

1. Probleme : suivi des coupures et aide a la decision energetique.
2. Donnees : sources reelles, fichiers collectes, qualite et tracabilite.
3. Application : suivi, carte, notifications et recommandations.
4. Modele ML : prediction de duree, classes courte/moyenne/longue, limites et confiance.
5. Demonstration : ajouter un abonnement, ajouter une coupure, verifier l'alerte.
6. Conclusion : donnees reelles exploitees, pipeline reproductible, axes d'amelioration.

## Questions possibles du jury

**Pourquoi utiliser PostgreSQL ?**
Stocker les coupures, signalements, abonnements et notifications dans une base relationnelle fiable, proche d'un usage reel.

**Pourquoi garder SQLite ?**
SQLite sert uniquement de mode local de secours pour lancer une demo rapide si Docker/PostgreSQL n'est pas disponible.

**Quelles donnees sont reelles ?**
Le dataset combine `data/final/dataset_coupures_reelles_combine.csv` contient les lignes retenues apres filtrage des sources officielles, medias et terrain. Les lignes de simulation sont exclues du chargement de demo.

**Pourquoi le modele n'est pas parfait ?**
Le volume de donnees reelles reste limite et les classes sont desequilibrees : la classe `moyenne` est majoritaire et la classe `courte` minoritaire. Le modele doit donc etre presente comme une aide a la decision, pas comme une verite absolue.

**Pourquoi comparer `standard` et `balanced` ?**
La variante `balanced` teste une ponderation des classes minoritaires. La page `/modele` compare les deux variantes pour choisir selon les metriques observees.

**Que montre la confiance de prediction ?**
Elle indique si le classifieur distingue clairement une classe ou si les probabilites sont proches. En confiance faible, la prediction doit etre verifiee avec les donnees terrain.

**Comment reproduire la demo ?**
Lancer PostgreSQL, charger les donnees reelles, entrainer les modeles si besoin, lancer Flask, puis suivre la checklist demo manuelle.

## Verification rapide en 2 minutes

Verifier Docker/PostgreSQL :

```powershell
docker compose ps
.\.venv\Scripts\python.exe -c "import psycopg2; conn=psycopg2.connect(host='localhost', port=5433, dbname='wattwatcher_db', user='postgres', password='postgres'); cur=conn.cursor(); cur.execute('select count(*) from coupures'); print('postgres_rows=', cur.fetchone()[0]); conn.close()"
```

Verifier que Flask repond :

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5000/api/model-metrics
```

Verifier les KPI :

```powershell
$stats = Invoke-RestMethod http://127.0.0.1:5000/api/stats
$stats.kpis
```

Verifier le modele :

```powershell
$metrics = Invoke-RestMethod http://127.0.0.1:5000/api/model-metrics
$metrics.available
$metrics.dataset.class_balance
```

Verifier une prediction :

```powershell
$prediction = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/predict-duration -ContentType 'application/json' -Body '{"region":"Centre","ville":"Ouagadougou","zone":"Tanghin","type_coupure":"pr\u00e9vue","mois":7,"heure_num":8,"jour_num":4,"temperature_max":36,"precipitation":0,"irradiation_solaire":5.5,"model_variant":"standard"}'
$prediction.model_variant
$prediction.prediction
```

## Tests automatiques

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Test manuel rapide des APIs

Statistiques :

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/stats
```

Metriques ML :

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/model-metrics
```

Resultats attendus avec les donnees reelles actuelles :

```text
PostgreSQL propre : 330 coupures
Modele disponible : available=True
Desequilibre classes : moyenne/courte, ratio 4.46
Tests automatises : 39 passed
```

Prediction standard :

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/predict-duration -ContentType 'application/json' -Body '{"region":"Centre","ville":"Ouagadougou","zone":"Tanghin","type_coupure":"pr\u00e9vue","mois":7,"heure_num":8,"jour_num":4,"temperature_max":36,"precipitation":0,"irradiation_solaire":5.5,"model_variant":"standard"}'
```

Prediction balanced :

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/predict-duration -ContentType 'application/json' -Body '{"region":"Centre","ville":"Ouagadougou","zone":"Tanghin","type_coupure":"pr\u00e9vue","mois":7,"heure_num":8,"jour_num":4,"temperature_max":36,"precipitation":0,"irradiation_solaire":5.5,"model_variant":"balanced"}'
```

## Generer les rendus HTML/JSON

```powershell
.\.venv\Scripts\python.exe render_real_pages.py
```

Les fichiers sont produits dans :

```text
data/rendered/
docs/rapport/fiche_modele.md
```

## Arreter les services

Arreter PostgreSQL Docker :

```powershell
docker compose down
```

Trouver le processus Flask sur le port 5000 :

```powershell
netstat -ano | Select-String ":5000"
```

Arreter un processus Flask par PID :

```powershell
Stop-Process -Id <PID> -Force
```

## Depannage rapide

Si la valeur `type_coupure` avec accent s'affiche mal dans PowerShell, utiliser l'echappement JSON ASCII :

```json
"type_coupure":"pr\u00e9vue"
```

Si le port 5000 est deja occupe :

```powershell
netstat -ano | Select-String ":5000"
Stop-Process -Id <PID> -Force
```

Si PostgreSQL ne repond pas :

```powershell
docker compose ps
docker compose up -d
```

Si la page `/notifications` echoue en SQLite local apres une evolution du schema, relancer l'application. Le demarrage applique automatiquement les colonnes manquantes.

Si une demo a ajoute des lignes de test dans PostgreSQL, remettre la base propre :

```powershell
.\.venv\Scripts\python.exe ingestion\load_to_postgres.py --csv data\final\dataset_coupures_reelles_combine.csv --replace-coupures
```
