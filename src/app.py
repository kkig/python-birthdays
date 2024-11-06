import time
import os

import redis
# from redis.cache import CacheConfig
# import sqlite3
# from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


cache = redis.Redis(
    host="localhost", 
    port=6379, 
    # cache_config=CacheConfig(), 
    decode_responses=True
    )

# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return cache.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)


# # Configure CS50 Library to use SQLite database
# con = sqlite3.connect("birthdays.db")
# db = con.cursor()
# res = db.execute("SELECT * FROM birthdays")
# datats = [x for x in res]
# data = res.fetchall()
# # id, name, month, day = res.fetchall()
# con.close()

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
        name = request.form.get("name")
        bday = request.form.get("bday")
        if name and bday:
            return render_template("index.html", name=name, bday=bday)
        
        # Invalid input
        return render_template("index.html", error="Invalid input")

    else:

        # TODO: Display the entries in the database on index.html

        return render_template("index.html", name=request.form.get("name"))

# @app.route("/test", methods=["GET"])
# def test():
#     return {"message": "Hello World"}
    # if request.method == "GET":
    #     return datats

# @app.route('/count')
# def hello():
#     count = get_hit_count()
#     return 'Hello world! I have been seen {} times.\n'.format(count)