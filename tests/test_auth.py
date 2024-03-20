import pytest
#from flask import session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from hello_app.models import Account  
from werkzeug.security import generate_password_hash
from hello_app import create_app
from hello_app.dbconnect import Base

SQL_SCRIPT = """
PRAGMA foreign_keys=OFF;

CREATE TABLE IF NOT EXISTS role (
roleID INTEGER PRIMARY KEY NOT NULL,
rolename VARCHAR(255) NOT NULL);

CREATE TABLE IF NOT EXISTS accountrole (
id INTEGER PRIMARY KEY NOT NULL,
accountID INTEGER NOT NULL,
roleID INTEGER NOT NULL,
FOREIGN KEY(accountID) REFERENCES account(accountID),
FOREIGN KEY(roleID) REFERENCES role(roleID));

CREATE TABLE IF NOT EXISTS note (
noteID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
title VARCHAR(255) NOT NULL,
text TEXT NOT NULL,
created DATETIME NOT NULL,
lastedited DATETIME,
imagelink VARCHAR(255),
author INTEGER NOT NULL,
FOREIGN KEY(author) REFERENCES account(accountID));

CREATE TABLE IF NOT EXISTS account (
accountID INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR NOT NULL,
password VARCHAR NOT NULL,
email VARCHAR NOT NULL);
"""

@pytest.fixture
def app():
    # Opret app med testkonfiguration
    _app = create_app({'TESTING': True, 'DATABASE_URI': 'sqlite:///:memory:'})
    
    # Opret en ny engine og session for test
    test_engine = create_engine('sqlite:///:memory:', echo=True)
    _app.db_session = scoped_session(sessionmaker(bind=test_engine))
    
    # Opret databasen
    with _app.app_context():
        Base.metadata.create_all(bind=test_engine)
        yield _app
        Base.metadata.drop_all(bind=test_engine)
    
    _app.db_session.remove()

@pytest.fixture
def client(app):
    # Returner en test client for app
    with app.test_client() as client:
        yield client

def test_login_success(client):
    # Tilføj testbruger
    hashed_password = generate_password_hash('test')
    user = Account(username='testuser', password=hashed_password, email="test@testuser.com")
    app.db_session.add(user)
    app.db_session.commit()

    response = client.post('auth/login', data=dict(
        username='testuser',
        password='test',
        email='test@testuser.com'
    ), follow_redirects=True)
    assert response.status_code == 200

"""
def test_login_success(client):
    response = client.post('auth/login', data=dict(
        username='testuser',
        password='test',
        email='test@testuser.com'
    ), follow_redirects=True)
    assert response.status_code == 200
    
def test_login_fail(client):
    response = client.post('auth/login', data=dict(
        username='testuser',
        password='wrongpassword',
        email='test@testuser.com'
    ), follow_redirects=True)
    assert response.status_code == 401
    
def test_signup_success(client):
    response = client.post('auth/signup', data=dict(
        username='newuser',
        password='newpassword',
        email='newuser@test.com')
    , follow_redirects=True)
    assert response.status_code == 201
    
# fail ved at oprette en med samme brugernavn
def test_signup_fail(client):
    response = client.post('auth/signup', data=dict(
        username='testuser',
        password='test',
        email='test@test.com')
    , follow_redirects=True)
    assert response.status_code == 409

def test_signup_fail_missing_username(client):
    response = client.post('auth/signup', data=dict(
        password='test',
        email='test@test.com')
    , follow_redirects=True)
    assert response.status_code == 400

def test_logout(client):
    # Log ind først
    logout_response = client.get('auth/logout', follow_redirects=True)
    assert logout_response.status_code == 200
    assert session.get('user', None) is None

"""
