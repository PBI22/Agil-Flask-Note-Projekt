"""
This module contains tests for the authentication functionality of a Flask application. 
It includes tests for login success and failure scenarios, signup process, and logout functionality.

Functions:
- test_login_success(client): Tests successful login with valid credentials.
- test_login_fail(client): Tests login failure with invalid credentials.
- test_login_wrong_pass(client): Tests login failure with a correct username but incorrect password.
- test_signup(client, dbsession): Tests the signup process and verifies that the new user 
  is added to the database.
- test_logout(client): Tests the logout process, ensuring the user is properly logged out.

Each function simulates HTTP requests to the respective authentication endpoints 
and asserts the expected outcomes based on the response status codes and response data content.
"""

from .conftest import Account

def test_login_success(client):
    """
    Test the login functionality with valid credentials.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function sends a POST request to the '/auth/login' endpoint with valid username and password.
    It then checks the response status code, the presence of 'Hjem' in the response data, 
    and the presence of 'Logged in as:' and 'Logout' in the decoded response data. 
    It also checks that the response data does not contain the string 'Invalid username or password'.
    If any of the assertions fail, an AssertionError is raised.

    Example Usage:
    test_login_success(client)
    """
    response = client.post(
        "/auth/login",
        data={
            "username":"testuser",
            "password":"test"   
            },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Logged in as:" in response.data.decode("utf-8")
    assert "Logout" in response.data.decode("utf-8")
    assert "Invalid username or password" not in response.data.decode("utf-8")


def test_login_fail(client):
    """
    Test the login functionality with invalid credentials.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function sends a POST request to the '/auth/login' endpoint with invalid username and password.
    It then checks the response status code and the presence of 'Invalid username or password' in
    the decoded response data. If any of the assertions fail, an AssertionError is raised.

    Example Usage:
    test_login_fail(client)
    """
    response = client.post(
            "/auth/login",
            data={
                "username":"testuser",
                "password":"wrongpassword"   
                },
            follow_redirects=True,
        )
    assert response.status_code == 200
    assert "Invalid username or password" in response.data.decode("utf-8")


def test_login_wrong_pass(client):
    """
    Test the login functionality with an incorrect password.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function sends a POST request to the '/auth/login' endpoint with a valid username and 
    an incorrect password. It then checks the response status code and the presence of 
    'Invalid username or password' in the decoded response data. If any of the assertions fail,
    an AssertionError is raised.

    Example Usage:
    test_login_wrong_pass(client)
    """
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Invalid username or password" in response.data.decode("utf-8")


def test_signup(client, dbsession):
    """
    Test the signup functionality of the application.

    This function sends a POST request to the '/auth/signup' endpoint with the necessary
    data for creating a new user account, checks if the user is successfully added to the
    database, verifies that the response status code is 200, and ensures that the response
    data includes the expected strings indicating a successful signup.
    """
    response = client.post(
        "/auth/signup",
        data={
            "username": "testsignupuser",
            "email": "testsignup@test.dk",
            "password": "test",
            "confirm_password": "test",  # Ensure the confirmation password matches
        },
        follow_redirects=True,
    )
    # Verify that the user is correctly added to the database
    user = dbsession.query(Account).filter_by(username="testsignupuser").first()
    assert user is not None
    assert user.username == "testsignupuser"
    assert user.email == "testsignup@test.dk"
    # Ensure password is hashed and does not equal the plaintext
    assert user.password != "test"

    # Check response status code and body content
    assert response.status_code == 200
    # Check for success message and user redirection/logged-in indicators
    response_data = response.data.decode("utf-8")
    assert "Account created successfully!" in response_data
    assert "Logged in as:" in response_data
    assert "Logout" in response_data
    assert "Invalid username or password" not in response_data


def test_logout(client):
    """
    Test the logout functionality of the application.

    Parameters:
    - client: The Flask test client object.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function tests the logout functionality of the application. 
    It first logs in the user by sending a POST request to the '/auth/login' 
    endpoint with valid username and password. It then checks if the login was successful
    by verifying the response status code, the presence of 'Hjem', 'Logged in as:',
    and 'Logout' in the response data.

    After logging in, the function sends a GET request to the '/auth/logout' 
    endpoint to log out the user. It checks if the logout was successful by verifying
    the response status code and the presence of 'You have been logged out' in the
    response data. It also checks that 'Logged in as:' is not present in the response data.

    If any of the assertions fail, an AssertionError is raised.

    Example Usage:
    test_logout(client)
    """
    # Log ind først
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "test"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Logged in as:" in response.data.decode("utf-8")
    assert "Logout" in response.data.decode("utf-8")
    # Log ud
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert "You have been logged out" in response.data.decode("utf-8")
    assert "Logged in as:" not in response.data.decode("utf-8")
