# 3rd party
from fastapi.testclient import TestClient
import pytest

# my own
from app.main import app
from app.models import AnswerModel

client = TestClient(app)


def test_insert_answer_fails_on_empty():
    with TestClient(app) as client:
        response = client.post(
            "/answers/",
            json={
                "result_accuracy": "",
                "member_support": "",
                "turnaround_time": "",
                "feedback": "",
                "email": "",
                "vid_upload": ""
            }
            )
        assert response.status_code == 406
        assert response.json() == {"detail": "one or more of the required fields is empty"}


def test_insert_answer():
    with TestClient(app) as client:
        response = client.post(
            "/answers/",
            json={
                "result_accuracy": "5 stars",
                "member_support": "5 stars",
                "turnaround_time": "5 stars",
                "feedback": "blah blah",
                "email": "blah@blah.com",
                "vid_upload": "/somewhere/at/somewhere"
            }
            )
        assert response.status_code == 201
        assert response.json() == {"status": "successfully saved answer", "IP": "testclient"}


def test_get_an_answer():
    with TestClient(app) as client:
        response = client.get("/answers/1")
        assert response.status_code == 200
        assert response.json() == {
            "result_accuracy": "5 stars",
            "member_support": "5 stars",
            "turnaround_time": "5 stars",
            "feedback": "blah blah",
            "email": "blah@blah.com",
            "vid_upload": "/somewhere/at/somewhere"
        }


def test_get_all_answers():
    with TestClient(app) as client:
        response = client.get("/answers/")
        assert response.status_code == 200
        assert len(response.json()) != 0
