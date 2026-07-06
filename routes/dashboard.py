from flask import Blueprint, render_template

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

from utils.auth import login_required, role_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/admin")
@login_required
@role_required("Admin")
def admin():

    return render_template(
        "dashboard/admin.html",
        total_patients=Patient.query.count(),
        total_doctors=Doctor.query.count(),
        total_appointments=Appointment.query.count(),
        pending_appointments=Appointment.query.filter_by(
            status="Pending"
        ).count()
    )


@dashboard_bp.route("/doctor")
@login_required
@role_required("Doctor")
def doctor():

    return render_template("dashboard/doctor.html")


@dashboard_bp.route("/nurse")
@login_required
@role_required("Nurse")
def nurse():

    return render_template("dashboard/nurse.html")


@dashboard_bp.route("/patient")
@login_required
@role_required("Patient")
def patient():

    return render_template("dashboard/patient.html")