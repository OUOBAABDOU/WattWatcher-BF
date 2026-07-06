CREATE TABLE IF NOT EXISTS source_documents (
    id_source SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50),
    url TEXT,
    date_collecte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_publication DATE,
    titre TEXT,
    texte_original TEXT,
    fichier_local TEXT,
    niveau_confiance NUMERIC(3,2)
);

CREATE TABLE IF NOT EXISTS coupures (
    id_coupure SERIAL PRIMARY KEY,
    id_source INT REFERENCES source_documents(id_source),
    date_publication DATE,
    date_debut DATE NOT NULL,
    heure_debut TIME NOT NULL,
    date_fin DATE,
    heure_fin TIME,
    duree_minutes INT,
    annee INT,
    mois INT,
    jour_semaine VARCHAR(30),
    periode_journee VARCHAR(30),
    region VARCHAR(100),
    province VARCHAR(100),
    ville VARCHAR(100),
    zone VARCHAR(150),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    type_coupure VARCHAR(50),
    cause TEXT,
    statut VARCHAR(50),
    source_name VARCHAR(100),
    source_type VARCHAR(50),
    url_source TEXT,
    niveau_confiance NUMERIC(3,2),
    niveau_impact VARCHAR(50),
    temperature_max NUMERIC(5,2),
    precipitation NUMERIC(8,2),
    irradiation_solaire NUMERIC(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS signalements (
    id_signalement SERIAL PRIMARY KEY,
    nom_signalant VARCHAR(100),
    telephone VARCHAR(30),
    region VARCHAR(100),
    ville VARCHAR(100),
    zone VARCHAR(150),
    date_signalement DATE,
    heure_debut TIME,
    heure_fin TIME,
    description TEXT,
    statut_confirmation VARCHAR(50) DEFAULT 'en_attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS abonnements (
    id_abonnement SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    contact VARCHAR(120) NOT NULL,
    canal VARCHAR(50) DEFAULT 'web',
    region VARCHAR(100),
    ville VARCHAR(100),
    zone VARCHAR(150),
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
    id_notification SERIAL PRIMARY KEY,
    id_coupure INT REFERENCES coupures(id_coupure),
    id_abonnement INT REFERENCES abonnements(id_abonnement),
    message TEXT NOT NULL,
    canal VARCHAR(50),
    destinataire VARCHAR(120),
    statut_envoi VARCHAR(50),
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommandations (
    id_recommandation SERIAL PRIMARY KEY,
    titre VARCHAR(150),
    description TEXT,
    type_source_energie VARCHAR(80),
    condition_application VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id_run SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(120) NOT NULL,
    date_start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_end TIMESTAMP,
    status VARCHAR(40) NOT NULL DEFAULT 'running',
    records_read INT DEFAULT 0,
    records_inserted INT DEFAULT 0,
    records_rejected INT DEFAULT 0,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_coupures_date ON coupures(date_debut);
CREATE INDEX IF NOT EXISTS idx_coupures_region ON coupures(region);
CREATE INDEX IF NOT EXISTS idx_coupures_zone ON coupures(zone);

CREATE INDEX IF NOT EXISTS idx_abonnements_region ON abonnements(region);
CREATE INDEX IF NOT EXISTS idx_notifications_date ON notifications(date_envoi);
CREATE INDEX IF NOT EXISTS idx_pipeline_runs_date ON pipeline_runs(date_start);
