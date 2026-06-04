from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Etudiant, Absence
from sqlalchemy import func

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def index():
    total_etudiants = Etudiant.query.count()
    total_absences = Absence.query.count()
    total_heures = db.session.query(func.sum(Absence.nb_heures)).scalar() or 0
    absences_justifiees = Absence.query.filter_by(justifiee=True).count()
    absences_non_justifiees = Absence.query.filter_by(justifiee=False).count()

    if total_absences > 0:
        taux_justifiees = round((absences_justifiees / total_absences) * 100, 1)
        taux_non_justifiees = round((absences_non_justifiees / total_absences) * 100, 1)
    else:
        taux_justifiees = 0
        taux_non_justifiees = 0

    absences_par_classe = db.session.query(
        Etudiant.classe,
        func.count(Absence.id)
    ).join(Absence).group_by(Etudiant.classe).all()

    classe_max = db.session.query(
        Etudiant.classe,
        func.sum(Absence.nb_heures).label('total_heures')
    ).join(Absence).group_by(Etudiant.classe).order_by(func.sum(Absence.nb_heures).desc()).first()

    etudiant_max = db.session.query(
        Etudiant,
        func.sum(Absence.nb_heures).label('total_heures')
    ).join(Absence).group_by(Etudiant.id).order_by(func.sum(Absence.nb_heures).desc()).first()

    return render_template('dashboard.html',
                           total_etudiants=total_etudiants,
                           total_absences=total_absences,
                           total_heures=total_heures,
                           absences_justifiees=absences_justifiees,
                           absences_non_justifiees=absences_non_justifiees,
                           taux_justifiees=taux_justifiees,
                           taux_non_justifiees=taux_non_justifiees,
                           absences_par_classe=absences_par_classe,
                           classe_max=classe_max,
                           etudiant_max=etudiant_max)