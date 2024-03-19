# Utility functions
from .dbconnect import dbsession
<<<<<<< HEAD
from .models import Note,Account
from flask import flash,session
from datetime import datetime


def load_md_template(filename):
    folder = "md_templates/"
    with open(folder + filename + ".md", "r",encoding='utf-8') as file:
        skabelon_md = file.read()
        return skabelon_md    
    
=======
from .models import Note
from flask import flash, session
from datetime import datetime
from . import app
>>>>>>> b4f2c461131d9ea4c6917e1921e3e676690c1d00
    
def updateList():
    
    try:
        notes_db = []
        for row in dbsession.query(Note).order_by(Note.noteID):
            notes_db.append(row)
    except Exception as e:
        app.logger.critical(f"Failed to update list: {e}")
    return notes_db


def create_note_post(request):
    try:

        title = request.form['title']
        note = request.form['note']
        created = datetime.now()
        lastEdited = datetime.now()
        imagelink = request.form['imagelink']
        #account = dbsession.query(Account).filter_by(username=session['user']).first()
        account_ID = session['userID']
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = account_ID  )
        dbsession.add(note)
        dbsession.commit()
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        dbsession.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked
        app.logger.error(f"Failed to create note: {e} from user: {session['user']}")

def edit_note_post(request, id):
    try:
        upd = dbsession.query(Note).filter(Note.noteID == id).first()
        upd.title = request.form['title']
        upd.text = request.form['note']
        upd.lastedited = datetime.now()
        upd.imagelink = request.form['imagelink']
        dbsession.commit()
        flash('Note updated successfully!', 'success')  # Viser en success-besked
    
    except Exception as e:
        flash(f'Failed to edit note: {str(e)}', 'error')  # Viser en failure-besked
        app.logger.error(f"Failed to edit note: {e} from user: {session['user']}")
        
def find_note(id):
    try:
        note = next((note for note in updateList() if note.noteID == int(id)), None)
    except Exception as e:
        app.logger.error(f"Failed to find note: {e} from user: {session['user']}")
    return note

def searchbar(query):
    try:
        search_results = dbsession.query(Note).filter(Note.title.contains(query) | Note.text.contains(query)).all()
    except Exception as e:
        app.logger.error(f"Failed to search for: {query} from user: {session['user']}")
    return search_results