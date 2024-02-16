from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from . import app
import os

@app.route("/")
def home():
    
    filename = os.path.join(app.static_folder, 'note.json')

    try:
        with open(filename, 'r') as file:
                notes = json.load(file)

    except FileNotFoundError:
        print("Note fil ikke fundet!")
        notes = {}

    return render_template("home.html", notes = notes)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/note/")
def note():
    return render_template("note.html")

@app.route("/create/")
def create():
    return render_template("createnote.html")

@app.route("/create/", methods=["POST"])
def create_note():
    try:
        name = request.form['name']
        note = request.form['note']
        author = request.form['author']
        created = datetime.now()

        filename = os.path.join(app.static_folder, 'note.json')

        with open(filename, 'r') as file:
            notes = json.load(file)

        notes[name] = {
            "note": note,
            "author": author,
            "created": created.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(filename, 'w') as file:
            json.dump(notes, file, indent=4, ensure_ascii=False)
        
        flash('Note created successfully!', 'success')  # Viser en success-besked
    except Exception as e:
        flash(f'Failed to create note: {str(e)}', 'error')  # Viser en failure-besked

    return redirect(url_for('home'))

@app.route("/edit/")
def edit():
    return render_template("editnote.html")

@app.route("/view/")
def view():
    return render_template("viewnote.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
@app.route("/edit/<name>")
def get_edit(name = None):
    if name is None:
        flash(f"Failed to edit - Note is None")  # Viser en failure-besked

        return redirect(url_for('home')) 
    filename = os.path.join(app.static_folder, 'note.json')

    try:
        with open(filename, 'r') as file:
                notes = json.load(file)

    except FileNotFoundError:
        flash(f"Note file not found")
        notes = {}

    return render_template("editnote.html", name,notes)