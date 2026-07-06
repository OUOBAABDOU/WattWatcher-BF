"""Scraping des articles médias et extraction de coupures structurées."""
import argparse
import csv
import os
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import create_engine

KEYWORDS = ['SONABEL', 'coupure', 'électricité', 'courant', 'fourniture', 'perturbation', 'suspension']
REGIONS = ['Boucle du Mouhoun', 'Cascades', 'Centre', 'Centre-Est', 'Centre-Nord', 'Centre-Ouest', 'Centre-Sud', 'Est', 'Hauts-Bassins', 'Nord', 'Plateau-Central', 'Sahel', 'Sud-Ouest']
KNOWN_CITIES = ['Ouagadougou', 'Bobo-Dioulasso', 'Koudougou', 'Ouahigouya', 'Fada', 'Banfora', 'Dédougou', 'Kaya', 'Gaoua', 'Tanghin', 'Gounghin']
LOCATION_COORDS = {
    'Ouagadougou': (12.3714, -1.5197, 'Centre'),
    'Tanghin': (12.394, -1.525, 'Centre'),
    'Gounghin': (12.358, -1.543, 'Centre'),
}


def fetch_html(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 WattWatcherBF academic project'}, timeout=30)
    r.raise_for_status()
    return r.text


def extract_text(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1') or soup.find('title')
    paragraphs = [p.get_text(' ', strip=True) for p in soup.find_all('p')]
    return {'titre': title.get_text(' ', strip=True) if title else '', 'texte': ' '.join(paragraphs)}


def extract_hours(text):
    patterns = [
        r"(\d{1,2})\s*h\s*(\d{0,2})\s*(?:à|-|jusqu.?à)\s*(\d{1,2})\s*h\s*(\d{0,2})",
        r"de\s*(\d{1,2})[:h](\d{0,2})\s*(?:à|-|jusqu.?à)\s*(\d{1,2})[:h](\d{0,2})",
    ]
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text, flags=re.I))
    return list(dict.fromkeys(matches))


def normalize_time(hour, minute):
    minute = minute or '00'
    return f'{int(hour):02d}:{int(minute):02d}'


def extract_date(text):
    iso = re.search(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b", text)
    if iso:
        return f'{iso.group(1)}-{int(iso.group(2)):02d}-{int(iso.group(3)):02d}'
    fr = re.search(r"\b(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(20\d{2})\b", text, flags=re.I)
    months = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}
    if fr:
        return f'{fr.group(3)}-{months[fr.group(2).lower()]:02d}-{int(fr.group(1)):02d}'
    return date.today().isoformat()


def first_known(text, values):
    for value in values:
        if re.search(rf"\b{re.escape(value)}\b", text, flags=re.I):
            return value
    return ''


def extract_zones(text):
    candidates = re.findall(r"(?:zone(?:s)?|quartier(?:s)?|secteur(?:s)?)\s+(?:de\s+)?([A-ZÉÈÀÂÎÔÛÇ][\wÉÈÀÂÎÔÛÇéèàâîôûç' -]{2,80})", text)
    cleaned = []
    for item in candidates:
        item = re.split(r"[,.;:]|\sainsi\s", item, flags=re.I)[0].strip()
        item = re.split(r"\s+de\s+\d{1,2}\s*h|\s+\d{1,2}\s*h", item, flags=re.I)[0].strip()
        if re.search(r"société|nationale|électricité|courant|fourniture", item, flags=re.I):
            continue
        parts = [part.strip(" -'") for part in re.split(r"\set\s|/", item, flags=re.I)]
        for part in parts:
            if part and part not in cleaned:
                cleaned.append(part)
    return cleaned


def coordinates_for(city, zone):
    for key in (zone, city):
        if key in LOCATION_COORDS:
            lat, lon, region = LOCATION_COORDS[key]
            return lat, lon, region
    return '', '', ''


def extract_structured_rows(item, data):
    text = f"{data.get('titre', '')} {data.get('texte', '')}"
    hours = extract_hours(text)
    if not hours:
        return []
    publication_date = extract_date(text)
    region = first_known(text, REGIONS) or 'Non précisée'
    city = first_known(text, KNOWN_CITIES) or 'Non précisée'
    zones = extract_zones(text) or [city]
    rows = []
    for start_h, start_m, end_h, end_m in hours:
        start_time = normalize_time(start_h, start_m)
        end_time = normalize_time(end_h, end_m)
        start_dt = datetime.strptime(f'{publication_date} {start_time}', '%Y-%m-%d %H:%M')
        end_dt = datetime.strptime(f'{publication_date} {end_time}', '%Y-%m-%d %H:%M')
        duration = max(0, int((end_dt - start_dt).total_seconds() // 60))
        for zone in zones:
            latitude, longitude, detected_region = coordinates_for(city, zone)
            rows.append({
                'date_publication': publication_date,
                'date_debut': publication_date,
                'heure_debut': start_time,
                'date_fin': publication_date,
                'heure_fin': end_time,
                'duree_minutes': duration,
                'annee': int(publication_date[:4]),
                'mois': int(publication_date[5:7]),
                'jour_semaine': start_dt.strftime('%A'),
                'periode_journee': 'matin' if int(start_h) < 12 else 'après-midi',
                'region': detected_region or region,
                'province': '',
                'ville': city,
                'zone': zone,
                'latitude': latitude,
                'longitude': longitude,
                'type_coupure': 'prévue',
                'cause': 'Communiqué ou article collecté automatiquement',
                'statut': 'prévue',
                'source_name': item.get('titre') or item.get('type_source') or 'Source web',
                'source_type': item.get('type_source') or 'media',
                'url_source': item.get('url'),
                'niveau_confiance': 0.65,
                'niveau_impact': 'moyen',
                'temperature_max': '',
                'precipitation': '',
                'irradiation_solaire': '',
            })
    return rows


def dedupe_rows(rows):
    seen = set()
    unique = []
    for row in rows:
        key = (row['date_debut'], row['heure_debut'], row['heure_fin'], row['ville'], row['zone'], row['url_source'])
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def write_csv(path, rows, fieldnames):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_structured_rows(rows):
    if not rows:
        return 0
    load_dotenv()
    database_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5433/wattwatcher_db')
    engine = create_engine(database_url)
    pd.DataFrame(rows).to_sql('coupures', engine, if_exists='append', index=False, method='multi')
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', default='data/raw/url_seeds_sonabel_medias.csv')
    parser.add_argument('--out', default='data/raw/medias/articles_collectes.csv')
    parser.add_argument('--structured-out', default='data/raw/medias/coupures_structurees.csv')
    parser.add_argument('--load-db', action='store_true')
    args = parser.parse_args()

    raw_rows = []
    structured_rows = []
    with open(args.seeds, encoding='utf-8') as f:
        for item in csv.DictReader(f):
            try:
                data = extract_text(fetch_html(item['url']))
                text = data['titre'] + ' ' + data['texte']
                if any(k.upper() in text.upper() for k in KEYWORDS):
                    raw_rows.append({**item, **data, 'heures_detectees': str(extract_hours(data['texte'])), 'statut_collecte': 'ok'})
                    structured_rows.extend(extract_structured_rows(item, data))
            except Exception as exc:
                raw_rows.append({**item, 'titre': '', 'texte': '', 'heures_detectees': '', 'statut_collecte': f'erreur: {exc}'})

    structured_rows = dedupe_rows(structured_rows)
    write_csv(args.out, raw_rows, ['titre', 'url', 'type_source', 'texte', 'heures_detectees', 'statut_collecte'])
    structured_fields = ['date_publication', 'date_debut', 'heure_debut', 'date_fin', 'heure_fin', 'duree_minutes', 'annee', 'mois', 'jour_semaine', 'periode_journee', 'region', 'province', 'ville', 'zone', 'latitude', 'longitude', 'type_coupure', 'cause', 'statut', 'source_name', 'source_type', 'url_source', 'niveau_confiance', 'niveau_impact', 'temperature_max', 'precipitation', 'irradiation_solaire']
    write_csv(args.structured_out, structured_rows, structured_fields)
    loaded = load_structured_rows(structured_rows) if args.load_db else 0
    print(f'{len(raw_rows)} article(s) collecté(s), {len(structured_rows)} coupure(s) structurée(s), {loaded} chargée(s) en base.')


if __name__ == '__main__':
    main()
