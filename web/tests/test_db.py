import sqlite3

import pytest

from birthdays.db import get_db


def test_get_close_db(app):
    """get_db should return the same connection each time it's called."""
    with app.app_context():
        db = get_db()
        assert db is get_db()

    """Connection should be closed after the context above"""
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # Reokace init_db with one that records that it's been called.
    monkeypatch.setattr("birthdays.db.init_db", fake_init_db)

    # Runner fixture call the init-db command
    result = runner.invoke(args=["init-db"])

    assert "Initialized" in result.output
    assert Recorder.called
