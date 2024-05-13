"""
This module configures the testing environment for the Flask application `hello_app`. 
It includes fixtures for setting up a test client and a database session. 
The test client fixture initializes a temporary in-memory database, 
populates it with a test user, and provides a Flask test client for making requests. 
The database session fixture provides a session object for database operations during tests.
"""

import os
import pytest
from werkzeug.security import generate_password_hash
# pylint: disable=C0413
os.environ["TESTING"] = "True"
from hello_app.webapp import app as flask_app
from hello_app.models import Account, Note
from hello_app.dbconnect import dbsession as db
# pylint: enable=C0413

flask_app.config["WTF_CSRF_ENABLED"] = False #NOSONAR
@pytest.fixture(scope="function")
def client():
    """
    This function is a pytest fixture that sets up an in-memory database
    and returns a test client for the Flask application.

    Parameters:
    - None

    Returns:
    - test_client: A test client for the Flask application.

    """
    with flask_app.app_context():
        hashed_password = generate_password_hash("test")  # NOSONAR
        user = Account(
            username="testuser",
            password=hashed_password,
            email="test@testuser.com",
            roleID=1,
        )
        db.add(user)
        db.commit()
        yield flask_app.test_client()
        # Ryd op i databasen efter hver test
        db.query(Account).delete()
        db.query(Note).delete()
        db.commit()


# gør så vi kan bruge dbsession som et argument i vores tests
@pytest.fixture(scope="function")
def dbsession():
    """
This function returns the database session object.

Returns:
    dbsession (Session): The database session object.
"""
    yield db
