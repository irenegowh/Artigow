# tests/test_app.py
import pytest
import os
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_welcome_message(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenido a Artigow!' in response.data
