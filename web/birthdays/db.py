# import mysql.connector
# from mysql.connector import errorcode

import sqlite3
# from datetime import datetime

import click
from flask import g, current_app


# Internal use
# def _conn_db():
#     """Connect to the application's database."""
#     try:
#         cnx = mysql.connector.connect(**current_app.config["DB_CONF"])
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#         exit(1)

#     return cnx


# fn to handle database operations
def get_db():
    """Connect to the application's database. The coonection is unique
    for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the connection."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear exisitng data and create new tables."""

    # Get connection to db to execute the SQL commands
    db = get_db()

    # Open schema.sql to run SQL commands
    # - open_resource opens a file relative to the application
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


## register_converter tells Python how to interpret timestamp values in the database
# sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    """Register database from functions with the Flask app.
    This is called by the application factory."""
    # teardown_appcontext tells Flask to call this when clearning up
    #   after returning the response
    app.teardown_appcontext(close_db)

    # add_command adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)
