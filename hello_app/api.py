from datetime import datetime, timedelta, timezone
from functools import wraps
from html import escape
from logging import log
import traceback
from flask import (
    Blueprint,
    jsonify,
    request,
    make_response
    )
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    create_access_token,
    verify_jwt_in_request
    )
from werkzeug.security import check_password_hash
from flasgger import Swagger
from flasgger import swag_from
from .utils import app, dbsession
from .models import Note, Account

CONNECTION_ERROR = "A Connection Error Has Occured"

api = Blueprint('api', __name__)
swagger = Swagger(app)

# Laver en JWTManager
jwt = JWTManager()
# Indstiller JWT secret key og token expiry date - Senere så skal den flyttes ud af filen for at være sikker
app.config['JWT_SECRET_KEY'] = 'my_secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

# Initialize JWTManager
jwt.init_app(app)

# allows swagger to start up before getting asked for a jwt, will still require a jwt when sending requests
def jwt_or_swagger_required(f):
    """
    Check if the request is from Swagger (potential safety concern,
    but would take more time to fetch jwt with e.g. javascript)

    Parameters:
    - f: The function to be decorated

    Returns:
    - The decorated function

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Check if the request is from Swagger (potential safety concern,
            but would take more time to fetch jwt with e.g. javascript) """
        if 'swagger' in request.url.lower():
            # If from Swagger UI
            return f(*args, **kwargs)
        # If not from Swagger UI, verify jwt
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return decorated_function

# Logger ind og giver brugeren en JWT Token
@api.route('/login', methods=['POST'])
@swag_from('static/swaggerformatting/login.yml')
def login():
    """
    This function handles the login process for the API.

    Parameters:
        - None

    Returns:
        - A JSON response containing an access token if the login is successful.

    Raises:
        - None
    """
    data = request.json
    username = data.get('username') # cant escape directly here cause it cant handle if its None
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username or password missing'}), 400
    
    username = escape(username) # escape for sql injection protection
    password = escape(password)

    account = dbsession.query(Account).filter_by(username=username).first()
    if not account or not check_password_hash(account.password, password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    access_token = create_access_token(
        identity={"username": username, "author": account.accountID}
    )
    return jsonify({'access_token': access_token}), 200

# Test route: Alle kan få adgang hertil
@api.route('/unprotected')
@swag_from('static/swaggerformatting/unprotected.yml')
def unprotected():
    """
    This function is a route that can be accessed by anyone without requiring a valid JWT token. 
    It returns a JSON response with a message indicating that anyone can view this route.

    Parameters:
        None

    Returns:
        A JSON response with a message indicating that anyone can view this route.

    Raises:
        None
    """
    return jsonify({'message': 'Anyone can view this!'})

# Test route: Kun folk med en valid token kan få adgang
@api.route('/protected', methods=['GET'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/protected.yml')
def protected():
    """
    This function is a protected route that requires a valid JWT token for access. 
    It returns the current user's identity as a JSON response.

    Parameters:
        None

    Returns:
        A JSON response containing the current user's identity.

    Raises:
        None
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
# Tager alle noter
@api.route('/notes', methods=['GET'])
@swag_from('static/swaggerformatting/view.yml')
def display_notes():
    """
    This function retrieves all notes from the database and returns them as a JSON response.

    Parameters:
        None

    Returns:
        A JSON response containing all notes in ISO format.

    Raises:
        Exception: If an internal error occurs while retrieving the notes.
    """
    try:
        all_notes = dbsession.query(Note).all()
        note_isoformat = [note.to_isoformat() for note in all_notes]
        return jsonify(note_isoformat)
    except Exception:
        log(traceback.format_exc())
        return CONNECTION_ERROR

# Tager en note fra id
@api.route('/notes/<id>', methods=['GET'])
@swag_from('static/swaggerformatting/viewid.yml')
def display_note(id):
    """
    This function retrieves a note from the database based on the provided ID and returns it as a JSON response.

    Parameters:
        - id (str): The ID of the note to retrieve.

    Returns:
        - A JSON response containing the note in ISO format.

    Raises:
        - Exception: If an internal error occurs while retrieving the note.
    """
    try:
        note_from_id = dbsession.query(Note).filter(Note.noteID == id).all()
        if not note_from_id:
            return jsonify({"message": "Note not found"}), 404
        note_isoformat = [note.to_isoformat() for note in note_from_id] # Tager alle med specifikt id
        return jsonify(note_isoformat)
    except Exception:
        log(traceback.format_exc())
        return CONNECTION_ERROR

"""
Tager title, text og imagelink til at lave en post request
(curl kan eksempelvis bruges. Check "curl requests.md" i Artefakter/API)
"""
@api.route('/notes/create', methods=['POST'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/create.yml')
def create_note():
    """
    Create a new note in the database.

    Parameters:
        None

    Returns:
        A JSON response containing the details of the newly created note, 
        including the note ID, image link, text, title, author, and a success message.

    Raises:
        Exception: If an internal error occurs while creating the note.
    """
    current_user = get_jwt_identity()
    try:
        note = request.json
        title = escape(note.get('title'))
        text = escape(note.get('text'))
        created = datetime.now(timezone.utc)
        lastedited = datetime.now(timezone.utc)
        imagelink = escape(note.get('imagelink',""))
        author = current_user['author']

        new_note = Note(
            title=title,
            text=text,
            created=created,
            lastedited=lastedited,
            imagelink=imagelink,
            author=author,
        )

        dbsession.add(new_note)
        dbsession.commit()
        return (
            jsonify(
                {
                    "noteID": new_note.noteID,
                    "imagelink": new_note.imagelink,
                    "text": new_note.text,
                    "titel": new_note.title,
                    "author": new_note.author,
                    "message": "Note created successfully",
                }
            ),
            201,
        )
    except AttributeError:
        return jsonify({"message": "Invalid data"}), 400 # Hvis der mangler data der hvor deres bruger escape metoden
    except Exception:
        dbsession.rollback()
        log(traceback.format_exc())
        return CONNECTION_ERROR

# Sletter en note ud fra id
@api.route('/notes/<id>', methods=['DELETE'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/delete.yml')
def delete_note(id):
    """
    Delete a note from the database based on the provided ID.

    Parameters:
        - id (str): The ID of the note to delete.

    Returns:
        - A response indicating the success or failure of the deletion.

    Raises:
        - Exception: If an internal error occurs while deleting the note.
    """
    current_user = get_jwt_identity() # takes author id from jwt
    try:
        note_author_query = dbsession.query(Note).filter(Note.author == current_user['author']).first()
        if note_author_query is None:
            return "The author does not exist"

        note = dbsession.query(Note).filter(Note.noteID == id).first()

        if note is None:
            return "The note does not exist"

        if current_user['author'] != note.author:
            return "Current user is not the author of note"

        dbsession.delete(note)
        dbsession.commit()

        return make_response("Note with id:" + escape(id) + " has been deleted", 200)
    except Exception:
        dbsession.rollback()
        log(traceback.format_exc())
        return CONNECTION_ERROR

# Redigere en eksisterende note ud fra id og input
@api.route('/notes/<id>', methods=['PUT'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/editid.yml')
def edit_note(id):
    """
    Edit a note in the database based on the provided ID and input.

    Parameters:
        - id (str): The ID of the note to edit.

    Returns:
        - A JSON response containing the updated details of the note,
        including the updated title, text, image link, and a success message.

    Raises:
        - Exception: If an internal error occurs while editing the note.
    """
    current_user = get_jwt_identity() # takes author id from jwt
    try:
        note_author_query = dbsession.query(Note).filter(Note.author == current_user['author']).first()
        if note_author_query is None:
            return jsonify({"message": "The author does not exist"}), 404

        edit_query = dbsession.query(Note).filter(Note.noteID == id).first()

        if edit_query is None:
            return jsonify({"message": "Note not found"}), 404

        if current_user['author'] != edit_query.author:
            return "Current user is not author of the note"
        note = request.json
        title = escape(note.get('title'))
        text = escape(note.get('text'))
        lastedited = datetime.now(timezone.utc)
        imagelink = escape(note.get('imagelink'))

        # Laves så kun ændrede data tabeller bliver ændret(ellers gør den det andet tomt)
        edit_query.title = title
        edit_query.text = text
        edit_query.imagelink = imagelink
        edit_query.lastedited = lastedited

        dbsession.commit()

        return jsonify(
            {
                "titel": title,
                "text": text,
                "imagelink": imagelink,
                "message": "Note edited successfully",
            }
        )
    except Exception:
        dbsession.rollback()
        log(traceback.format_exc())
        return "An internal error has occurred!"
