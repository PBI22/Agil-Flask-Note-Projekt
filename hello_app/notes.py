"""
This module defines the 'notes' blueprint and provides routes for 
creating, editing, viewing, deleting, and searching notes.

The blueprint handles various endpoints that allow users to interact with note data. 
It includes functionality to:
- Create a new note via a form.
- Edit an existing note if the user has the appropriate permissions.
- View a note in Markdown format.
- Delete a note if the user is either an admin or the author of the note.
- Search for notes based on a text query.

Each route is protected with authentication where necessary, ensuring that only logged-in 
users can modify or delete notes. The module integrates with the application's database
session to perform CRUD operations on the notes.

Routes:
- /create/ : GET and POST methods to display a form and create a note.
- /edit/<id> : GET and POST methods to display a form for editing and update a note.
- /view/<id> : GET method to display a note.
- /delete/<id> : GET method to delete a note.
- /search : GET method to search for notes based on a query.

The module uses Flask's rendering capabilities to return HTML pages that include forms 
and note content, and leverages Flask's messaging and redirection features to enhance 
user interaction and feedback.
"""
from datetime import datetime, timezone
import markdown2
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import NoteForm, EditNoteForm
from .auth import login_required
from .utils import (
    create_note_post,
    edit_note_post,
    find_note,
    searchbar,
    dbsession,
    app,
    session,
)

# Note blueprint med (url_prefix='/notes')

notes = Blueprint("notes", __name__)
NOT_FOUND_MESSAGE = "Note not found"


@notes.route("/create/", methods=["GET", "POST"])  # NOSONAR
@login_required
def create_note():
    """
    Create a new note.

    This function is used to create a new note.
    If the request method is GET, it renders the 'createnote.html' template.
    If the request method is POST, it calls the 'create_note_post' function
    passing the request object as an argument, and then redirects to the 'home' page.

    Returns:
        None

    """
    form = NoteForm()
    if form.validate_on_submit():
        create_note_post(form)
        return redirect(url_for("home"))

    return render_template("createnote.html", form=form)


@notes.route("/edit/<int:id>", methods=["GET", "POST"])  # NOSONAR
@login_required
def edit(id):
    """
    Edit a note.

    Parameters:
    - id (int): The ID of the note to be edited.

    Returns:
    - None
    """
    note = find_note(id)
    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("home"))

    form = EditNoteForm(obj=note)  # Pre-populate form with note data
    if form.validate_on_submit():
        edit_note_post(form, id)  # Pass the form and note ID
        return redirect(url_for("home"))

    return render_template("editnote.html", form=form, note_id=id)


@notes.route("/view/<id>")
def view(id=None):
    """
    View a specific note.

    Parameters:
    - id (str): The ID of the note to view.

    Returns:
    - If the note is found, renders the 'mdnote.html' template with the note and its markdown content.
    - If the note is not found, flashes an error message and redirects to the home page.
    - If an exception occurs, logs the error and redirects to the home page.

    """
    note = find_note(id)
    try:
        if note:
            note_markdown = markdown2.markdown(
                note.text,
                extras=[
                    "tables",
                    "fenced-code-blocks",
                    "code-friendly",
                    "mermaid",
                    "task_list",
                    "admonitions",
                ],
            )
            return render_template(
                "mdnote.html", note=note, note_markdown=note_markdown
            )

        flash(NOT_FOUND_MESSAGE, "error")
        return redirect(url_for("home"))
    except Exception as e:
        app.logger.error(
            "Failed to view note: %s from user: %s", e, session.get("user")
        )
        return redirect(url_for("home"))


@notes.route("/delete/<id>")
@login_required
def delete_note(id=None):
    """
    Delete a note.

    This function is used to delete a note from the database.
    It requires the user to be logged in and have the necessary authorization to delete the note.

    Parameters:
    - id (int): The ID of the note to be deleted.

    Returns:
    - redirect: Redirects the user to the home page after deleting the note.

    Raises:
    - Exception: If there is an error while deleting the note.

    """
    try:
        note = find_note(id)
        if note is None:
            flash(NOT_FOUND_MESSAGE, "error")
        else:
            if session["roleID"] == 2 or session["userID"] == note.author:
                dbsession.delete(note)
                dbsession.commit()
                flash("Note deleted successfully!", "success")
            else:
                flash("You are not authorized to delete this note", "error")

    except Exception as e:
        flash(f"Failed to delete note: {str(e)}", "error")
        app.logger.error(
            "Failed to delete note: %s from user: %s", e, session.get("user")
        )

    return redirect(url_for("home"))


@notes.route("/search")
def search_results():
    """
    Searches for results based on a given query.

    Parameters:
    - query (str): The search query.

    Returns:
    - redirect: If the query is empty, redirects to the home page.
    - render_template: Renders the search_results.html template with the search results and query.

    """
    query = request.args.get("query")
    if not query:
        return redirect(url_for("home"))
    results = searchbar(query)
    return render_template("search_results.html", results=results, query=query)
