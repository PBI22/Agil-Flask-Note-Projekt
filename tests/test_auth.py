# test_auth.py
from .conftest import Account

"""
Testing af auth endpoints - Burde reelt opdeles i mindre tests senere hen.
"""

def test_login_success(client):
    response = client.post('/auth/login', data=dict(
        username='testuser',
        password='test'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Logged in as:' in response.data.decode('utf-8')
    assert 'Logout' in response.data.decode('utf-8')
    assert 'Invalid username or password' not in response.data.decode('utf-8')

def test_login_fail(client):
    response = client.post('/auth/login', data=dict(
        username='testuser',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password' in response.data.decode('utf-8')

def test_login_wrong_pass(client):
    response = client.post('/auth/login', data=dict(
        username='testuser',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password' in response.data.decode('utf-8')

def test_signup(client,dbsession):
    response = client.post('/auth/signup', data=dict(
        username='testsignupuser',
        password='test',
        email="testsignup@test.dk"
    ), follow_redirects=True)
    # Tjek brugeren er i databasen
    user = dbsession.query(Account).filter_by(username='testsignupuser').first()
    assert user is not None
    assert user.username == 'testsignupuser'
    assert user.password != 'test' # fordi password er hashed
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Logged in as:' in response.data.decode('utf-8')
    assert 'Logout' in response.data.decode('utf-8')
    assert 'Invalid username or password' not in response.data.decode('utf-8')

def test_logout(client):
    # Log ind først
    response = client.post('/auth/login', data=dict(
        username='testuser',
        password='test'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Hjem' in response.data
    assert 'Logged in as:' in response.data.decode('utf-8')
    assert 'Logout' in response.data.decode('utf-8')
    # Log ud
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'You have been logged out' in response.data.decode('utf-8')
    assert 'Logged in as:' not in response.data.decode('utf-8')
    