from datetime import datetime
from extensions import db

class SourceDocument(db.Model):
    __tablename__ = 'source_documents'
    id_source = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(100), nullable=False)
    source_type = db.Column(db.String(50))
    url = db.Column(db.Text)
    date_collecte = db.Column(db.DateTime, default=datetime.utcnow)
    date_publication = db.Column(db.Date)
    titre = db.Column(db.Text)
    texte_original = db.Column(db.Text)
    fichier_local = db.Column(db.Text)
    niveau_confiance = db.Column(db.Float, default=0.5)

class Coupure(db.Model):
    __tablename__ = 'coupures'
    id_coupure = db.Column(db.Integer, primary_key=True)
    id_source = db.Column(db.Integer, db.ForeignKey('source_documents.id_source'), nullable=True)
    date_publication = db.Column(db.Date)
    date_debut = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    date_fin = db.Column(db.Date)
    heure_fin = db.Column(db.Time)
    duree_minutes = db.Column(db.Integer)
    annee = db.Column(db.Integer)
    mois = db.Column(db.Integer)
    jour_semaine = db.Column(db.String(30))
    periode_journee = db.Column(db.String(30))
    region = db.Column(db.String(100))
    province = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    zone = db.Column(db.String(150))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    type_coupure = db.Column(db.String(50))
    cause = db.Column(db.Text)
    statut = db.Column(db.String(50))
    source_name = db.Column(db.String(100))
    source_type = db.Column(db.String(50))
    url_source = db.Column(db.Text)
    niveau_confiance = db.Column(db.Float)
    niveau_impact = db.Column(db.String(50))
    temperature_max = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    irradiation_solaire = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Signalement(db.Model):
    __tablename__ = 'signalements'
    id_signalement = db.Column(db.Integer, primary_key=True)
    nom_signalant = db.Column(db.String(100))
    telephone = db.Column(db.String(30))
    region = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    zone = db.Column(db.String(150))
    date_signalement = db.Column(db.Date)
    heure_debut = db.Column(db.Time)
    heure_fin = db.Column(db.Time)
    description = db.Column(db.Text)
    statut_confirmation = db.Column(db.String(50), default='en_attente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Abonnement(db.Model):
    __tablename__ = 'abonnements'
    id_abonnement = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    contact = db.Column(db.String(120), nullable=False)
    canal = db.Column(db.String(50), default='web')
    region = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    zone = db.Column(db.String(150))
    actif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id_notification = db.Column(db.Integer, primary_key=True)
    id_coupure = db.Column(db.Integer, db.ForeignKey('coupures.id_coupure'), nullable=True)
    id_abonnement = db.Column(db.Integer, db.ForeignKey('abonnements.id_abonnement'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    canal = db.Column(db.String(50), default='web')
    destinataire = db.Column(db.String(120))
    statut_envoi = db.Column(db.String(50), default='simulée')
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)

class PipelineRun(db.Model):
    __tablename__ = 'pipeline_runs'
    id_run = db.Column(db.Integer, primary_key=True)
    pipeline_name = db.Column(db.String(120), nullable=False)
    date_start = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_end = db.Column(db.DateTime)
    status = db.Column(db.String(40), default='running', nullable=False)
    records_read = db.Column(db.Integer, default=0)
    records_inserted = db.Column(db.Integer, default=0)
    records_rejected = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
