import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_get_users():
    client = app.test_client()

    response = client.get("/api/users")

    assert response.status_code == 200


def test_get_attendance():
    client = app.test_client()

    response = client.get("/api/attendance")

    assert response.status_code == 200