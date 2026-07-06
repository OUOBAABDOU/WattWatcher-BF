# Dictionnaire de données

## Table `coupures`

| Champ | Description |
|---|---|
| id_coupure | Identifiant unique |
| date_publication | Date de publication du communiqué/source |
| date_debut | Date de début |
| heure_debut | Heure de début |
| date_fin | Date de fin |
| heure_fin | Heure de fin |
| duree_minutes | Durée calculée en minutes |
| annee | Année |
| mois | Mois |
| jour_semaine | Jour de la semaine |
| periode_journee | matin, après-midi, soir |
| region | Région administrative |
| province | Province |
| ville | Ville |
| zone | Quartier/localité |
| latitude | Latitude approximative |
| longitude | Longitude approximative |
| type_coupure | prévue, imprévue, perturbation, travaux |
| cause | Cause ou description |
| statut | prévue, en cours, terminée |
| source_name | Nom de la source |
| source_type | officielle, média, terrain, simulation |
| url_source | Lien de la source |
| niveau_confiance | Fiabilité entre 0 et 1 |
| niveau_impact | faible, moyen, élevé |
| temperature_max | Température maximale |
| precipitation | Précipitations |
| irradiation_solaire | Irradiation solaire journalière |

## Rapport qualité des données

| Champ | Description |
|---|---|
| total_lignes | Nombre de lignes contrôlées |
| completude_moyenne | Pourcentage moyen de complétude des champs obligatoires |
| completude_par_colonne | Détail de complétude par champ contrôlé |
| doublons | Nombre de doublons détectés sur date, heures, ville, zone et URL |
| anomalies | Contrôles d’anomalies : durée invalide, dates incohérentes, type de source inconnu |
| repartition_sources | Nombre de lignes par type de source |
| score_qualite | Score synthétique entre 0 et 100 |

## Table `pipeline_runs`

| Champ | Description |
|---|---|
| id_run | Identifiant unique de l'exécution |
| pipeline_name | Nom du pipeline exécuté |
| date_start | Date et heure de début |
| date_end | Date et heure de fin |
| status | running, success ou failed |
| records_read | Nombre de lignes lues |
| records_inserted | Nombre de lignes insérées ou produites |
| records_rejected | Nombre de lignes rejetées |
| error_message | Message d'erreur si l'exécution échoue |
