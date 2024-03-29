# Utility functions
from .dbconnect import dbsession
from .models import Note, Account
from flask import flash, session, redirect, url_for
from .auth import login_required
from datetime import datetime
from . import app
    
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
        imagelink = request.form.get('imagelink',None) # None hvis der ikke er noget
        account_ID = session['userID']     
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = account_ID)
        dbsession.add(note)
        dbsession.commit()
        
        flash('Note created successfully!', 'success') 
    except Exception as e:
        dbsession.rollback()
        flash(f'Failed to create note: {str(e)}', 'error') 
        app.logger.error(f"Failed to create note: {e} from user: {session['user']}")

@login_required
def edit_note_post(request, id):
    try:
        upd = dbsession.query(Note).filter(Note.noteID == id).first()
        userID = session['userID']
        userRole = session['roleID']
        if userID == upd.author or userRole == 2:#admin skal tages fra db 
            upd = dbsession.query(Note).filter(Note.noteID == id).first()
            upd.title = request.form['title']
            upd.text = request.form['note']
            upd.lastedited = datetime.now()
            upd.imagelink = request.form.get('imagelink',None)
            dbsession.commit()
            flash('Note created successfully!', 'success') 
        else:
            flash('You are not authorized to edit this note', 'error')
    except Exception as e:
        flash(f'Failed to edit note: {str(e)}', 'error')
        app.logger.error(f"Failed to edit note: {e} from user: {session['user']}")
        
def find_note(id):
    try:
        note = next((note for note in updateList() if note.noteID == int(id)), None)
    except Exception as e:
        app.logger.error(f"Failed to find note: {e} from user: {session['user']}")
    return note

def searchbar(query):
    try:
        search_results = dbsession.query(Note).filter(Note.title.contains(query) | Note.text.contains(query) | Account.username.contains(query)).all()
    except Exception as e:
        app.logger.error(f"Failed to search for: {query} from user: {session['user']}")
    return search_results
