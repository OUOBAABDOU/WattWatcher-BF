# Fiche modèle ML — WattWatcher BF

**Fichier métriques :** `data\processed\model_metrics_real.json`

## Usage prévu
Estimer la durée probable d’une coupure et classer le risque en courte, moyenne ou longue.

## Données utilisées
330 lignes réelles exploitables, dont 66 lignes de test.

## Distribution des classes
| Classe | Lignes |
| --- | --- |
| courte | 39 |
| longue | 117 |
| moyenne | 174 |

## Déséquilibre des classes
| Classe majoritaire | Lignes | Classe minoritaire | Lignes | Ratio |
| --- | --- | --- | --- | --- |
| moyenne | 174 | courte | 39 | 4.46 |

## Statistiques de durée
| Min | Médiane | Moyenne | Max |
| --- | --- | --- | --- |
| 60.0 | 240.0 | 226.09 | 480.0 |

## Résultats principaux
| Métrique | Valeur |
| --- | --- |
| MAE régression | 117.72 min |
| RMSE régression | 139.4 min |
| R2 régression | -0.135 |
| Accuracy classification | 0.515 |
| Accuracy baseline | 0.53 |

## Comparaison des variantes
| Variante | Class weight | MAE | Accuracy | Macro-F1 | Weighted-F1 |
| --- | --- | --- | --- | --- | --- |
| standard | none | 117.72 | 0.515 | 0.312 | 0.446 |
| balanced | balanced | 117.72 | 0.455 | 0.312 | 0.431 |

## Variables les plus importantes
| Variable | Importance |
| --- | --- |
| temperature_max | 0.2153 |
| irradiation_solaire | 0.208 |
| mois | 0.114 |
| precipitation | 0.101 |
| heure_num | 0.0984 |
| jour_num | 0.0954 |
| zone | 0.062 |
| type_coupure | 0.0432 |

## Analyse des erreurs de test
66 lignes de test analysées, MAE observée 117.72 min, 32 erreurs de classification.

### Fiabilite par niveau de confiance
| Niveau | Lignes | Correctes | Accuracy | Confiance moyenne |
| --- | --- | --- | --- | --- |
| faible | 4 | 2 | 0.5 | 0.43 |
| moyenne | 51 | 26 | 0.51 | 0.543 |
| élevée | 11 | 6 | 0.545 | 0.685 |

| Lieu | Durée réelle | Durée prédite | Erreur | Classe réelle | Classe prédite |
| --- | --- | --- | --- | --- | --- |
| Hauts-Bassins / Bobo-Dioulasso / Accart-Ville | 480.0 | 159.26 | 320.74 | longue | moyenne |
| Centre / Ouagadougou / Dassasgho | 480.0 | 161.28 | 318.72 | longue | moyenne |
| Sud-Ouest / Gaoua / Secteur 3 | 480.0 | 197.21 | 282.79 | longue | longue |

## Limites
Le volume de données réelles reste limité. Les prédictions exactes en minutes doivent rester indicatives et être confirmées par les sources terrain.

## Recommandation
Variante recommandée pour la classification : standard. Variante avec la meilleure MAE : standard.