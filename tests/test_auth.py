import pytest
import os
from flask import Flask
from hello_app.webapp import app
from werkzeug.security import generate_password_hash
from hello_app.models import Account
from hello_app.dbconnect import dbsession as db

"""
fix liste:
Tjek logs når der tests
opret resterende tests
husk clean up + clean up db

"""

@pytest.fixture
def client():
    os.environ["TESTING"] = "True"
    # Opsæt in-memory database for hver test
    with app.app_context():
        hashed_password = generate_password_hash('test')
        user = Account(username='testuser', password=hashed_password)
        user = Account(username='testuser', password=hashed_password, email="test@testuser.com")
        db.add(user)
        db.commit()
        yield app.test_client()
        os.environ.pop("TESTING")  # Ryd op efter testen
        

def test_login_success(client):
    response = client.post('auth/login', data=dict(
        username='testuser',
        password='test'
    ), follow_redirects=True)
    assert response.status_code == 200
    #tjek at siden er blevet redirected til home
    assert b'Hjem' in response.data
    assert 'Logged in as:' in response.data.decode('utf-8')
    assert 'Logout' in response.data.decode('utf-8')
    assert 'Invalid username or password' not in response.data.decode('utf-8')
    
def test_login_fail(client):
    response = client.post('auth/login', data=dict(
        username='testuser',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password'in response.data.decode('utf-8')
