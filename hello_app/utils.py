# Utility functions
from .dbconnect import dbsession
from .models import Note
from flask import flash
from datetime import datetime
from flask_login import current_user


def load_md_template(filename):
    folder = "md_templates/"
    with open(folder + filename + ".md", "r",encoding='utf-8') as file:
        skabelon_md = file.read()
        return skabelon_md    
    
    
def updateList():
    notes_db = []
    for row in dbsession.query(Note).order_by(Note.noteID):
        notes_db.append(row)
    return notes_db


def create_note_post(request):
    try:

        title = request.form['title']
        note = request.form['note']
        # Temp input, skal fjernes senere hen
        if note[:3] == "!S!":
            note = load_md_template('skabelon_note')
        created = datetime.now()
        lastEdited = datetime.now()
        imagelink = request.form['imagelink']
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = current_user.id)
        dbsession.add(note)
        dbsession.commit()
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        dbsession.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

def edit_note_post(request, id):
    try:
        upd = dbsession.query(Note).filter(Note.noteID == id).first()
        upd.title = request.form['title']
        upd.text = request.form['note']
        upd.lastedited = datetime.now()
        upd.imagelink = request.form['imagelink']
        dbsession.commit()
        flash('Note created successfully!', 'success')  # Viser en success-besked
    
    except Exception as e:
        flash(f'Failed to edit note: {str(e)}', 'error')  # Viser en failure-besked
        
def find_note(id):
    note = next((note for note in updateList() if note.noteID == int(id)), None)
    return note

def searchbar(query):
    search_results = dbsession.query(Note).filter(Note.title.contains(query) | Note.text.contains(query)).all()
    return search_results