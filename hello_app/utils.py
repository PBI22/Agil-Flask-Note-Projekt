# Utility functions
import json
import random
import string
from .dbconnect import dbsession
from .models import Note
from flask import flash, session
from datetime import datetime
from . import app
from werkzeug.utils import secure_filename
import os
from .blobton import ACCOUNT, CONTAINER, blob_service


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

        title = request.form['title']
        note = request.form['note']
        
        files_list = []  # Initialize an empty list to store file dictionaries

        if 'file' in request.files:
            files = request.files.getlist("file")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    fileextension = filename.rsplit('.', 1)[1]
                    Randomfilename = id_generator()
                    filename = Randomfilename + '.' + fileextension
                    ref = 'http://' + ACCOUNT + '.blob.core.windows.net/' + CONTAINER + '/' + filename
                    file_dump = {
                        "Type": fileextension,
                        "Name": filename,
                        "Link": ref
                    }
                    try:
                        blob_client = blob_service.get_blob_client(container=CONTAINER, blob=filename)
                        blob_client.upload_blob(file)
                        files_list.append(file_dump)  # Append the file dictionary to the list
                    except Exception as e:
                        flash('Exception=' + str(e))
                        pass
                    
        created = datetime.now()
        lastEdited = datetime.now()
        files_json = json.dumps(files_list)
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = files_json, author = account_ID)
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
        upd.author = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        dbsession.commit()
        flash('Note created successfully!', 'success')  # Viser en success-besked
    
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
# Generates random name for files in our Blob Storage         
def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))