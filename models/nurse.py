from database.db import db


class Nurse(db.Model):
    __tablename__ = "nurses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    department = db.Column(db.String(100), nullable=False)
    shift = db.Column(db.String(50), nullable=False)