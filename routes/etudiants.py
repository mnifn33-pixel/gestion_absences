from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Etudiant, Absence
import openpyxl

bp = Blueprint('etudiants', __name__)

@bp.route('/etudiants')
@login_required
def liste():
    if current_user.role not in ['admin', 'administration']:
        flash('Accès refusé !', 'danger')
        return redirect(url_for('dashboard.index'))
    classe = request.args.get('classe')
    recherche = request.args.get('recherche')
    num_etudiant = request.args.get('num_etudiant')
    etudiant_id = request.args.get('id')

    query = Absence.query.join(Etudiant)
    if etudiant_id:
        query = query.filter(Etudiant.id == etudiant_id)
    if classe:
        query = query.filter(Etudiant.classe == classe)
    if num_etudiant:
        query = query.filter(Etudiant.num_etudiant == num_etudiant)
    if recherche:
        query = query.filter(
            (Etudiant.nom.ilike(f'%{recherche}%')) |
            (Etudiant.prenom.ilike(f'%{recherche}%')) |
            ((Etudiant.nom + ' ' + Etudiant.prenom).ilike(f'%{recherche}%')) |
            ((Etudiant.prenom + ' ' + Etudiant.nom).ilike(f'%{recherche}%'))
        )
    absences = query.order_by(Absence.date_absence.desc()).all()
    classes = db.session.query(Etudiant.classe).distinct().all()
    classes = [c[0] for c in classes]

    return render_template('etudiants/liste.html',
                           absences=absences,
                           classes=classes,
                           classe=classe,
                           recherche=recherche,
                           num_etudiant=num_etudiant,
                           etudiant_id=etudiant_id)

@bp.route('/etudiants/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if current_user.role not in ['admin', 'administration']:
        flash('Accès refusé !', 'danger')
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        classe = request.form['classe']
        num_etudiant = request.form['num_etudiant']

        etudiant_existant = Etudiant.query.filter_by(num_etudiant=num_etudiant).first()
        if etudiant_existant:
            flash('Ce numéro étudiant existe déjà !', 'danger')
            return redirect(url_for('etudiants.ajouter'))

        etudiant = Etudiant(nom=nom, prenom=prenom, classe=classe, num_etudiant=num_etudiant)
        db.session.add(etudiant)
        db.session.commit()
        flash('Étudiant ajouté avec succès !', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('etudiants/ajouter.html')
@bp.route('/etudiants/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier(id):
    if current_user.role not in ['admin', 'administration']:
        flash('Accès refusé !', 'danger')
        return redirect(url_for('dashboard.index'))
    etudiant = Etudiant.query.get_or_404(id)
    if request.method == 'POST':
        etudiant.nom = request.form['nom']
        etudiant.prenom = request.form['prenom']
        etudiant.classe = request.form['classe']
        etudiant.num_etudiant = request.form['num_etudiant']
        db.session.commit()
        flash('Étudiant modifié avec succès !', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('etudiants/modifier.html', etudiant=etudiant)

@bp.route('/etudiants/supprimer/<int:id>')
@login_required
def supprimer(id):
    if current_user.role not in ['admin', 'administration']:
        flash('Accès refusé !', 'danger')
        return redirect(url_for('dashboard.index'))
    etudiant = Etudiant.query.get_or_404(id)
    db.session.delete(etudiant)
    db.session.commit()
    flash('Étudiant supprimé avec succès !', 'success')
    return redirect(url_for('dashboard.index'))

@bp.route('/etudiants/importer', methods=['GET', 'POST'])
@login_required
def importer():
    if current_user.role not in ['admin', 'administration']:
        flash('Accès refusé !', 'danger')
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        fichier = request.files['fichier']
        if not fichier:
            flash('Aucun fichier sélectionné !', 'danger')
            return redirect(url_for('etudiants.importer'))

        wb = openpyxl.load_workbook(fichier)
        ws = wb.active
        count = 0