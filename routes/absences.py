from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Absence, Etudiant
from datetime import datetime

bp = Blueprint('absences', __name__)

@bp.route('/absences/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if request.method == 'POST':
        if current_user.role == 'enseignant':
            num_etudiant = request.form['num_etudiant']
            etudiant = Etudiant.query.filter_by(num_etudiant=num_etudiant).first()
            if not etudiant:
                flash('Numéro étudiant introuvable !', 'danger')
                return redirect(url_for('absences.ajouter'))
            etudiant_id = etudiant.id
        else:
            etudiant_id = request.form['etudiant_id']

        date_absence = datetime.strptime(request.form['date_absence'], '%Y-%m-%d').date()
        matiere = request.form['matiere']
        nb_heures = float(request.form['nb_heures'])
        justifiee = True if request.form.get('justifiee') else False
        motif = request.form.get('motif', '')

        absence = Absence(
            etudiant_id=etudiant_id,
            date_absence=date_absence,
            matiere=matiere,
            nb_heures=nb_heures,
            justifiee=justifiee,
            motif=motif
        )
        db.session.add(absence)
        db.session.commit()
        flash('Absence ajoutée avec succès !', 'success')
        return redirect(url_for('absences.ajouter'))

    etudiants = Etudiant.query.all() if current_user.role != 'enseignant' else None
    return render_template('absences/ajouter.html', etudiants=etudiants)


@bp.route('/absences/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier(id):
    absence = Absence.query.get_or_404(id)
    etudiants = Etudiant.query.all() if current_user.role != 'enseignant' else None
    if request.method == 'POST':
        if current_user.role == 'enseignant':
            num_etudiant = request.form['num_etudiant']
            etudiant = Etudiant.query.filter_by(num_etudiant=num_etudiant).first()
            if not etudiant:
                flash('Numéro étudiant introuvable !', 'danger')
                return redirect(url_for('absences.modifier', id=id))
            absence.etudiant_id = etudiant.id
        else:
            absence.etudiant_id = request.form['etudiant_id']

        absence.date_absence = datetime.strptime(request.form['date_absence'], '%Y-%m-%d').date()
        absence.matiere = request.form['matiere']
        absence.nb_heures = float(request.form['nb_heures'])
        absence.justifiee = True if request.form.get('justifiee') else False
        absence.motif = request.form.get('motif', '')
        db.session.commit()
        flash('Absence modifiée avec succès !', 'success')
        return redirect(url_for('etudiants.liste'))
    return render_template('absences/modifier.html', absence=absence, etudiants=etudiants)


@bp.route('/absences/supprimer/<int:id>')
@login_required
def supprimer(id):
    absence = Absence.query.get_or_404(id)
    db.session.delete(absence)
    db.session.commit()
    flash('Absence supprimée avec succès !', 'success')
    return redirect(url_for('etudiants.liste'))