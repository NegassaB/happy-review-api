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
