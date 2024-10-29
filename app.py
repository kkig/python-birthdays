import os

import sqlite3
# from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
con = sqlite3.connect("birthdays.db")
db = con.cursor()
res = db.execute("SELECT * FROM birthdays")
datats = [x for x in res]
data = res.fetchall()
# id, name, month, day = res.fetchall()
con.close()

# db.execute("""
#     INSERT INTO birthdays VALUES
#            ('666', 'Henry', 09, 08),
#            ('555', 'Paul', 05, 12),
# """)
# db.commit()
# db = SQL("sqlite:///birthdays.db")


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

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        return render_template("index.html")

@app.route("/test", methods=["GET"])
def test():
    if request.method == "GET":
        return datats

