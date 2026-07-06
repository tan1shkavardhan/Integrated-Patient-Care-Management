from flask import Blueprint, render_template, request, redirect

from database.db import db
from models.patient import Patient

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/patients")
def list_patients():

    patients = Patient.query.all()

    return render_template(
        "patient/list.html",
        patients=patients
    )


@patient_bp.route("/patients/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        form = request.form

        patient = Patient(
            fullname=form["fullname"],
            age=form["age"],
            gender=form["gender"],
            contact=form["contact"],
            address=form["address"],
            blood_group=form["blood_group"]
        )

        db.session.add(patient)
        db.session.commit()

        return redirect("/patients")

    return render_template("patient/add.html")


@patient_bp.route("/patients/profile/<int:id>")
def patient_profile(id):

    patient = Patient.query.get_or_404(id)

    return render_template(
        "patient/profile.html",
        patient=patient
    )


@patient_bp.route("/patients/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        form = request.form

        patient.fullname = form["fullname"]
        patient.age = form["age"]
        patient.gender = form["gender"]
        patient.contact = form["contact"]
        patient.address = form["address"]
        patient.blood_group = form["blood_group"]

        db.session.commit()

        return redirect("/patients")

    return render_template(
        "patient/edit.html",
        patient=patient
    )


@patient_bp.route("/patients/delete/<int:id>")
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect("/patients")