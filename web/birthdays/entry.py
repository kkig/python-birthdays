from datetime import date
# from dbloader import DB


# from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask import render_template, request, g, Blueprint, flash
from .db import get_db

bp = Blueprint("entry", __name__)
conn = None


@bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@bp.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form["name"]
        bday = request.form["bday"]
        error = None

        if name == "":
            error = "Name is required."
        elif not name.isalnum():
            error = "Name should only use numbers and characters."
        elif bday == "None":
            error = "Birthday is required."

        try:
            bday = date.fromisoformat(bday)
        except ValueError:
            error = "Invalid birthday."

        if not error:
            db.execute(
                "INSERT INTO person (firstname, birthday) VALUES (?, ?)",
                (name, bday),
            )
            db.commit()

        flash(error)

    # TODO: Display the entries in the database on index.html
    bdays = db.execute("SELECT * FROM person").fetchall()

    return render_template("entry/index.html", data=bdays)
