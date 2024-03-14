from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from . import app
import os
from .models import Note
import markdown2


"""
simple funktion der lige loader en "markdown skabelon, som demonstration
inden databasen er implementeret.

"""
def load_md_template(filename):
    folder = "md_templates/"
    with open(folder + filename + ".md", "r",encoding='utf-8') as file:
        skabelon_md = file.read()
        return skabelon_md    

"""
Midlertidig Datastorage Liste med Test notes 

"""
notes_db = [
    Note(1, "Note 1", "This is a note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(2, "Note 2", "This is another note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(3, "Note 3", "This is yet another note", datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(4, "Note 4", load_md_template('skabelon_note'), datetime.now(), datetime.now(), "https://via.placeholder.com/150", 1),
    Note(5, "SLA", load_md_template('sla'), datetime.now(), datetime.now(),None, 1)
]




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

        created = datetime.now()
        lastEdited = datetime.now()
        imagelink = request.form['imagelink']
        account_ID = 1 # skal ændres senere når vi implementere brugerlogin - 1 er Guest pt
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

    #Tjekker hvis det er et markdown note (som markeres med !MD i starten af teksten)
    if note.text.startswith("!MD"):
        note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
        return render_template("mdnote.html", note=note, note_markdown=note_markdown)
    else:
        return render_template("mdnote.html", note=note, note_markdown=note.text)

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




