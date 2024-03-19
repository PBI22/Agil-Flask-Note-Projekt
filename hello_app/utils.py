# Utility functions
from .dbconnect import dbsession
from .models import Note
from flask import flash, session, url_for, redirect
from datetime import datetime
from . import app   
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
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = account_ID)
        dbsession.add(note)
        dbsession.commit()
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        dbsession.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked



#check id and role before allowing edit
def edit_note_post(request, id):
    try:
        if 'user' not in session:
            flash('Error: You are not logged in.')
            return redirect(url_for('login'))
        upd = dbsession.query(Note).filter(Note.noteID == id).first()
        user = session['user']
        if user['username'] == upd.author or user['role'] == 'Admin':

        

            upd = dbsession.query(Note).filter(Note.noteID == id).first()
            upd.title = request.form['title']
            upd.text = request.form['note']
            upd.lastedited = datetime.now()
            upd.imagelink = request.form['imagelink']
            upd.author = user['username'] # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
            dbsession.commit()
            flash('Note created successfully!', 'success')  # Viser en success-besked
        else:
            flash('You are not authorized to edit this note', 'error')
    
    except Exception as e:
        flash(f'Failed to edit note: {str(e)}', 'error')  # Viser en failure-besked
        app.logger.error(f"Failed to edit note: {e} from user: {session['user']}")




def find_note(id):
    note = next((note for note in updateList() if note.noteID == int(id)), None)
    return note

def searchbar(query):
    search_results = dbsession.query(Note).filter(Note.title.contains(query) | Note.text.contains(query)).all()
    return search_results