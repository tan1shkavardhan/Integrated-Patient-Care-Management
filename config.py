import urllib.parse


class Config:

    SECRET_KEY = "patientcare123"

    password = urllib.parse.quote_plus("tan1shk@")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:{password}@localhost/patientcare"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False