"""
This module contains utility functions for the application. 

It includes functions for updating the list of notes from the database, 
and other helper functions used across the application.
"""

from datetime import datetime, timezone
from flask import flash, session
from .dbconnect import dbsession
from .models import Note, Account
from .auth import login_required
from . import app


def update_list():
    """
    Update the list of notes from the database.

    Returns:
        list: A list of Note objects representing the notes in the database.

    Raises:
        Exception: If there is an error while updating the list.

    """

    try:
        notes_db = []
        for row in dbsession.query(Note).order_by(Note.noteID):
            notes_db.append(row)
    except Exception as e:
        app.logger.critical("Failed to update list: %s", e)
    return notes_db


def create_note_post(form):
    """
    Create a new note and save it to the database using the provided form data.

    Parameters:
    - form (Form): A FlaskForm object containing validated form data.

    Returns:
    None

    Raises:
    - Exception: If there is an error creating the note.
    """
    try:
        # Extract data from form directly instead of request.form
        title = form.title.data
        note_text = form.text.data
        imagelink = form.imagelink.data or None  # Uses None if imagelink is empty
        created = datetime.now(timezone.utc)
        lastedited = datetime.now(timezone.utc)
        account_id = session["userID"]  # Make sure session is imported and available

        # Create a new note instance
        new_note = Note(
            title=title,
            text=note_text,
            created=created,
            lastedited=lastedited,
            imagelink=imagelink,
            author=account_id,
        )
        dbsession.add(new_note)
        dbsession.commit()
        flash("Note created successfully", "success")
    except Exception as e:
        dbsession.rollback()
        flash(f"Failed to create note: {str(e)}", "error")
        app.logger.error(
            "Failed to create note: %s from user: %s", e, session.get("user", "Unknown")
        )


@login_required
def edit_note_post(form, note_id):
    """
    Edit a note and update it in the database.

    Parameters:
        form (FlaskForm): The form object containing the validated data.
        note_id (int): The ID of the note to be edited.

    Returns:
        None

    Notes:
        - If the user is logged in and authorized to edit the note,
          the note will be updated in the database with the new title, text, last edited timestamp, and optional image link.
        - If the user is not authorized to edit the note, an error message will be flashed.
    """
    try:
        note = dbsession.query(Note).filter_by(noteID=note_id).first()
        if note is None:
            flash("Note not found.", "error")
            return

        user_id = session["userID"]
        user_role = session["roleID"]
        if user_id == note.author or user_role == 2:  # 2 is the admin role
            note.title = form.title.data
            note.text = form.text.data
            note.lastedited = datetime.now(timezone.utc)
            note.imagelink = form.imagelink.data
            dbsession.commit()
            flash("Note updated successfully", "success")
        else:
            flash("You are not authorized to edit this note", "error")
    except Exception as e:
        dbsession.rollback()
        flash(f"Failed to edit note: {str(e)}", "error")
        app.logger.error(
            "Failed to edit note: %s from user: %s", e, session.get("user", "Unknown")
        )


def find_note(note_id):
    """
    Find a note by its ID.

    Args:
        note_id (int): The ID of the note to find.

    Returns:
        Note or None: The Note object with the specified ID, or None if no note is found.

    Raises:
        Exception: If there is an error while finding the note.

    """
    try:
        note = next(
            (note for note in update_list() if note.noteID == int(note_id)), None
        )
    except Exception as e:
        app.logger.error("Failed to find note: %s from user: %s", e, session["user"])
    return note

def searchbar(query):
    """
    Searches for notes and accounts based on a given query.

    Parameters:
    - query (str): The search query.

    Returns:
    - list: A list of search results, which includes notes and accounts.

    Raises:
    - Exception: If there is an error during the search process.

    Example:
    search_results = searchbar("python")
    """
    try:
        search_results = (
            dbsession.query(Note)
            .filter(
                Note.title.contains(query)
                | Note.text.contains(query)
                | Account.username.contains(query)
            )
            .all()
        )
    except Exception as e:
        app.logger.error(
            "Failed to search for: %s  from user: %s  with error: %s",
            query,
            session["user"],
            e,
        )
    return search_results
