from flask import Flask
from models import db
app = Flask(__name__)
app.config['SECRET_KEY']= 'admin_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absences.db'
db.init_app(app)
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
    
