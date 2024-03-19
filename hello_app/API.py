from datetime import datetime
from flask import Blueprint, jsonify
from .utils import *
from .models import Note

api = Blueprint('api', __name__)

@api.route('/notes', methods=['GET'])
def display_notes():
    all_notes = dbsession.query(Note).all()
    data_list = []
    for note in all_notes:
        data_dict = {
            'noteID': note.noteID,
            'title': note.title,
            'text': note.text,
            'created': note.created.isoformat(),
            'lastedited': note.lastedited.isoformat(),
            'imagelink': note.imagelink,
            'author': note.author,
        }
        data_list.append(data_dict)

    return jsonify(data_list)

def display_note(id): #Laves senere hvor den tager en note
    pass

