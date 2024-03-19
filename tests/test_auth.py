import pytest
from hello_app.webapp import app
from hello_app.dbconnect import engine, dbsession as db, Base
from hello_app.models import Account  # Antager Base er din declarative base
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Opsæt in-memory database for hver test
    with app.app_context():
        Base.metadata.create_all(engine)  # Bruger engine til at skabe alle tabeller
        # Tilføjer testbruger
        hashed_password = generate_password_hash('test')
        user = Account(username='testuser', password=hashed_password, email="test@testuser.com")
        db.add(user)
        db.commit()
        yield app.test_client()
        Base.metadata.drop_all(engine)  # Dropper alle tabeller efter test


def test_login(client):
    response = client.post('auth/login', data=dict(
        username='testuser',
        password='test',
        email='test@testuser.com'
    ), follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
    

