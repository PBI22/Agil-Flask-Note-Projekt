from flask import Blueprint, render_template, request, redirect, url_for, flash
from .auth import login_required
import markdown2
from .utils import *

#Note blueprint med (url_prefix='/notes')

notes = Blueprint('notes', __name__)

@notes.route("/create/", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "GET":
        return render_template("createnote.html")
    else:

        create_note_post(request)
        return redirect(url_for('home')) 

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
    try:
        if note and note.text.startswith("!MD"):
            note_markdown = markdown2.markdown(note.text.replace("!MD", ""), extras=["tables","fenced-code-blocks","code-friendly","mermaid","task_list","admonitions"])
            return render_template("mdnote.html", note=note, note_markdown=note_markdown)
        elif note:
            return render_template("mdnote.html", note=note, note_markdown=note.text)
        else:
            flash("Note not found", "error")
            app.logger.error(f"Failed to view note: {e} from user: {session['user']}")
            return redirect(url_for('home')) 
    except Exception as e:
        app.logger.error(f"Failed to view note: {e} from user: {session['user']}")
        return redirect(url_for('home'))
        
@notes.route("/delete/<id>")
@login_required
def delete_note(id=None):
    try:
        note = find_note(id)
        if note is None:
            flash('Note not found', 'error')
        else:
            user = session['userID']
            if session['role'] == 'Admin' or user == note.author:
                dbsession.delete(note)
                dbsession.commit()
                flash('Note deleted successfully!', 'success')
            else:
                flash('You are not authorized to delete this note', 'error')

    except Exception as e:
        flash(f'Failed to delete note: {str(e)}', 'error')
        app.logger.error(f"Failed to delete note: {e} from user: {session.get('user')}")

    return redirect(url_for('home'))  

@notes.route("/search")
def search_results():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('home')) 
    results = searchbar(query) 
    return render_template('search_results.html', results=results, query=query)