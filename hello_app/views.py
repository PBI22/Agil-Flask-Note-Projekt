import markdown2
import json
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from . import app
from .models import Note
from .utils import *

# Define custom filter to parse JSON
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value)

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
    else:
        create_note_post(request)

    return redirect(url_for('home'))

# Upload file
@app.route("/upload", methods=["GET","POST"])
def upload_file():
    files_list = []  # Initialize an empty list to store file dictionaries
    if 'file' in request.files:
        files = request.files.getlist("file")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fileextension = filename.rsplit('.', 1)[1]
                Randomfilename = id_generator()
                filename = Randomfilename + '.' + fileextension
                ref = 'http://' + account + '.blob.core.windows.net/' + container + '/' + filename
                file_dump = {
                    "Type": fileextension,
                    "Name": filename,
                    "Link": ref
                }
                try:
                    blob_client = blob_service.get_blob_client(container=container, blob=filename)
                    blob_client.upload_blob(file)
                    files_list.append(file_dump)  # Append the file dictionary to the list
                except Exception as e:
                    flash('Exception=' + str(e))
                    pass
    
    # Construct a list of file links
    file_links = [file['Link'] for file in files_list]
    
    # Return a JSON response containing the file links
    return jsonify({'file_links': file_links})

@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id = None):

    note = find_note(id)

    if note is None:
        flash('Note not found', 'error')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template("editnote.html", note=note)
    
    elif request.method == "POST":
        edit_note_post(request, id)

    else:
        flash("Invalid request method")
        
    return redirect(url_for('home'))

@app.route("/view/<id>")
def view(id = None):
    
    note = find_note(id)
    imagelink_data = json.loads(note.imagelink) if note.imagelink else None

    #Tjekker hvis det er et markdown note (som markeres med !MD i starten af teksten)
    if note.text.startswith("!MD"):
        note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
        return render_template("mdnote.html", note=note, note_markdown=note_markdown, imagelink_data=imagelink_data)
    else:
        return render_template("mdnote.html", note=note, note_markdown=note.text, imagelink_data=imagelink_data)


@app.route("/delete/<id>")
def delete_note(id = None):
    
    if id is None:
        flash('Id is invalid', 'error')
        return redirect(url_for('home'))
    else:
        note = find_note(id)
        if note is None:
            flash('Note not found', 'error')
            return redirect(url_for('home'))
        else:
            session.delete(note)
            session.commit()
            flash('Note deleted successfully!', 'success')


    return redirect(url_for('home'))
