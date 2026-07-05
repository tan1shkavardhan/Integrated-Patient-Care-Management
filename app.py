from flask import Flask, render_template
from database.db import db
from models.user import User

app = Flask(__name__)

app.config["SECRET_KEY"] = "patientcare123"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:tan1shk%40@localhost/patientcare"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)