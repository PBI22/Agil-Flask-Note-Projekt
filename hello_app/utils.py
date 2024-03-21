# Utility functions
import json
from .dbconnect import dbsession
from .models import Note
from flask import flash, session, redirect, url_for
from .auth import login_required
from datetime import datetime
from werkzeug.utils import secure_filename
from .blobton import ACCOUNT, CONTAINER
from . import app
    
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'} 
    
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
        files_list = []  
        title = request.form['title']
        note_text = request.form['note']
        filenames = request.form.getlist('filenames')  # Get the filenames
        for file, filename in zip(request.files.getlist("file"), filenames):
            if file and allowed_file(file.filename):
                filename = secure_filename(filename)
                fileextension = filename.rsplit('.', 1)[1]
                ref = 'http://' + ACCOUNT + '.blob.core.windows.net/' + CONTAINER + '/' + filename
                file_dump = {
                    "Type": fileextension,
                    "Name": filename,
                    "Link": ref
                }
                try:
                    files_list.append(file_dump)  # Append the file dictionary to the list
                except Exception as e:
                    flash('Exception=' + str(e))
                    pass

        created = datetime.now()
        last_edited = datetime.now()
        account_ID = 1  # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt

        # Convert the list of file dictionaries to JSON
        files_json = json.dumps(files_list)

        # Create the Note object with the list of files as JSON
        note = Note(title=title, text=note_text, created=created, lastedited=last_edited, imagelink=files_json, author=account_ID)
        dbsession.add(note)
        dbsession.commit()

        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        dbsession.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

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
        search_results = dbsession.query(Note).filter(Note.title.contains(query) | Note.text.contains(query)).all()
    except Exception as e:
        app.logger.error(f"Failed to search for: {query} from user: {session['user']}")
    return search_results

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS