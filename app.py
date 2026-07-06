from flask import Flask

from config import Config

from database.db import db

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.nurse import Nurse
from models.appointment import Appointment

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.patient import patient_bp
from routes.doctor import doctor_bp
from routes.nurse import nurse_bp
from routes.appointment import appointment_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(nurse_bp)
app.register_blueprint(appointment_bp)

if __name__ == "__main__":
    app.run(debug=True)