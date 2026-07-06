# Spécification API

## GET /api/coupures
Retourne les coupures enregistrées. Les paramètres `region`, `ville`, `zone`, `statut` et `aujourdhui=1` permettent de filtrer les résultats.

## GET /api/stats
Retourne les indicateurs : total, durée moyenne, durée médiane, durée maximale, durée cumulée, coupures actives, coupures par région, zone, source, statut, type, durée moyenne par région et points cartographiques.

## GET /api/map-points
Retourne les zones géolocalisées disponibles pour la carte : région, ville, zone, latitude, longitude, nombre de coupures, durée moyenne et dernière coupure.

## GET /api/data-quality
Retourne le rapport qualité des données : complétude moyenne, complétude par colonne, doublons, anomalies, score qualité et répartition des sources.

## GET /api/source-traceability
Retourne la traçabilité des sources : catalogue, URLs seedées, fichiers produits, tailles, nombres de lignes et répartition par type de source.

## GET /api/model-metrics
Retourne les métriques du modèle ML entraîné sur données réelles : lignes utilisées, distribution des classes, déséquilibre majorité/minorité, statistiques de durée, paramètres, MAE/RMSE/R2, accuracy, baseline, matrice de confusion, importance des variables et comparaison des variantes standard/balanced.

## GET /api/model-card
Retourne une fiche modèle prête pour le rapport : résumé, usage prévu, données utilisées, distribution des classes, déséquilibre des classes, statistiques de durée, résultats, comparaison des variantes, variables importantes, analyse des erreurs de test, fiabilité par niveau de confiance, limites et Markdown généré.

## GET /api/model-predictions
Retourne l'analyse des prédictions du jeu de test : MAE observée, accuracy de classification, fiabilité par niveau de confiance, pires erreurs de durée et erreurs de classification.

## POST /api/predict-duration
Retourne une prédiction de durée, la classe `courte`, `moyenne` ou `longue`, la confiance de cette classe, les probabilités par classe, le niveau de confiance et un message d'aide à la décision. Les champs d'entrée sont : région, ville, zone, type, mois, heure, jour, température, précipitation et irradiation solaire. Le champ optionnel `model_variant` accepte `standard` ou `balanced`.

## GET /api/pipeline-runs
Retourne les dernières exécutions du pipeline : nom, dates de début/fin, statut, lignes lues, insérées, rejetées et message d’erreur éventuel.

## GET /suivi
Affiche le suivi temps réel par région, ville, zone et statut, avec les coupures actives.

## GET /carte
Affiche la carte interactive des zones touchées et le tableau des points géolocalisés.

## POST /coupures
Ajoute une coupure depuis le formulaire HTML et génère des notifications simulées pour les abonnements correspondant à la zone.

## POST /signalements
Ajoute un signalement utilisateur.

## GET/POST /notifications
Affiche les abonnements et les notifications. Le formulaire permet de créer un abonnement par région, ville ou zone.

## GET /notifications/simuler
Génère des notifications simulées pour une coupure prévue ou en cours.

## GET /recommandations
Affiche des recommandations énergétiques personnalisées. Les paramètres `region` et `zone` permettent d’adapter les conseils à une zone donnée.

## GET /qualite
Affiche la page HTML de suivi de la qualité des données.

## GET /sources
Affiche la page HTML de traçabilité des sources, des URLs collectées et des fichiers produits.

## GET /modele
Affiche la page HTML des résultats du modèle prédictif ML.

## GET /modele/fiche
Affiche la fiche modèle ML prête pour le rapport.

## GET /modele/erreurs
Affiche l'analyse des erreurs du modèle sur le jeu de test.

## GET/POST /prediction
Affiche le formulaire de prédiction ML et le résultat estimé pour un scénario de coupure.

## GET /pipeline
Affiche la page HTML de traçabilité des exécutions du pipeline.
