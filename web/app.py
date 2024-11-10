import time
import os
from datetime import date
from dbloader import DB

# import sqlite3
# from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

conn = None


# @app.before_request
# def before_request(request):
#     """Ensure DB is connected"""
#     global conn

#     if not conn:
#         conn = DB()
#         conn.populate()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        bday = request.form.get("bday")
        birthday = date.fromisoformat(bday)
        if name and bday:
            return render_template("index.html", name=name, bday=birthday)

        # Invalid input
        return render_template("index.html", error="Invalid input")

    else:
        # TODO: Display the entries in the database on index.html
        global conn

        if not conn:
            conn = DB()
            conn.populate()
        # names = []
        # bdays = []

        rec = conn.query_all()
        # for person in rec:
        #     _, name, date = person
        #     names.append(name)
        #     bdays.append(date)

        return render_template("index.html", data=rec)


@app.route("/names")
def listNames():
    global conn

    if not conn:
        conn = DB()
        conn.populate()
    rec = conn.query_all()

    respose = ""
    for c in rec:
        respose = respose + "<div> Hello " + c[1] + " born in " + str(c[2]) + "</div>"
    return respose


if __name__ == "__main__":
    app.run()
