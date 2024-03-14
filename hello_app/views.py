from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from . import app
import os
from .models import Note
from .dbconnect import session

def updateList():
    notes_db = []
    for row in session.query(Note).order_by(Note.noteID):
        notes_db.append(row)
    return notes_db



# Vores landing Page - Der viser listen over noter
@app.route("/")
def home():
    return render_template("home.html", notes = updateList(), datetime = datetime.now())


# Create note
@app.route("/create/", methods=["GET","POST"])
def create_note():

    if request.method == "GET":
        return render_template("createnote.html")

    # Hvis ikke GET, så er det POST, og så kører vi denne logik
    try:

        title = request.form['title']
        note = request.form['note']
        created = datetime.now()
        lastEdited = datetime.now()
        imagelink = request.form['imagelink']
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
        
        note = Note(title = title, text = note, created = created, lastedited = lastEdited, imagelink = imagelink, author = account_ID)
        session.add(note)
        session.commit()
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        session.rollback()
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

    return redirect(url_for('home'))

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id = None):

    # Tager notes fra vores "notes_db" liste. Hvis notes ikke findes, så returneres en failure-besked. Eller laver vi en ny note.
    note = next((note for note in updateList() if note.noteID == int(id)), None)

    if note is None:
        flash('Note not found', 'error')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template("editnote.html", note=note)
    
    elif request.method == "POST":
        try:
            upd = session.query(Note).filter(Note.noteID == id).first()
            upd.title = request.form['title']
            upd.text = request.form['note']
            upd.lastedited = datetime.now()
            upd.imagelink = request.form['imagelink']
            upd.author = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
            session.commit()
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
        note = next((note for note in updateList() if note.noteID == int(id)), None)
        if note is None:
            flash('Note not found', 'error')
            return redirect(url_for('home'))
        else:
            session.delete(note)
            session.commit()
            flash('Note deleted successfully!', 'success')


    return redirect(url_for('home'))




