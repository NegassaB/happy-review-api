from re import L
import pytest
from app.crud import (open_db_cxn, close_db_cxn, create_db_tables, get_reviewee_email, get_reviewee_host)
from app.database import db


def test_open_db_cxn():
    open_db_cxn()
    assert db.is_closed() is False


def test_close_db_cxn():
    close_db_cxn()
    assert db.is_closed() is True


def test_create_db_tables():
    create_db_tables()
    assert db.table_exists("review_question_table") is True
    assert db.table_exists("answer_table") is True


def test_get_reviewee_host():
    res = get_reviewee_email("")
    assert res is None


def test_get_reviewee_email():
    res = get_reviewee_host("")
    assert res is None


def test_get_reviewee_host_no_duplicates():
    pass


def test_get_reviewee_email_no_duplicates():
    pass
