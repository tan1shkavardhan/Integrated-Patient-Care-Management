from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
from database.db import db
from models.user import User
from werkzeug.security import check_password_hash
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "patientcare123"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:tan1shk%40@localhost/patientcare"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():

    fullname = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = generate_password_hash(request.form["password"])
    role = request.form["role"]

    user = User(
        fullname=fullname,
        email=email,
        phone=phone,
        password=password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        if user.role == "Admin":
            return redirect("/admin")

        elif user.role == "Doctor":
            return redirect("/doctor")

        elif user.role == "Nurse":
            return redirect("/nurse")

        else:
            return redirect("/patient")

    return "Invalid Email or Password"


@app.route("/admin")
def admin():
    return "<h1>Admin Dashboard</h1>"


@app.route("/doctor")
def doctor():
    return "<h1>Doctor Dashboard</h1>"


@app.route("/nurse")
def nurse():
    return "<h1>Nurse Dashboard</h1>"


@app.route("/patient")
def patient():
    return "<h1>Patient Dashboard</h1>"

@app.route("/patient/register")
def patient_register():
    return render_template("patient_register.html")


@app.route("/patient/register", methods=["POST"])
def save_patient():

    patient = Patient(
        fullname=request.form["fullname"],
        age=request.form["age"],
        gender=request.form["gender"],
        contact=request.form["contact"],
        address=request.form["address"],
        blood_group=request.form["blood_group"]
    )

    db.session.add(patient)
    db.session.commit()

    return "Patient Registered Successfully!"

@app.route("/patients")
def patient_list():

    patients = Patient.query.all()

    return render_template(
        "patient_list.html",
        patients=patients
    )

@app.route("/patients/profile/<int:id>")
def patient_profile(id):

    patient = Patient.query.get_or_404(id)

    return render_template("patient_profile.html", patient=patient)


@app.route("/patients/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient.fullname = request.form["fullname"]
        patient.age = request.form["age"]
        patient.gender = request.form["gender"]
        patient.contact = request.form["contact"]
        patient.address = request.form["address"]
        patient.blood_group = request.form["blood_group"]

        db.session.commit()

        return redirect("/patients")

    return render_template("edit_patient.html", patient=patient)

@app.route("/doctor/register", methods=["GET", "POST"])
def doctor_register():

    if request.method == "POST":

        doctor = Doctor(
            name=request.form["name"],
            specialization=request.form["specialization"],
            qualification=request.form["qualification"],
            department=request.form["department"],
            contact=request.form["contact"],
            email=request.form["email"],
            available_time=request.form["available_time"]
        )

        db.session.add(doctor)
        db.session.commit()

        return redirect("/doctors")

    return render_template("doctor_register.html")

@app.route("/doctors")
def doctor_list():

    doctors = Doctor.query.all()

    return render_template(
        "doctor_list.html",
        doctors=doctors
    )

@app.route("/doctor/edit/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":

        doctor.name = request.form["name"]
        doctor.specialization = request.form["specialization"]
        doctor.qualification = request.form["qualification"]
        doctor.department = request.form["department"]
        doctor.contact = request.form["contact"]
        doctor.email = request.form["email"]
        doctor.available_time = request.form["available_time"]

        db.session.commit()

        return redirect("/doctors")

    return render_template("edit_doctor.html", doctor=doctor)

@app.route("/doctor/delete/<int:id>")
def delete_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    db.session.delete(doctor)
    db.session.commit()

    return redirect("/doctors")


@app.route("/appointment/register", methods=["GET", "POST"])
def appointment_register():

    if request.method == "POST":

        appointment = Appointment(
            patient_id=request.form["patient_id"],
            doctor_id=request.form["doctor_id"],
            appointment_date=datetime.strptime(
                request.form["appointment_date"], "%Y-%m-%d"
            ).date(),
            appointment_time=datetime.strptime(
                request.form["appointment_time"], "%H:%M"
            ).time(),
            reason=request.form["reason"]
        )

        db.session.add(appointment)
        db.session.commit()

        return redirect("/appointments")

    patients = Patient.query.all()
    doctors = Doctor.query.all()

    return render_template(
        "appointment_register.html",
        patients=patients,
        doctors=doctors
    )


@app.route("/appointments")
def appointment_list():

    appointments = Appointment.query.all()

    return render_template(
        "appointment_list.html",
        appointments=appointments
    )

if __name__ == "__main__":
    app.run(debug=True)