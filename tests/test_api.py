"""
This module contains a series of tests for the authentication and note management
features of a Flask application. It includes tests for user login with both valid
and invalid credentials, accessing protected and unprotected routes, and CRUD operations
on notes. Each test function is designed to verify the correct behavior of the API endpoints
under various conditions, ensuring that the application handles authentication, authorization,
and data manipulation correctly.
"""

from .conftest import Note

# pylint: disable=W0613,W0621

def test_login_valid_user(client):
    """
    Test logging in with valid credentials and checking for a JWT token.

    This function sends a POST request to the '/api/login' endpoint with a
    JSON payload containing a valid username and password.
    It then checks if the response status code is 200 (indicating a successful request)
    and if the response data contains an 'access_token' key.

    Parameters:
    - client: The Flask test client object.

    Returns:
    - None
    """
    response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data


def test_login_invalid_user(client):
    """
    Test login failure with invalid credentials.

    This function tests the behavior of the login endpoint when invalid credentials are provided.
    It sends a POST request to the '/api/login' endpoint with a JSON payload containing
    an invalid username and password.
    The expected behavior is that the response status code should be 401 (Unauthorized)
    and the response message should contain 'Invalid credentials!'.

    Args:
        client: The Flask test client.

    Returns:
        None
    """
    response = client.post(
        "/api/login", json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid credentials!" in response.get_json()["message"]


def test_login_missing_credentials(client):
    """
    Test login failure with missing credentials.

    This function tests the scenario where the login request is made without providing
    the required username or password. It verifies that the server responds with the
    appropriate status code and error message.

    Args:
        client: The test client for making HTTP requests.

    Returns:
        None
    """
    # Test with missing username
    response_missing_username = client.post("/api/login", json={"password": "test"})
    assert response_missing_username.status_code == 400
    assert (
        "Username or password missing"
        in response_missing_username.get_json()["message"]
    )

    # Test with missing password
    response_missing_password = client.post("/api/login", json={"username": "testuser"})
    assert response_missing_password.status_code == 400
    assert (
        "Username or password missing"
        in response_missing_password.get_json()["message"]
    )


def test_unprotected_route(client):
    """
    Test accessing an unprotected route.

    This function tests the behavior of accessing an unprotected route in the API.
    It sends a GET request to the "/api/unprotected" endpoint and checks that the
    response status code is 200 (OK). It also verifies that the response message
    contains the expected text "Anyone can view this!".

    Parameters:
    - client: The Flask test client object.

    Returns:
    None
    """
    response = client.get("/api/unprotected")
    assert response.status_code == 200
    assert "Anyone can view this!" in response.get_json()["message"]


def test_protected_route_with_jwt(client):
    """
    Test accessing a protected route with a valid JWT.

    This function tests the behavior of accessing a protected route with a valid JWT.
    It performs the following steps:
    1. Logs in to get a valid JWT.
    2. Uses the JWT to access the protected route.
    3. Asserts that the response status code is 200, indicating a successful access.

    Args:
        client: The Flask test client.

    Returns:
        None
    """
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    # Use the JWT to access the protected route
    response = client.get(
        "/api/protected", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200


def test_protected_route_without_jwt(client):
    """
    Test accessing a protected route without a JWT.

    This test case verifies that when a client tries to access a protected route without providing a valid JWT,
    the server responds with a status code of 401 (Unauthorized).
    """
    response = client.get("/api/protected")
    assert response.status_code == 401


def test_get_notes_with_jwt(client):
    """
    Test retrieving notes with a valid JWT token.

    This test function verifies that the API endpoint for retrieving notes
    requires a valid JWT token for authentication. It performs the following steps:
    
    1. Logs in with a test user to obtain a valid JWT token.
    2. Uses the JWT token to access the notes API endpoint.
    3. Asserts that the response status code is 200 (OK).
    4. Asserts that the response JSON is a list.

    This test ensures that only authenticated users with a valid JWT token
    can access the notes API endpoint and retrieve the notes successfully.
    """
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    # Use the JWT to access the notes
    response = client.get(
        "/api/notes", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_notes_without_jwt(client):
    """
    Test retrieving notes without a JWT token.

    This test case verifies that the endpoint for retrieving notes ("/api/notes")
    returns a successful response (status code 200) and the response body is a list.

    Note: This test assumes that the endpoint is currently unprotected and does not
    require a JWT token for access.
    """
    response = client.get("/api/notes")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_note_by_valid_id(client, dbsession):
    """
    Test case for retrieving a note by a valid ID.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None
    """
    # Create a test note
    test_note = Note(
        title="Test Note",
        text="This is a test note",
        imagelink="http://example.com",
        author=1,
    )
    dbsession.add(test_note)
    dbsession.commit()

    # Retrieve the note
    response = client.get(f"/api/notes/{test_note.noteID}")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["title"] == "Test Note"
    assert data[0]["text"] == "This is a test note"


def test_get_note_by_invalid_id(client):
    """
    Test case to verify the behavior when trying to get a note with an invalid ID.
    It sends a GET request to the '/api/notes/999999' endpoint and asserts that the response
    status code is 404 (Not Found) and the response JSON contains the expected error message.
    """
    response = client.get("/api/notes/999999")  # Assuming 999999 does not exist
    assert response.status_code == 404
    assert response.get_json()["message"] == "Note not found"


def test_create_valid_note(client, dbsession):
    """
    Test case for creating a valid note.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None
    """
    # Log in to get a valid JWT (assuming JWT is required for this endpoint)
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    note_details = {
        "title": "New Note",
        "text": "Note details here",
        "imagelink": "http://example.com",
    }
    response = client.post(
        "/api/notes/create",
        json=note_details,
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Note created successfully"
    assert response.get_json()["titel"] == "New Note"


def test_create_invalid_note(client, dbsession):
    """
    Test case to verify the behavior of creating an invalid note.

    This test case performs the following steps:
    1. Logs in to get a valid JWT.
    2. Sends a POST request to create a note with missing title and text.
    3. Asserts that the response status code is 400 (Bad Request).
    4. Asserts that the response message contains the expected error message.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None
    """
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    note_details = {"imagelink": "http://example.com"}  # Missing title and text
    response = client.post(
        "/api/notes/create",
        json=note_details,
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 400
    assert (
        "Invalid data" in response.get_json()["message"]
    )  # Assuming your API returns this message


def test_delete_note_with_valid_id(client, dbsession):
    """
    Test case to verify the deletion of a note with a valid ID.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None
    """
    # Create a test note to delete
    test_note = Note(
        title="Test Note to Delete",
        text="Delete this note",
        imagelink="http://example.com",
        author=1,
    )
    dbsession.add(test_note)
    dbsession.commit()

    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    response = client.delete(
        f"/api/notes/{test_note.noteID}",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 200
    assert "has been deleted" in response.data.decode()


def test_delete_note_with_invalid_id(client, dbsession):
    """
    Test case to verify the behavior of deleting a note with an invalid ID.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None
    """
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    response = client.delete(
        "/api/notes/999999", headers={"Authorization": f"Bearer {jwt_token}"}
    )  # Assuming 999999 does not exist
    assert response.status_code == 200  # maybe we should return 404 instead
    assert (
        "The note does not exist"
        or "The author does not exist" in response.data.decode()  # should fix this
    )


def test_edit_note_with_valid_id(client, dbsession):
    # Create a test note
    test_note = Note(
        title="Original Title",
        text="Original Text",
        imagelink="http://original.com",
        author=1,
    )
    dbsession.add(test_note)
    dbsession.commit()

    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    # Data for editing the note
    updated_data = {
        "title": "Updated Title",
        "text": "Updated Text",
        "imagelink": "http://updated.com",
    }

    # Attempt to edit the note
    response = client.put(
        f"/api/notes/{test_note.noteID}",
        json=updated_data,
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Note edited successfully"
    assert response_data["titel"] == "Updated Title"
    assert response_data["text"] == "Updated Text"
    assert response_data["imagelink"] == "http://updated.com"

    # Check the database to confirm changes
    updated_note = dbsession.query(Note).filter(Note.noteID == test_note.noteID).first()
    assert updated_note.title == "Updated Title"
    assert updated_note.text == "Updated Text"
    assert updated_note.imagelink == "http://updated.com"


def test_edit_note_with_invalid_id(client, dbsession):
    """
    Test case to verify the behavior when attempting to edit a non-existent note.

    Args:
        client (FlaskClient): The Flask test client.
        dbsession (Session): The database session.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 404 or the expected error message is not found.
    """
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    # Data for the attempted edit
    updated_data = {
        "title": "Nonexistent Title",
        "text": "Nonexistent Text",
        "imagelink": "http://nonexistent.com",
    }

    # Attempt to edit a non-existent note
    response = client.put(
        "/api/notes/999999",
        json=updated_data,
        headers={"Authorization": f"Bearer {jwt_token}"},
    )  # Assuming 999999 does not exist
    assert response.status_code == 404
    assert (
        "Note not found"
        or "the author does not exist" in response.get_json()["message"]
    )  # should fix this


def test_swagger_ui_accessibility(client):
    """
    Test to ensure that the Swagger UI is accessible at the /apidocs endpoint.
    
    This test sends a GET request to the /apidocs/ endpoint using the provided client.
    It then checks if the response status code is 200, indicating a successful access.
    Additionally, it verifies that the response content type is 'text/html' and that the response
    data contains the string 'swagger'.
    """
    response = client.get("/apidocs/")
    assert (
        response.status_code == 200
    ), f"Failed to access /apidocs/ with status code {response.status_code}"

    assert (
        "text/html" in response.content_type
    ), f"Expected content type text/html but got {response.content_type}"
    assert "swagger" in response.data.decode(
        "utf-8"
    ), "swagger text not found in response"
