from datetime import date
from helpers import toDate
# import pytest


def test_bad_string():
    assert toDate("Jim") is None


def test_bad_type():
    assert toDate(999 - 10 - 20) is None


def test_format():
    assert toDate("1999-10-19") == date(1999, 10, 19)
