import os

from flask import Flask


# Get config to connect to database
# def get_db_conf():
#     _config = {
#         "user": "root",
#         "host": "db",
#         "database": "bdays",
#     }

#     try:
#         pwd = open("/run/secrets/db-password", "r")
#         _config["password"] = pwd.read()
#         pwd.close()
#         return _config
#     except ValueError:
#         print("Error opening password file.")
#         exit(1)


# Create app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "birthdays.sqlite")
    )

    if test_config is None:
        # load the instance config if it exists - when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config if available
        app.config.update(test_config)

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the database
    from . import db

    db.init_app(app)

    # Apply the blueprints to the app
    from . import entry

    app.register_blueprint(entry.bp)

    return app
