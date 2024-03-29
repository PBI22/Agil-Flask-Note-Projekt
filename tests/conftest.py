# conftest.py
import pytest
import os
os.environ['TESTING'] = 'True'
from hello_app.webapp import app as flask_app
from hello_app.models import Account, Note
from werkzeug.security import generate_password_hash
from hello_app.dbconnect import dbsession as db


@pytest.fixture(scope='function')
def client():
    # Sæt op in-memory database for hver test
    with flask_app.app_context():
        hashed_password = generate_password_hash('test')
        user = Account(username='testuser', password=hashed_password, email="test@testuser.com", roleID=1)
        db.add(user)
        db.commit()
        yield flask_app.test_client()
        # Ryd op i databasen efter hver test
        db.query(Account).delete()
        db.query(Note).delete()
        db.commit()
        
# gør så vi kan bruge dbsession som et argument i vores tests
@pytest.fixture(scope='function')
def dbsession():
    yield db
