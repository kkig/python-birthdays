import pytest

from birthdays.db import get_db


def test_index(client, app):
    """Check that the endpoint exists."""
    response = client.post(
        "/",
        data={"name": "apple", "bday": "2020-09-10"},
    )
    assert response.status_code == 200
    assert b"apple" in response.data

    with app.app_context():
        res = (
            get_db()
            .execute("SELECT * FROM person WHERE firstname = 'apple'")
            .fetchone()
        )
        assert res is not None
