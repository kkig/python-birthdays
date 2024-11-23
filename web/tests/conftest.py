import os
import tempfile

import pytest

from birthdays import create_app
from birthdays.db import get_db, init_db

# Read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    # Create temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    # Create the app with test config
    # Override DATABASE path (instance folder) to temporary path
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # Create the database tables and insert test data to that tables
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # Close and remove the temporary database path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Test client for the app"""
    # with test_client, tests will use the client to make requests
    #   without running server
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test runner for the app's Click commands."""
    # test_cli_runner creates a runner that can call the Click commands
    return app.test_cli_runner()
