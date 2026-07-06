from database.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    patient = db.relationship("Patient", backref="user", uselist=False)
    doctor = db.relationship("Doctor", backref="user", uselist=False)
    nurse = db.relationship("Nurse", backref="user", uselist=False)