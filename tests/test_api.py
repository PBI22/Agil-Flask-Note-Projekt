from .conftest import Note

def test_login_valid_user(client):
    """
    Test logging in with valid credentials and checking for a JWT token.
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
    """
    response = client.post(
        "/api/login", json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid credentials!" in response.get_json()["message"]


def test_login_missing_credentials(client):
    """
    Test login failure with missing credentials.
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
    """
    response = client.get("/api/unprotected")
    assert response.status_code == 200
    assert "Anyone can view this!" in response.get_json()["message"]


def test_protected_route_with_jwt(client):
    """
    Test accessing a protected route with a valid JWT.
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
    """
    response = client.get("/api/protected")
    assert response.status_code == 401


def test_get_notes_with_jwt(client):
    """
    Test retrieving notes with a valid JWT token.
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
    """
    response = client.get("/api/notes")
    assert response.status_code == 200 # current endpoint is unprotected atm
    assert isinstance(response.get_json(), list) # current endpoint is unprotected atm


def test_get_note_by_valid_id(client, dbsession):
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
    assert data[0]['title'] == "Test Note"
    assert data[0]["text"] == "This is a test note"


def test_get_note_by_invalid_id(client):
    response = client.get("/api/notes/999999")  # Assuming 999999 does not exist
    assert response.status_code == 404
    assert response.get_json()["message"] == "Note not found"


def test_create_valid_note(client, dbsession):
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
    # Log in to get a valid JWT
    login_response = client.post(
        "/api/login", json={"username": "testuser", "password": "test"}
    )
    jwt_token = login_response.get_json()["access_token"]

    response = client.delete(
        "/api/notes/999999", headers={"Authorization": f"Bearer {jwt_token}"}
    )  # Assuming 999999 does not exist
    assert response.status_code == 200 # maybe we should return 404 instead
    assert (
        "The note does not exist" or "The author does not exist" in response.data.decode() # should fix this
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
    assert "Note not found" or "the author does not exist" in response.get_json()["message"] # should fix this


def test_swagger_ui_accessibility(client):
    """
    Test to ensure that the Swagger UI is accessible at the /apidocs endpoint.
    """
    response = client.get("/apidocs/")
    assert (
        response.status_code == 200
    ), "Failed to access /apidocs/ with status code {}".format(response.status_code)
    assert (
        "text/html" in response.content_type
    ), "Expected content type text/html but got {}".format(response.content_type)
    assert "swagger" in response.data.decode(
        "utf-8"
    ), "swagger text not found in response"
