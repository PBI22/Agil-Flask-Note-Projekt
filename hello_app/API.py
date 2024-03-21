from datetime import datetime, timedelta
from html import escape
from logging import log
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from .utils import *
from .models import Note, Account
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
import traceback

api = Blueprint('api', __name__)

# Laver en JWTManager
jwt = JWTManager()
# Indstiller JWT secret key og token expiry date - Senere så skal den flyttes ud af filen for at være sikker
app.config['JWT_SECRET_KEY'] = 'my_secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

# Initialize JWTManager
jwt.init_app(app)

# Logger ind og giver brugeren en JWT Token
@api.route('/login', methods=['POST'])
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
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

# Test route: Kun folk med en valid token kan få adgang
@api.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    username = current_user['username']
    author = current_user['author']
    return jsonify({'message': f'Hello, {escape(username)}, your Author id is: {author}! You can only use this with a valid token'}), 200

# Tager alle noter
@api.route('/view', methods=['GET'])
def display_notes():
    try:
        all_notes = dbsession.query(Note).all()
        note_isoformat = [note.to_isoformat() for note in all_notes]
        return jsonify(note_isoformat)
    except Exception as e:
        log(traceback.format_exc())
        return "An internal error has occurred!"

# Tager en note fra id
@api.route('/view/<id>', methods=['GET'])
def display_note(id):
    try:
        note_from_id = dbsession.query(Note).filter(Note.noteID == id).all()
        note_isoformat = [note.to_isoformat() for note in note_from_id] # Tager alle med specifikt id, det virker det dårligt men gider ikke
        return jsonify(note_isoformat)
    except Exception as e:
        log(traceback.format_exc())
        return "An internal error has occurred!"
# Tager title, text og imagelink til at lave en post request(curl kan eksempelvis bruges. Check "curl requests.md" i Artefakter/API)
@api.route('/create', methods=['POST'])
@jwt_required()
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

# Sletter en note ud fra id (muligvis skal der senere tilføjes sikkerhed, så ikke alle kan slette noter ud fra APIen)
@api.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete_note(id):
    try:
        note = dbsession.query(Note).filter(Note.noteID == id).first()
        if note:
            dbsession.delete(note)
            dbsession.commit()
            return "Note with id: " + id + " has been deleted"
        else:
            return "Error deleting note", 404
    except Exception as e:
        dbsession.rollback()
        log(traceback.format_exc())
        return "An internal error has occurred!"
    except:
            return "Error deleting note", 404

# Redigere en eksisterende note ud fra id og input(Kan testes med cURL request i "curl requests.md" fundet i mappen Artefakter/API)
@api.route('/edit/<id>', methods=['PUT'])
@jwt_required()
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