import markdown2
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from . import app
from .models import Note, Account
from .utils import *
from .auth import auth, login_required
from .API import api
from .log_config import setup_app_logging

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')

#Setup af logging til appen
setup_app_logging(app)

# Vores landing Page - Der viser listen over noter
@app.route("/")
def home():
    app.logger.info("Home page requested")
    return render_template("home.html", notes = updateList(), datetime = datetime.now())

# Create note
@app.route("/create/", methods=["GET","POST"])
@login_required
def create_note():

    if request.method == "GET":
        #app.logger.info("Create note page requested from %s", session.get('username'))
        return render_template("createnote.html")

    # Hvis ikke GET, så er det POST, og så kører vi denne logik
    else:
        create_note_post(request)

    return redirect(url_for('home'))

@app.route("/edit/<id>", methods=["GET","POST"])
@login_required
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

    #Tjekker hvis det er et markdown note (som markeres med !MD i starten af teksten)
    if note.text.startswith("!MD"):
        note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
        return render_template("mdnote.html", note=note, note_markdown=note_markdown)
    else:
        return render_template("mdnote.html", note=note, note_markdown=note.text)


@app.route("/delete/<id>")
@login_required
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
            
            dbsession.delete(note)
            dbsession.commit()
            flash('Note deleted successfully!', 'success')


    return redirect(url_for('home'))

@app.route("/search")
def search_results():
    query = request.args.get('query')

    if not query or query == "":
        return redirect(url_for('home'))

    # Søg efter noter, der matcher søgeordet
    search_results = searchbar(query)
    return render_template('search_results.html', results=search_results, query=query)

@app.route('/robots.txt')
def robots_txt():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    folder_path = os.path.join(root_dir, 'static')
    return send_from_directory(app.static_folder, 'robots.txt')
