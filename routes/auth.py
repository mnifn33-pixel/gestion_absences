from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

bp = Blueprint('auth', __name__)

CODE_ADMIN = '2024'
CODE_ADMINISTRATION ='2025'
CODE_ENSEIGNANT = '2026'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        password = request.form['password']
        code = request.form['code_secret']

        if code == CODE_ADMIN:
            role = 'admin'
        elif code == CODE_ENSEIGNANT:
            role = 'enseignant'
        else:
            flash('Code secret incorrect !', 'danger')
            return redirect(url_for('auth.register'))

        user_existant = User.query.filter_by(email=email).first()
        if user_existant:
            flash('Cet email existe déjà !', 'danger')
            return redirect(url_for('auth.register'))

        nouveau_user = User(
            nom=nom,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(nouveau_user)
        db.session.commit()
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')
