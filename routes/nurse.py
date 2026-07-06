from flask import Blueprint, render_template, request, redirect

from database.db import db
from models.nurse import Nurse

nurse_bp = Blueprint("nurse", __name__)


@nurse_bp.route("/nurses")
def list_nurses():

    nurses = Nurse.query.all()

    return render_template(
        "nurse/list.html",
        nurses=nurses
    )


@nurse_bp.route("/nurses/add", methods=["GET", "POST"])
def add_nurse():

    if request.method == "POST":

        form = request.form

        nurse = Nurse(
            name=form["name"],
            department=form["department"],
            shift=form["shift"],
            contact=form["contact"],
            email=form["email"]
        )

        db.session.add(nurse)
        db.session.commit()

        return redirect("/nurses")

    return render_template("nurse/register.html")


@nurse_bp.route("/nurses/edit/<int:id>", methods=["GET", "POST"])
def edit_nurse(id):

    nurse = Nurse.query.get_or_404(id)

    if request.method == "POST":

        form = request.form

        nurse.name = form["name"]
        nurse.department = form["department"]
        nurse.shift = form["shift"]
        nurse.contact = form["contact"]
        nurse.email = form["email"]

        db.session.commit()

        return redirect("/nurses")

    return render_template(
        "nurse/edit.html",
        nurse=nurse
    )


@nurse_bp.route("/nurses/delete/<int:id>")
def delete_nurse(id):

    nurse = Nurse.query.get_or_404(id)

    db.session.delete(nurse)
    db.session.commit()

    return redirect("/nurses")