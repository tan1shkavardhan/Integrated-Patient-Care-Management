from flask import Blueprint, render_template, request, redirect
from datetime import datetime

from database.db import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/appointments")
def list_appointments():

    appointments = Appointment.query.all()

    return render_template(
        "appointment/list.html",
        appointments=appointments
    )


@appointment_bp.route("/appointments/add", methods=["GET", "POST"])
def add_appointment():

    if request.method == "POST":

        form = request.form

        appointment = Appointment(
            patient_id=form["patient_id"],
            doctor_id=form["doctor_id"],
            appointment_date=datetime.strptime(
                form["appointment_date"], "%Y-%m-%d"
            ).date(),
            appointment_time=datetime.strptime(
                form["appointment_time"], "%H:%M"
            ).time(),
            reason=form["reason"]
        )

        db.session.add(appointment)
        db.session.commit()

        return redirect("/appointments")

    return render_template(
        "appointment/add.html",
        patients=Patient.query.all(),
        doctors=Doctor.query.all()
    )


@appointment_bp.route("/appointments/delete/<int:id>")
def delete_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    db.session.delete(appointment)
    db.session.commit()

    return redirect("/appointments")