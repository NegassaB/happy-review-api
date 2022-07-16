# 3rd party
import pytest

# my own
from app.crud import (
    create_answer,
    open_db_cxn,
    close_db_cxn,
    create_db_tables,
    get_reviewee_email,
    get_reviewee_host,
    get_single_answer,
    get_all_answers,
)
from app.database import db
from app.schemas import AnswerSchema


def test1_open_db_cxn():
    open_db_cxn()
    assert db.is_closed() is False


def test2_close_db_cxn():
    close_db_cxn()
    assert db.is_closed() is True


def test3_create_db_tables():
    create_db_tables()
    assert db.table_exists("review_question_table") is True
    assert db.table_exists("answer_table") is True


def test4_create_answer():
    json = {
        "result_accuracy": "5 stars",
        "member_support": "5 stars",
        "turnaround_time": "5 stars",
        "feedback": "blah blah",
        "email": "blah@blah.com",
        "vid_upload": "/somewhere/at/somewhere"
    }
    create_answer(AnswerSchema(**json), host="1.1.1.1")
    res = get_single_answer(id=1)
    assert res.result_accuracy == json["result_accuracy"]


def test5_get_reviewee_host():
    res = get_reviewee_email("")
    assert res is None


def test6_get_reviewee_email():
    res = get_reviewee_host("")
    assert res is None


def test7_get_single_answer():
    res = get_single_answer(id=1)
    assert res is not None
    assert res.ans_id == 1


def test8_get_all_answers():
    res = get_all_answers()
    assert isinstance(res, list)
    assert len(res) != 0


def test9_create_answer_duplicates_throws_exception():
    with pytest.raises(Exception):
        json = {
            "result_accuracy": "5 stars",
            "member_support": "5 stars",
            "turnaround_time": "5 stars",
            "feedback": "blah blah",
            "email": "blah@blah.com",
            "vid_upload": "/somewhere/at/somewhere"
        }
        create_answer(AnswerSchema(**json), host="1.1.1.1")


def test10_create_answer_fails_on_empty():
    with pytest.raises(Exception):
        json = {
            "result_accuracy": "",
            "member_support": "",
            "turnaround_time": "",
            "feedback": "",
            "email": "b",
            "vid_upload": ""
        }
        create_answer(AnswerSchema(**json), host="1.1.1.1")


def test11_create_review_question():
    pass
