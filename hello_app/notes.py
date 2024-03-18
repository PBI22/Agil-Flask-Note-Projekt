from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from .auth import login_required
import markdown2
from .utils import *


notes = Blueprint('notes', __name__)

@notes.route("/create/", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "GET":
        return render_template("createnote.html")
    else:

        create_note_post(request)
        return redirect(url_for('home'))  # Ændret fra 'home' til 'notes.home'

@notes.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id=None):
    note = find_note(id)
    if note is None:
        flash('Note not found', 'error')
        return redirect(url_for('home'))  
    if request.method == "GET":
        return render_template("editnote.html", note=note)
    else:
        
        edit_note_post(request, id)
        return redirect(url_for('home'))  

@notes.route("/view/<id>")
def view(id=None):
    note = find_note(id)
    if note and note.text.startswith("!MD"):
        note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
        return render_template("mdnote.html", note=note, note_markdown=note_markdown)
    elif note:
        return render_template("mdnote.html", note=note, note_markdown=note.text)
    else:
        flash("Note not found", "error")
        return redirect(url_for('home')) 
    
@notes.route("/delete/<id>")
@login_required
def delete_note(id=None):
    note = find_note(id)
    if note is None:
        flash('Note not found', 'error')
    else:
        dbsession.delete(note)
        dbsession.commit()
        flash('Note deleted successfully!', 'success')
    return redirect(url_for('home'))  

@notes.route("/search")
def search_results():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('home')) 
    results = searchbar(query)  # Antager denne funktion returnerer søgeresultater
    return render_template('search_results.html', results=results, query=query)