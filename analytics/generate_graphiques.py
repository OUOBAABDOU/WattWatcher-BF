import sys
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine, text
import numpy as np

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))

from config import Config

# Configuration des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Créer le dossier de captures
CAPTURES_DIR = ROOT_DIR / "docs" / "captures"
CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

def get_db_connection():
    """Créer une connexion à la base de données PostgreSQL"""
    # Utiliser l'URL de connexion depuis Config
    db_url = Config.SQLALCHEMY_DATABASE_URI
    # Convertir postgresql+psycopg2:// en postgresql:// pour SQLAlchemy direct
    if db_url.startswith('postgresql+psycopg2://'):
        db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
    engine = create_engine(db_url)
    return engine

def fetch_data(query):
    """Exécuter une requête SQL et retourner un DataFrame"""
    engine = get_db_connection()
    try:
        df = pd.read_sql(query, engine)
        return df
    finally:
        engine.dispose()

def graphique_duree_moyenne_par_region():
    """Graphique : Durée moyenne des coupures par région"""
    query = """
    SELECT region, AVG(duree_minutes) as duree_moyenne, COUNT(*) as nb_coupures
    FROM coupures
    WHERE region IS NOT NULL AND duree_minutes IS NOT NULL
    GROUP BY region
    ORDER BY duree_moyenne DESC
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique duree moyenne par region")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(df['region'], df['duree_moyenne'], color='steelblue', alpha=0.8)
    ax.set_xlabel('Région', fontsize=12, fontweight='bold')
    ax.set_ylabel('Durée moyenne (minutes)', fontsize=12, fontweight='bold')
    ax.set_title('Durée moyenne des coupures par région', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticklabels(df['region'], rotation=45, ha='right')
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_duree_moyenne_region.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_duree_moyenne_region.png")

def graphique_distribution_durees():
    """Graphique : Distribution des durées de coupures"""
    query = """
    SELECT duree_minutes
    FROM coupures
    WHERE duree_minutes IS NOT NULL AND duree_minutes > 0
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique distribution des durees")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(df['duree_minutes'], bins=30, color='coral', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Durée (minutes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_title('Distribution des durées de coupures', fontsize=14, fontweight='bold', pad=20)
    ax.axvline(df['duree_minutes'].mean(), color='red', linestyle='--', linewidth=2, label=f'Moyenne: {df["duree_minutes"].mean():.0f} min')
    ax.axvline(df['duree_minutes'].median(), color='green', linestyle='--', linewidth=2, label=f'Médiane: {df["duree_minutes"].median():.0f} min')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_distribution_durees.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_distribution_durees.png")

def graphique_coupures_par_jour_semaine():
    """Graphique : Coupures par jour de la semaine"""
    query = """
    SELECT jour_semaine, COUNT(*) as nb_coupures
    FROM coupures
    WHERE jour_semaine IS NOT NULL
    GROUP BY jour_semaine
    ORDER BY 
        CASE jour_semaine
            WHEN 'Lundi' THEN 1
            WHEN 'Mardi' THEN 2
            WHEN 'Mercredi' THEN 3
            WHEN 'Jeudi' THEN 4
            WHEN 'Vendredi' THEN 5
            WHEN 'Samedi' THEN 6
            WHEN 'Dimanche' THEN 7
            ELSE 8
        END
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique coupures par jour de semaine")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['jour_semaine'], df['nb_coupures'], color='mediumseagreen', alpha=0.8)
    ax.set_xlabel('Jour de la semaine', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_title('Coupures par jour de la semaine', fontsize=14, fontweight='bold', pad=20)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_coupures_jour_semaine.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_coupures_jour_semaine.png")

def graphique_coupures_par_periode_journee():
    """Graphique : Coupures par période de la journée"""
    query = """
    SELECT periode_journee, COUNT(*) as nb_coupures
    FROM coupures
    WHERE periode_journee IS NOT NULL
    GROUP BY periode_journee
    ORDER BY nb_coupures DESC
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique coupures par periode journee")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = ax.bar(df['periode_journee'], df['nb_coupures'], color=colors[:len(df)], alpha=0.8)
    ax.set_xlabel('Période de la journée', fontsize=12, fontweight='bold')
    ax.set_ylabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_title('Coupures par période de la journée', fontsize=14, fontweight='bold', pad=20)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_coupures_periode_journee.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_coupures_periode_journee.png")

def graphique_coupures_par_cause():
    """Graphique : Coupures par cause"""
    query = """
    SELECT cause, COUNT(*) as nb_coupures
    FROM coupures
    WHERE cause IS NOT NULL AND cause != ''
    GROUP BY cause
    ORDER BY nb_coupures DESC
    LIMIT 10
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique coupures par cause")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df['cause'], df['nb_coupures'], color='purple', alpha=0.7)
    ax.set_xlabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cause', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 des causes de coupures', fontsize=14, fontweight='bold', pad=20)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_coupures_par_cause.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_coupures_par_cause.png")

def graphique_evolution_annuelle():
    """Graphique : Évolution annuelle des coupures"""
    query = """
    SELECT annee, COUNT(*) as nb_coupures, AVG(duree_minutes) as duree_moyenne
    FROM coupures
    WHERE annee IS NOT NULL
    GROUP BY annee
    ORDER BY annee
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique evolution annuelle")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Graphique 1 : Nombre de coupures par année
    ax1.plot(df['annee'], df['nb_coupures'], marker='o', linewidth=2, markersize=8, color='blue')
    ax1.set_xlabel('Année', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax1.set_title('Évolution annuelle du nombre de coupures', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2 : Durée moyenne par année
    ax2.plot(df['annee'], df['duree_moyenne'], marker='s', linewidth=2, markersize=8, color='red')
    ax2.set_xlabel('Année', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Durée moyenne (minutes)', fontsize=12, fontweight='bold')
    ax2.set_title('Évolution annuelle de la durée moyenne', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_evolution_annuelle.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_evolution_annuelle.png")

def graphique_top10_villes():
    """Graphique : Top 10 des villes les plus touchées"""
    query = """
    SELECT ville, COUNT(*) as nb_coupures, AVG(duree_minutes) as duree_moyenne
    FROM coupures
    WHERE ville IS NOT NULL AND ville != ''
    GROUP BY ville
    ORDER BY nb_coupures DESC
    LIMIT 10
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique top 10 villes")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df['ville'], df['nb_coupures'], color='darkorange', alpha=0.8)
    ax.set_xlabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ville', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 des villes les plus touchées', fontsize=14, fontweight='bold', pad=20)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_top10_villes.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_top10_villes.png")

def graphique_boxplot_duree_type():
    """Graphique : Box plot des durées par type de coupure"""
    query = """
    SELECT type_coupure, duree_minutes
    FROM coupures
    WHERE type_coupure IS NOT NULL AND duree_minutes IS NOT NULL AND duree_minutes > 0
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique boxplot duree par type")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    types = df['type_coupure'].unique()
    data_to_plot = [df[df['type_coupure'] == t]['duree_minutes'] for t in types]
    
    bp = ax.boxplot(data_to_plot, patch_artist=True)
    ax.set_xticklabels(types)
    
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    ax.set_xlabel('Type de coupure', fontsize=12, fontweight='bold')
    ax.set_ylabel('Durée (minutes)', fontsize=12, fontweight='bold')
    ax.set_title('Distribution des durées par type de coupure', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticklabels(types, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_boxplot_duree_type.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_boxplot_duree_type.png")

def graphique_heatmap_region_mois():
    """Graphique : Heatmap des coupures par région et mois"""
    query = """
    SELECT region, mois, COUNT(*) as nb_coupures
    FROM coupures
    WHERE region IS NOT NULL AND mois IS NOT NULL
    GROUP BY region, mois
    ORDER BY region, mois
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique heatmap region mois")
        return
    
    # Créer une matrice pivot
    pivot_df = df.pivot(index='region', columns='mois', values='nb_coupures').fillna(0)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(pivot_df, annot=True, fmt='g', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Nombre de coupures'})
    ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
    ax.set_ylabel('Région', fontsize=12, fontweight='bold')
    ax.set_title('Heatmap des coupures par région et mois', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_heatmap_region_mois.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_heatmap_region_mois.png")

def graphique_coupures_par_province():
    """Graphique : Coupures par province"""
    query = """
    SELECT province, COUNT(*) as nb_coupures
    FROM coupures
    WHERE province IS NOT NULL AND province != ''
    GROUP BY province
    ORDER BY nb_coupures DESC
    LIMIT 15
    """
    df = fetch_data(query)
    
    if df.empty:
        print("WARNING: Pas de donnees pour le graphique coupures par province")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(df['province'], df['nb_coupures'], color='teal', alpha=0.8)
    plt.gca().invert_yaxis()
    ax.set_xlabel('Nombre de coupures', fontsize=12, fontweight='bold')
    ax.set_ylabel('Province', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 des provinces les plus touchées', fontsize=14, fontweight='bold', pad=20)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(CAPTURES_DIR / 'graphique_coupures_par_province.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("OK: Graphique cree : graphique_coupures_par_province.png")

def main():
    """Générer tous les graphiques"""
    print("=" * 60)
    print("Génération des graphiques supplémentaires")
    print("=" * 60)
    print()
    
    graphiques = [
        ("Durée moyenne par région", graphique_duree_moyenne_par_region),
        ("Distribution des durées", graphique_distribution_durees),
        ("Coupures par jour de semaine", graphique_coupures_par_jour_semaine),
        ("Coupures par période journée", graphique_coupures_par_periode_journee),
        ("Coupures par cause", graphique_coupures_par_cause),
        ("Évolution annuelle", graphique_evolution_annuelle),
        ("Top 10 villes", graphique_top10_villes),
        ("Boxplot durée par type", graphique_boxplot_duree_type),
        ("Heatmap région x mois", graphique_heatmap_region_mois),
        ("Coupures par province", graphique_coupures_par_province),
    ]
    
    for nom, func in graphiques:
        print(f"Generation : {nom}...")
        try:
            func()
        except Exception as e:
            print(f"ERROR : {nom} - {e}")
        print()
    
    print("=" * 60)
    print(f"Graphiques sauvegardés dans : {CAPTURES_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
