from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import db

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.nurse import Nurse

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect("/login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        form = request.form

        user = User(
            fullname=form["fullname"],
            email=form["email"],
            phone=form["phone"],
            password=generate_password_hash(form["password"]),
            role=form["role"]
        )

        db.session.add(user)
        db.session.flush()

        if form["role"] == "Patient":

            patient = Patient(
                user_id=user.id,
                age=form["age"],
                gender=form["gender"],
                blood_group=form["blood_group"],
                address=form["address"]
            )

            db.session.add(patient)

        elif form["role"] == "Doctor":

            doctor = Doctor(
                user_id=user.id,
                specialization=form["specialization"],
                qualification=form["qualification"],
                department=form["doctor_department"],
                available_time=form["available_time"]
            )

            db.session.add(doctor)

        elif form["role"] == "Nurse":

            nurse = Nurse(
                user_id=user.id,
                department=form["nurse_department"],
                shift=form["shift"]
            )

            db.session.add(nurse)

        db.session.commit()

        return redirect("/login")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        form = request.form

        user = User.query.filter_by(
            email=form["email"]
        ).first()

        if (
            user
            and user.role == form["role"]
            and check_password_hash(
                user.password,
                form["password"]
            )
        ):

            session["user"] = user.fullname
            session["role"] = user.role
            session["user_id"] = user.id

            if user.role == "Admin":
                return redirect("/admin")

            elif user.role == "Doctor":
                return redirect("/doctor")

            elif user.role == "Nurse":
                return redirect("/nurse")

            return redirect("/patient")

        return "Invalid Email or Password"

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")