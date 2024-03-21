from datetime import datetime
from flask import Blueprint, jsonify, request
from .utils import *
from .models import Note
from sqlalchemy.exc import SQLAlchemyError

api = Blueprint('api', __name__)

# Tager alle noter
@api.route('/view', methods=['GET'])
def display_notes():
    try:
        all_notes = dbsession.query(Note).all()
        note_isoformat = [note.to_isoformat() for note in all_notes]
        return jsonify(note_isoformat)
    except SQLAlchemyError as e:
        return jsonify({'Error': str(e)}), 500


# Tager en note fra id
@api.route('/view/<id>', methods=['GET'])
def display_note(id):
    try:
        note_from_id = dbsession.query(Note).filter(Note.noteID == id).all()
        note_isoformat = [note.to_isoformat() for note in note_from_id] # Tager alle med specifikt id, det virker det dårligt men gider ikke
        return jsonify(note_isoformat)
    except SQLAlchemyError as e:
        return jsonify({'Error': str(e)}), 500
# Tager title, text og imagelink til at lave en post request(curl kan eksempelvis bruges. Check "curl requests.md" i Artefakter/API)
@api.route('/create', methods=['POST'])
def create_note():
    try:
        note = request.json
        title = note.get('title')
        text = note.get('text')
        created = datetime.now()
        lastedited = datetime.now()
        imagelink = note.get('imagelink')
        author = note.get('author')

        new_note = Note(title = title, text = text, created = created, lastedited = lastedited, imagelink = imagelink, author = author)

        dbsession.add(new_note)
        dbsession.commit() 
        return jsonify({'message': 'Note created successfully', 'noteID': new_note.noteID}), 201
    except SQLAlchemyError as e:
        dbsession.rollback()
        return jsonify({'Error': str(e)}), 500

# Sletter en note ud fra id (muligvis skal der senere tilføjes sikkerhed, så ikke alle kan slette noter ud fra APIen)
@api.route('/delete/<id>')
def delete_note(id):
    try:
        note = dbsession.query(Note).filter(Note.noteID == id).first()
        if note:
            dbsession.delete(note)
            dbsession.commit()
            return "Note with id: " + id + " has been deleted"
        else:
            return "Error deleting note", 404
    except SQLAlchemyError as e:
         dbsession.rollback()
         return str(e), 500
    except:
            return "Error deleting note", 404

# Redigere en eksisterende note ud fra id og input(Kan testes med cURL request i "curl requests.md" fundet i mappen Artefakter/API)
@api.route('/edit/<id>', methods=['PUT'])
def edit_note(id):
    try:
        edit_query = dbsession.query(Note).filter(Note.noteID == id).first()

        if not edit_query:
            return jsonify({"message": "Note not found"}), 404
        
        note = request.json
        title = note.get('title')
        text = note.get('text')
        lastedited = datetime.now()
        imagelink = note.get('imagelink')

        # Laves så kun ændrede data tabeller bliver ændret(ellers gør den det andet tomt)
        if title is not None:
            edit_query.title = title
        if text is not None:
            edit_query.text = text
        if imagelink is not None:
            edit_query.imagelink = imagelink
        edit_query.lastedited = lastedited

        dbsession.commit()

        return jsonify({"message": "Note updated successfully"}), 200
    except SQLAlchemyError as e:
        dbsession.rollback()
        return jsonify({'Error': str(e)}), 500

