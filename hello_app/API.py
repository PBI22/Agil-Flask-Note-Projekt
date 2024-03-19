from datetime import datetime
from flask import Blueprint, jsonify, request
from .utils import *
from .models import Note

api = Blueprint('api', __name__)

# Tager alle noter
@api.route('/view', methods=['GET'])
def display_notes():
    all_notes = dbsession.query(Note).all()
    note_isoformat = [note.to_isoformat() for note in all_notes]
    return jsonify(note_isoformat)

# Tager en note fra id
@api.route('/view/<id>', methods=['GET'])
def display_note(id):
    print("ID: " + id)
    note_from_id = dbsession.query(Note).filter(Note.noteID == id).all()
    note_isoformat = [note.to_isoformat() for note in note_from_id]
    return jsonify(note_isoformat)

# Tager title, text og imagelink til at lave en post request(curl kan eksempelvis bruges. Check "curl requests.md" i Artefakter/API)
@api.route('/create', methods=['POST'])
def create_note():
    note = request.json
    title = note.get('title')
    text = note.get('text')
    created = datetime.now()
    lastedited = datetime.now()
    imagelink = note.get('imagelink')
    author = 1

    new_note = Note(title = title, text = text, created = created, lastedited = lastedited, imagelink = imagelink, author = author)

    dbsession.add(new_note)
    dbsession.commit()
    return jsonify({'message': 'Note created successfully', 'noteID': new_note.noteID}), 201
