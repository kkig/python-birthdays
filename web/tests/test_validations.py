from datetime import date
from helpers import getDate
# import pytest


def test_bad_string():
    assert getDate("Jim") is None


def test_bad_type():
    assert getDate(999 - 10 - 20) is None


def test_format():
    assert getDate("1999-10-19") == date(1999, 10, 19)
