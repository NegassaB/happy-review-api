from fastapi.testclient import TestClient
import pytest
from app.main import app

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
                "email": "dd",
                "vid_upload": ""
            }
            )
        assert response.status_code == 403


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
        ans_2_test = client.get("/answers/1")
        assert ans_2_test is not None
        assert ans_2_test.reviewee_host == "testClient"


def test_get_all_answers():
    with TestClient(app) as client:
        all_ans = client.get("/answers/")
        assert all_ans is not None
        assert isinstance(all_ans, list)
        assert len(all_ans) != 0
