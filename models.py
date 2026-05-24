from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()
class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(150), nullable=False)
    email =db.Column(db.String(100), unique=True, nullable=False)
    password_hash= db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='enseignant')
    def __repr__(self):
        return f'<User {self.nom}>'
class etudiants(db.Model):
    __tablename__='etudiants'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom=db.Column(db.String(50), nullable=False)
    classe=db.Column(db.String(50), nullable=False)
    num_etudiant=db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self):
        return f'<etudiant {self.nom} {self.prenom}>'
class Absence (db.Model):
    __tablename__='absences'
    id=db.Column(db.Integer, primary_key=True)
    etudiant_id=db.Column(db.Integer, db.ForeignKey('etudiants.id'), nullable=False)
    date_absence=db.Column(db.Date, nullable=False)
    matiere=db.Column(db.String(50), nullable=False)
    nb_heures=db.Column(db.Float, default=1.5)
    justifiee=db.Column(db.Boolean, default=False)
    motif=db.Column(db.Text)
    def __repr__(self):
        return f'<absence {self.etudiant_id} {self.date_absence}>'