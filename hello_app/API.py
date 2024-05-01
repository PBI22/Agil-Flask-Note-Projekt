from datetime import datetime, timedelta
from functools import wraps
from html import escape
from logging import log
from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import check_password_hash
from .utils import app, dbsession
from .models import Note, Account
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, verify_jwt_in_request
import traceback
from flasgger import Swagger
from flasgger import swag_from

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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the request is from Swagger (potential safety concern, but would take more time to fetch jwt with e.g. javascript)
        if 'swagger' in request.url.lower():
            # If from Swagger UI
            return f(*args, **kwargs)
        else:
            # If not from Swagger UI, verify jwt
            verify_jwt_in_request()
            return f(*args, **kwargs)
    return decorated_function

# Logger ind og giver brugeren en JWT Token
@api.route('/login', methods=['POST'])
@swag_from('static/swaggerformatting/login.yml')
def login():
    data = request.json
    username = escape(data.get('username'))
    password = escape(data.get('password'))

    if not username or not password:
        return jsonify({'message': 'Username or password missing'}), 400

    account = dbsession.query(Account).filter_by(username=username).first()
    if not account or not check_password_hash(account.password, password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    access_token = create_access_token(identity={'username': username, 'author': account.accountID})
    return jsonify({'access_token': access_token}), 200 

# Test route: Alle kan få adgang hertil
@api.route('/unprotected')
@swag_from('static/swaggerformatting/unprotected.yml')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

# Test route: Kun folk med en valid token kan få adgang
@api.route('/protected', methods=['GET'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/protected.yml')
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
# Tager alle noter
@api.route('/notes', methods=['GET'])
@swag_from('static/swaggerformatting/view.yml')
def display_notes():
    try:
        all_notes = dbsession.query(Note).all()
        note_isoformat = [note.to_isoformat() for note in all_notes]
        return jsonify(note_isoformat)
    except Exception as e:
        log(traceback.format_exc())
        return "An internal error has occurred!"

# Tager en note fra id
@api.route('/notes/<id>', methods=['GET'])
@swag_from('static/swaggerformatting/viewid.yml')
def display_note(id):
    try:
        note_from_id = dbsession.query(Note).filter(Note.noteID == id).all()
        note_isoformat = [note.to_isoformat() for note in note_from_id] # Tager alle med specifikt id, det virker det dårligt men gider ikke
        return jsonify(note_isoformat)
    except Exception as e:
        log(traceback.format_exc())
        return "An internal error has occurred!"
# Tager title, text og imagelink til at lave en post request(curl kan eksempelvis bruges. Check "curl requests.md" i Artefakter/API)
@api.route('/notes/create', methods=['POST'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/create.yml')
def create_note():
    current_user = get_jwt_identity()
    try:
        note = request.json
        title = escape(note.get('title'))
        text = escape(note.get('text'))
        created = datetime.now()
        lastedited = datetime.now()
        imagelink = escape(note.get('imagelink'))
        author = current_user['author']

        new_note = Note(title = title, text = text, created = created, lastedited = lastedited, imagelink = imagelink, author = author)

        dbsession.add(new_note)
        dbsession.commit() 
        return jsonify({'noteID': new_note.noteID, 'Imagelink': new_note.imagelink,'Text': new_note.text, 'Titel': new_note.title, 'Author': new_note.author, 'Message': 'Note created successfully'}), 201
    except Exception as e:
        dbsession.rollback()
        log(traceback.format_exc())
        return "An internal error has occurred!"

# Sletter en note ud fra id
@api.route('/notes/<id>', methods=['DELETE'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/delete.yml')
def delete_note(id):
    current_user = get_jwt_identity() # takes author id from jwt
    try: #if session['roleID'] == 2 or session['userID'] == note.author:
        note = dbsession.query(Note).filter(Note.noteID == id).first()
        if note.author == current_user['author']: # checks note author against jwt author
            dbsession.delete(note)
            dbsession.commit()
            return make_response("Note with id:" + escape(id) + " has been deleted", 200)
        else:
            return "Error deleting note, not authorized to delete this, contact the author instead", 404
    except Exception as e:
        dbsession.rollback()
        log(traceback.format_exc())
        return "An internal error has occurred!"
    except:
            return "Error deleting note", 404

# Redigere en eksisterende note ud fra id og input
@api.route('/notes/<id>', methods=['PUT'])
@jwt_or_swagger_required
@swag_from('static/swaggerformatting/editid.yml')
def edit_note(id):
    try:
        edit_query = dbsession.query(Note).filter(Note.noteID == id).first()

        if not edit_query:
            return jsonify({"message": "Note not found"}), 404
        
        note = request.json
        title = escape(note.get('title'))
        text = escape(note.get('text'))
        lastedited = datetime.now()
        imagelink = escape(note.get('imagelink'))

        # Laves så kun ændrede data tabeller bliver ændret(ellers gør den det andet tomt)
        if title is not None:
            edit_query.title = title
        if text is not None:
            edit_query.text = text
        if imagelink is not None:
            edit_query.imagelink = imagelink
        edit_query.lastedited = lastedited

        dbsession.commit()

        return jsonify({'Titel': title, 'Text': text, 'Imagelink': imagelink, 'Message': 'Note edited successfully'})
    except Exception as e:
        dbsession.rollback()
        log(traceback.format_exc())
        return "An internal error has occurred!"