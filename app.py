from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash
from database.db import db
from models.user import User
from werkzeug.security import check_password_hash
from models.patient import Patient


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

if __name__ == "__main__":
    app.run(debug=True)