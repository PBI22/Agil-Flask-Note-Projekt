"""
This module contains tests for the note management features of a Flask application using pytest.

It includes tests for creating, editing, deleting, and searching notes,
both with and without user authentication.
Each test function is designed to simulate a client request to the Flask
application and assert the expected outcomes based on the response.

Functions:
- log_in_test_user(client): Fixture to log in a test user.
- test_create_note_get_not_logged_in(client): Tests access to the note creation page without being logged in.
- test_create_note_get(client, log_in_test_user): Tests the GET request for creating a note when logged in.
- test_create_note_post(client, log_in_test_user, dbsession): Tests the POST request for creating a note.
- test_edit_note_get_not_logged_in(client): Tests access to the note editing page without being logged in.
- test_edit_note_get(client, log_in_test_user, dbsession): Tests the GET request for editing a note.
- test_edit_note_post(client, log_in_test_user, dbsession): Tests the POST request for editing a note.
- test_delete_note_get_not_logged_in(client): Tests access to the note deletion page without being logged in.
- test_delete_note_post_success(client, log_in_test_user, dbsession): Tests successful deletion of a note.
- test_delete_note_post_fail(client, log_in_test_user, dbsession): Tests the failure case for note deletion.
- test_delete_note_admin(client, log_in_test_user, dbsession): Tests note deletion by an admin user.
- test_search_result_success(client, log_in_test_user, dbsession): Tests successful search for notes.
- test_search_result_fail(client, log_in_test_user, dbsession): Tests the search functionality with no results.

Each test is designed to ensure that the application behaves as expected under various conditions,
ensuring robustness and reliability of the note management system.
"""

from datetime import datetime
import pytest
from .conftest import Note


# pylint: disable=W0613,W0621
@pytest.fixture
def log_in_test_user(client):
    """
    Log in a test user.

    This function is a fixture that logs in a test user by setting the necessary session variables.
    It is a simplified version and should be replaced with the actual login logic.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - None

    Description:
    This function sets the session variables for a test user:
    - "user": The username of the test user.
    - "userID": The ID of the test user.
    - "userEmail": The email address of the test user.
    - "roleID": The role ID of the test user.

    Example usage:
    @pytest.fixture
    def log_in_test_user(client):
        with client.session_transaction() as session:
            session["user"] = "testuserNotes"
            session["userID"] = 9999
            session["userEmail"] = "testusernotes@test.com"
            session["roleID"] = 1  # standard bruger
    """
    with client.session_transaction() as session:
        session["user"] = "testuserNotes"
        session["userID"] = 9999
        session["userEmail"] = "testusernotes@test.com"
        session["roleID"] = 1  # standard bruger


# test create note uden at være logget ind:
def test_create_note_get_not_logged_in(client):
    """
    Test the 'test_create_note_get_not_logged_in' function.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function tests the behavior of the 'test_create_note_get_not_logged_in' function
    when the user is not logged in.
    It sends a GET request to the '/notes/create/' endpoint and checks various assertions
    to ensure that the expected error message is displayed and the response status code is correct.

    Assertions:
    - The response status code should be 200.
    - The string "You need to be logged in to view this page." should be present in the decoded response data.
    - The string "Login" should be present in the decoded response data.
    """
    response = client.get("/notes/create/", follow_redirects=True)
    assert "You need to be logged in to view this page." in response.data.decode(
        "utf-8"
    )
    assert "Login" in response.data.decode("utf-8")
    assert response.status_code == 200


# Test creating a note
def test_create_note_get(client, log_in_test_user):
    """
    Test the GET request for creating a note.

    This function tests the GET request for creating a note by sending a request
    to the "/notes/create/" endpoint and checking the response.

    Parameters:
    - client: The Flask test client.
    - log_in_test_user: The fixture that logs in a test user.

    Returns:
    - None

    Raises:
    - None

    Description:
    This function performs the following steps:
    1. Sends a GET request to the "/notes/create/" endpoint.
    2. Checks if the response contains the string "Logged in as:".
    3. Checks if the response contains the string "Create Note".
    4. Checks if the response contains the string "Opret Note".
    5. Checks if the response status code is 200.

    Example usage:
    test_create_note_get(client, log_in_test_user)
    """
    response = client.get("/notes/create/")
    assert "Logged in as: " in response.data.decode("utf-8")
    assert "Create Note" in response.data.decode("utf-8")
    assert "Opret Note" in response.data.decode("utf-8")
    assert response.status_code == 200


def test_create_note_post(client, log_in_test_user, dbsession):
    """
    Test the functionality of creating a note.

    Parameters:
    - client: The Flask test client.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function tests the functionality of creating a note by sending a POST request
    to the "/notes/create/" endpoint with the necessary data. 
    It then checks various assertions to ensure that the note is created successfully.

    Assertions:
    - The response status code should be 200.
    - The string "Hjem" should be present in the response data.
    - The string "Failed to create note" should not be present in the decoded response data.
    - The string "Note created successfully" should be present in the decoded response data.
    - The string "Test Note" should be present in the decoded response data.
    - The note with the title "Test Note" should exist in the database.
    - The title of the note should be "Test Note".
    - The text of the note should be "This is a test note".
    """
    response = client.post(
        "/notes/create/",
        data={
            "title":"Test Note", 
            "note":"This is a test note"
            },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Failed to create note" not in response.data.decode("utf-8")
    assert "Note created successfully" in response.data.decode("utf-8")
    # Fordi Test Note er titlen og vi redirecter til home, så tjekker vi om Test Note er i home
    assert "Test Note" in response.data.decode("utf-8")
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title="Test Note").first()
    assert note is not None
    assert note.title == "Test Note"
    assert note.text == "This is a test note"


def test_edit_note_get_not_logged_in(client):
    """
    Test the 'edit_note_get_not_logged_in' function.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function tests the behavior of the 'edit_note_get_not_logged_in' function
    when the user is not logged in. It sends a GET request to the '/notes/edit/1' endpoint
    and checks various assertions to ensure that the expected error message is displayed
    and the response status code is correct.

    Assertions:
    - The response status code should be 200.
    - The string "You need to be logged in to view this page." should be present in the decoded response data.
    - The string "Login" should be present in the decoded response data.
    """
    response = client.get("/notes/edit/1", follow_redirects=True)
    assert "You need to be logged in to view this page." in response.data.decode(
        "utf-8"
    )
    assert "Login" in response.data.decode("utf-8")
    assert response.status_code == 200


def test_edit_note_get(client, log_in_test_user, dbsession):
    """
    Test the GET request for editing a note.

    Parameters:
    - client: The Flask test client.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail or the response status code is not 200.

    Description:
    - Creates a note to edit.
    - Sends a GET request to the edit endpoint with the note ID.
    - Asserts that the response contains the expected content.
    - Asserts that the response status code is 200.
    """
    note = Note(
        title="Test Edit Note",
        text="This is a test edit note, for testing edit endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    response = client.get(f"/notes/edit/{note.noteID}")
    assert "Logged in as: " in response.data.decode("utf-8")
    assert "Edit Note" in response.data.decode("utf-8")
    assert "Rediger Note" in response.data.decode("utf-8")
    assert "This is a test edit note" in response.data.decode("utf-8")
    assert "Test Edit Note" in response.data.decode("utf-8")
    assert response.status_code == 200


def test_edit_note_post(client, log_in_test_user, dbsession):
    """
    Test the edit note post endpoint.

    This function tests the functionality of the edit note post endpoint in the application. 
    It creates a new note, edits it using the post request, and then checks the response 
    for the expected results.

    Parameters:
    - client: The Flask test client object.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session object.

    Returns:
    None

    Raises:
    None
    """
    note = Note(
        title="Test Edit Note Post",
        text="This is a test edit note post, for testing edit post endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    response = client.post(
        f"/notes/edit/{note.noteID}",
        data={
            "title":"EDITED Test Post",
            "note":"This is a test edit note, for testing edit endpoint in pytest, and this is the edited text",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Failed to edit note" not in response.data.decode("utf-8")
    assert "Note created successfully" in response.data.decode("utf-8")
    assert "EDITED Test Post" in response.data.decode("utf-8")


def test_delete_note_get_not_logged_in(client):
    """
    Test the 'delete_note_get_not_logged_in' function.

    Parameters:
    - client: The Flask test client.

    Returns:
    - None

    Raises:
    - AssertionError: If any of the assertions fail.

    Description:
    This function tests the behavior of the 'delete_note_get_not_logged_in' function when 
    the user is not logged in. It sends a GET request to the '/notes/delete/1' endpoint
    and checks various assertions to ensure that the expected error message is displayed
    and the response status code is correct.

    Assertions:
    - The response status code should be 200.
    - The string "You need to be logged in to view this page." should be present in the decoded response data.
    - The string "Login" should be present in the decoded response data.
    """
    response = client.get("/notes/delete/1", follow_redirects=True)
    assert "You need to be logged in to view this page." in response.data.decode(
        "utf-8"
    )
    assert "Login" in response.data.decode("utf-8")
    assert response.status_code == 200


def test_delete_note_post_success(client, log_in_test_user, dbsession):
    """
    Test the successful deletion of a note.

    This function tests the delete endpoint in pytest by creating a note and then deleting it.
    It verifies that the note is successfully deleted and no longer present in the response data.
    Additionally, it checks if the note is also deleted from the database.

    Parameters:
    - client: The Flask test client.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session.

    Returns:
    None

    Raises:
    None
    """
    note = Note(
        title="Test Delete Note",
        text="This is a test delete note, for testing delete endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    response = client.get(f"/notes/delete/{note.noteID}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Failed to delete note" not in response.data.decode("utf-8")
    assert "Note deleted successfully" in response.data.decode("utf-8")
    assert "Test Delete Note" not in response.data.decode("utf-8")
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title="Test Delete Note").first()
    assert note is None


def test_delete_note_post_fail(client, log_in_test_user, dbsession):
    """
    Test the failure case of deleting a note.

    This function tests the scenario where a user tries to delete a note that they are
    not authorized to delete. It creates a test note, sets up a different user session,
    and sends a request to delete the note. The function then asserts that the response
    status code is 200, the home page is displayed, an error message indicating lack of
    authorization is present in the response, the success message for deleting the note
    is not present in the response, and the test note is still present in the database.

    Parameters:
    - client: The Flask test client.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session.

    Returns:
    None

    Raises:
    None
    """
    note = Note(
        title="Test Delete Note Fail",
        text="This is a test delete note, for testing delete endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    # prøver at slette med en anden bruger
    with client.session_transaction() as session:
        session["user"] = "testuserNotes2"
        session["userID"] = 9998
        session["userEmail"] = "testusernotes2@test.com"
        session["roleID"] = 1
    response = client.get(f"/notes/delete/{note.noteID}", follow_redirects=True)

    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "You are not authorized to delete this note" in response.data.decode("utf-8")
    assert "Note deleted successfully" not in response.data.decode("utf-8")
    assert "Test Delete Note Fail" in response.data.decode("utf-8")
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title="Test Delete Note Fail").first()
    assert note is not None
    assert note.title == "Test Delete Note Fail"


def test_delete_note_admin(client, log_in_test_user, dbsession):
    """
    Test the delete note functionality for an admin user.

    Args:
        client: The Flask test client.
        log_in_test_user: A fixture that logs in a test user.
        dbsession: The database session.

    Returns:
        None

    Raises:
        AssertionError: If any of the assertions fail.

    Example:
        test_delete_note_admin(client, log_in_test_user, dbsession)
    """
    note = Note(
        title="Test Delete Note Admin",
        text="This is a test delete note, for testing delete endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    # prøver at slette med en admin (roleID = 2)
    with client.session_transaction() as session:
        session["user"] = "testuserNotesAdmin"
        session["userID"] = 9997
        session["userEmail"] = "admin@test.com"
        session["roleID"] = 2
    response = client.get(f"/notes/delete/{note.noteID}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hjem" in response.data
    assert "Note deleted successfully" in response.data.decode("utf-8")
    assert "Test Delete Note Admin" not in response.data.decode("utf-8")
    # for god ordens skyld tjekker vi også om noten er i databasen på den direkte måde
    note = dbsession.query(Note).filter_by(title="Test Delete Note Admin").first()
    assert note is None


def test_search_result_success(client, log_in_test_user, dbsession):
    """
    Test the success of the search result endpoint.

    This function tests the search result endpoint by creating a test note, 
    adding it to the database, and then making a GET request to the search 
    endpoint with a specific query. It asserts that the response status code
    is 200 and that the expected search note and search text are present in the response data.
S
    Parameters:
    - client: The Flask test client.
    - log_in_test_user: A fixture that logs in a test user.
    - dbsession: The database session.

    Returns:
    None

    Raises:
    None
    """
    note = Note(
        title="Test Search Note",
        text="This is a test search note, for testing search endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    response = client.get("/notes/search?query=Test Search Note")
    assert response.status_code == 200
    assert "Test Search Note" in response.data.decode("utf-8")
    assert "This is a test search note" in response.data.decode("utf-8")
    assert "Ryd søgning" in response.data.decode("utf-8")


def test_search_result_fail(client, log_in_test_user, dbsession):
    """
    Test the search result when there are no matching notes.

    :param client: The Flask test client.
    :param log_in_test_user: A fixture that logs in a test user.
    :param dbsession: The database session.

    :returns: None
    """
    note = Note(
        title="Test Search Note Fail",
        text="This is a test search note, for testing search endpoint in pytest",
        created=datetime.now(),
        lastedited=datetime.now(),
        imagelink=None,
        author=9999,
    )
    dbsession.add(note)
    dbsession.commit()
    response = client.get("/notes/search?query=Test Search Note XFail")
    assert response.status_code == 200
    assert "Test Search Note Fail" not in response.data.decode("utf-8")
    assert "This is a test search note" not in response.data.decode("utf-8")
    assert "Ryd søgning" not in response.data.decode("utf-8")
    assert "Søgningen gav ingen resultater!" in response.data.decode("utf-8")
    response = client.get("/notes/search?query=TestSearch")
    assert response.status_code == 200
    assert "Test Search Note Fail" not in response.data.decode("utf-8")
    assert "This is a test search note" not in response.data.decode("utf-8")
    assert "Ryd søgning" not in response.data.decode("utf-8")
    assert "Søgningen gav ingen resultater!" in response.data.decode("utf-8")

# pylint: enable=W0613,W0621
