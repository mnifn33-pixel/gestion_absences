from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import auth
app = Flask(__name__)
app.config['SECRET_KEY']= 'admin_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absences.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from routes import auth, etudiants, absences, dashboard
app.register_blueprint(auth.bp)
app.register_blueprint(etudiants.bp)
app.register_blueprint(absences.bp)
app.register_blueprint(dashboard.bp)
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
    
    
