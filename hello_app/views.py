from datetime import datetime
<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
=======
from flask import Flask, render_template, json
>>>>>>> feature-3.3-layout
from . import app
import json

# Opening JSON file
f = open('note.json')
 
# returns JSON object as 
# a dictionary
notes = json.load(f)
 
# Iterating through the json
# list
for i in notes:
    print(i)

@app.route("/")
def home():
    return render_template("home.html", len = len(notes), notes = notes)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/create/")
def create():
    return render_template("createnote.html")

@app.route("/create/", methods=["POST"])
def create_note():
    name = request.form['name']
    note = request.form['note']
    author = request.form['author']
    created = datetime.now()

    # Stien til din JSON-fil
    filepath = 'static/note.json'

    # Læs den eksisterende data
    with open(filepath, 'r') as file:
        notes = json.load(file)
    
    # Tilføj den nye note
    notes[name] = {
        "note": note,
        "author": author,
        "created": created.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Skriv det opdaterede dictionary tilbage til filen
    with open(filepath, 'w') as file:
        json.dump(notes, file, indent=4, ensure_ascii=False)

    return redirect(url_for('home'))

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
