# Utility functions
import string, random
from .dbconnect import session
from .models import Note
from flask import flash, redirect, url_for
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Kun billede filer


account = 'flasknoteblobstorage'   # Azure account name
container = "images" # Container name
connection_string = "DefaultEndpointsProtocol=https;AccountName=flasknoteblobstorage;AccountKey=BnJBe5WkjWApSRwguDmueGabw3+WZmnIE3GwjfnMezNM1Td+xO8TdrHKQiDGyomo7ZBxGjGIQuiJ+AStd6P1kA==;EndpointSuffix=core.windows.net"

blob_service = BlobServiceClient.from_connection_string(conn_str=connection_string)


def load_md_template(filename):
    folder = "md_templates/"
    with open(folder + filename + ".md", "r",encoding='utf-8') as file:
        skabelon_md = file.read()
        return skabelon_md    
    
    
def updateList():
    notes_db = []
    for row in session.query(Note).order_by(Note.noteID):
        notes_db.append(row)
    return notes_db


def create_note_post(request):
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

        # Temp input, skal fjernes senere hen
        if note[:3] == "!S!":
            note = load_md_template('skabelon_note')
        created = datetime.now()
        lastEdited = datetime.now()
        imagelink = ref
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = account_ID)
        session.add(note)
        session.commit()
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        session.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

def edit_note_post(request, id):
    try:
        upd = session.query(Note).filter(Note.noteID == id).first()
        upd.title = request.form['title']
        upd.text = request.form['note']
        upd.lastedited = datetime.now()
        upd.imagelink = request.form['imagelink']
        upd.author = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        session.commit()
        flash('Note created successfully!', 'success')  # Viser en success-besked
    
    except Exception as e:
        flash(f'Failed to edit note: {str(e)}', 'error')  # Viser en failure-besked
        
def find_note(id):
    note = next((note for note in updateList() if note.noteID == int(id)), None)
    return note

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))