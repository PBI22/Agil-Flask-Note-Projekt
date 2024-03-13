from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from werkzeug.utils import secure_filename
from . import app
import os
from .models import Note
from azure.storage.blob import BlobServiceClient
import string, random, requests

"""
Midlertidig Datastorage Liste med 3 Test notes i en liste

"""

notes_db = [
    Note(1, "Note 1", "This is a note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(2, "Note 2", "This is another note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(3, "Note 3", "This is yet another note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1)
]

UPLOAD_FOLDER = '/path/to/the/uploads' # Ændres til Blob Storage
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Kun billede filer


account = 'flasknoteblobstorage'   # Azure account name
container = "images" # Container name
connection_string = "DefaultEndpointsProtocol=https;AccountName=flasknoteblobstorage;AccountKey=BnJBe5WkjWApSRwguDmueGabw3+WZmnIE3GwjfnMezNM1Td+xO8TdrHKQiDGyomo7ZBxGjGIQuiJ+AStd6P1kA==;EndpointSuffix=core.windows.net"

blob_service = BlobServiceClient.from_connection_string(conn_str=connection_string)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Vores landing Page - Der viser listen over noter
@app.route("/")
def home():
    return render_template("home.html", notes = notes_db, datetime = datetime.now())


# Create note
@app.route("/create/", methods=["GET","POST"])
def create_note():

    if request.method == "GET":
        return render_template("createnote.html")

    # Hvis ikke GET, så er det POST, og så kører vi denne logik
    try:
        title = request.form['title']
        note = request.form['note']
        ref = '' # Tomt reference link når intet billede er valgt
        
        
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fileextension = filename.rsplit('.',1)[1]
                Randomfilename = id_generator()
                filename = Randomfilename + '.' + fileextension
                ref = 'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
                try:
                    blob_client = blob_service.get_blob_client(container=container, blob=filename)
                    blob_client.upload_blob(file)
                except Exception as e:
                    flash('Exception=' + str(e))
                    pass
                

        created = datetime.now()
        lastEdited = datetime.now()
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        imagelink = ref
        notes_db.append(Note(len(notes_db) + 1, title, note, created, lastEdited, imagelink, account_ID))
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

    return redirect(url_for('home'))


@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id = None):

    # Tager notes fra vores "notes_db" liste. Hvis notes ikke findes, så returneres en failure-besked. Eller laver vi en ny note.
    note = next((note for note in notes_db if note.id == int(id)), None)

    if note is None:
        flash('Note not found', 'error')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template("editnote.html", note=note)
    
    elif request.method == "POST":
        
        try:
            note.title = request.form['title']
            note.text = request.form['note']
            note.lastEdited = datetime.now()
            note.imagelink = request.form['imagelink']
            note.account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt

            flash('Note created successfully!', 'success')  # Viser en success-besked
            return redirect(url_for('home'))
    
        except Exception as e:
            flash(f'Failed to edit note: {str(e)}', 'error')  # Viser en failure-besked
    else:
        flash("Invalid request method")
        return redirect(url_for('home'))

@app.route("/view/<id>")
def view(id = None):
    note = next((note for note in notes_db if note.id == int(id)), None)
    return render_template("note.html", note=note)


@app.route("/delete/<id>")
def delete_note(id = None):
    
    if id is None:
        flash('Id is invalid', 'error')
        return redirect(url_for('home'))
    else:
        note = next((note for note in notes_db if note.id == int(id)), None)
        if note is None:
            flash('Note not found', 'error')
            return redirect(url_for('home'))
        else:
            notes_db.remove(note)
            flash('Note deleted successfully!', 'success')


    return redirect(url_for('home'))




def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))