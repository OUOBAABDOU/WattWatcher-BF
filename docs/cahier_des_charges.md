# Cahier des charges — WattWatcher BF

## Titre
Application de suivi des coupures d’électricité et de gestion énergétique au Burkina Faso.

## Problématique
Les coupures d’électricité perturbent les activités des ménages, entreprises, commerces et services. Les informations disponibles sont dispersées entre communiqués officiels, médias et signalements. Le projet vise à centraliser ces données, les analyser et fournir des informations utiles à la planification énergétique.

## Objectif général
Développer une application web qui collecte, stocke, analyse et visualise les données relatives aux coupures d’électricité afin d’aider les utilisateurs à mieux anticiper et gérer leur consommation énergétique.

## Objectifs spécifiques
- Collecter les données de coupures depuis plusieurs sources.
- Extraire automatiquement les informations utiles depuis texte, PDF ou image.
- Stocker les informations dans PostgreSQL.
- Nettoyer et transformer les données avec Python/Pandas.
- Produire des statistiques et visualisations.
- Mettre en place un tableau de bord interactif.
- Proposer une prédiction simple de la durée probable d’une coupure.
- Générer des recommandations énergétiques.
- Permettre aux utilisateurs de signaler une coupure.

## Fonctionnalités
- Liste des coupures.
- Ajout manuel d’une coupure.
- Tableau de bord.
- Graphiques par région, zone, année et durée.
- Signalements utilisateurs.
- Notifications simulées.
- Recommandations énergétiques.
- Scraping, OCR et extraction PDF.
- Croisement avec météo et irradiation solaire.
- Prédiction de durée.

## Technologies
Flask, PostgreSQL, Pandas, NumPy, Scikit-learn, Requests, BeautifulSoup, pdfplumber, pytesseract, Plotly, Docker.
