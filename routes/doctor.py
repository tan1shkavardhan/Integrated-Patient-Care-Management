from flask import Blueprint, render_template, request, redirect
from database.db import db
from models.doctor import Doctor

doctor_bp = Blueprint("doctor", __name__)


@doctor_bp.route("/doctors")
def list_doctors():
    doctors = Doctor.query.all()
    return render_template("doctor/list.html", doctors=doctors)


@doctor_bp.route("/doctors/add", methods=["GET", "POST"])
def add_doctor():

    if request.method == "POST":
        form = request.form

        doctor = Doctor(
            name=form["name"],
            specialization=form["specialization"],
            qualification=form["qualification"],
            department=form["department"],
            contact=form["contact"],
            email=form["email"],
            available_time=form["available_time"]
        )

        db.session.add(doctor)
        db.session.commit()

        return redirect("/doctors")

    return render_template("doctor/add.html")


@doctor_bp.route("/doctors/edit/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":
        form = request.form

        doctor.name = form["name"]
        doctor.specialization = form["specialization"]
        doctor.qualification = form["qualification"]
        doctor.department = form["department"]
        doctor.contact = form["contact"]
        doctor.email = form["email"]
        doctor.available_time = form["available_time"]

        db.session.commit()

        return redirect("/doctors")

    return render_template("doctors/edit.html", doctor=doctor)


@doctor_bp.route("/doctors/delete/<int:id>")
def delete_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    db.session.delete(doctor)
    db.session.commit()

    return redirect("/doctors")