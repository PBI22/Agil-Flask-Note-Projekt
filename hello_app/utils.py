"""
This module contains utility functions for the application. 

It includes functions for updating the list of notes from the database, 
and other helper functions used across the application.
"""

from datetime import datetime, timezone
from flask import flash, session
from .dbconnect import dbsession
from .models.Note import Note, Account
from .models.Quiz import Quiz, Question, Choice
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
def update_quiz_list():
    """
    Update the list of quizzes from the database.

    Returns:
        list: A list of Quiz objects representing the quizzes in the database.

    Raises:
        Exception: If there is an error while updating the list.

    """
    try:
        quizzes_db = []
        for row in dbsession.query(Quiz).order_by(Quiz.quizID):
            quizzes_db.append(row)
    except Exception as e:
        app.logger.critical("Failed to update quiz list: %s", e)
    return quizzes_db


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

def find_quiz(quiz_id):
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
        quiz = next(
            (quiz for quiz in update_quiz_list() if quiz.quizID == int(quiz_id)), None
        )
    except Exception as e:
        app.logger.error("Failed to find note: %s from user: %s", e, session["user"])
    return quiz

def create_quiz_post(form):
    """
    Create a new quiz and save it to the database.

    Parameters:
        form (dict): A dictionary containing the form data submitted by the user.

    Returns:
        None

    Raises:
        Exception: If there is an error creating the quiz.

    Description:
        This function takes in the form data submitted by the user and creates a new quiz in the database.
        It extracts the quiz name from the form and creates a new Quiz instance with the name,
        current timestamp, and the user's account ID. 
        The new quiz is then added to the database session and flushed to generate a unique quiz ID.

        Next, the function parses the questions and choices from the form. 
        It iterates over the question keys in the form and extracts the question text. 
        For each question, a new Question instance is created with the text and the quiz ID. 
        The new question is added to the database session and flushed to generate a unique question ID.

        Then, the function iterates over the choice keys in the form and 
        extracts the choice text and checkbox value. 
        It constructs the corresponding checkbox key and checks if the checkbox is checked. 
        If the choice key starts with the current question key, 
        a new Choice instance is created with the text, checkbox value, and the question ID. 
        The new choice is added to the database session.

        Finally, the function commits the changes to the database, flashes a success message, 
        and logs the successful creation of the quiz. If there is an error during the process, 
        the function rolls back the database session, flashes an error message with error details, 
        and logs the failed creation of the quiz.
    """
    try:
        # Extract quiz name
        quiz_name = form['quiz-name']

        # Structure insert query quiz
        new_quiz = Quiz(
            name=quiz_name,
            created=datetime.now(timezone.utc),
            lastedited=datetime.now(timezone.utc),
            accountID=session["userID"],
        )

        # Add the new quiz to the database session
        dbsession.add(new_quiz)
        dbsession.flush()

        # Parse questions and choices from the form
        question_keys = [key for key in form.keys() if key.startswith("question")]
        for question_key in question_keys:
            # Extract question text from the form
            question_text = form[question_key]

            # Create a new question instance associated with the quiz
            new_question = Question(text=question_text, quizID=new_quiz.quizID)

            # Add the new question to the database session
            dbsession.add(new_question)
            dbsession.flush()

            # Parse choices for the current question
            choice_keys = [
                key
                for key in form.keys()
                if key.startswith("choice") and not key.endswith("-correct")
            ]
            for choice_key in choice_keys:
                # Extract choice text from the form
                choice_text = form[choice_key]

                # Construct the corresponding checkbox key
                checkbox_key = f"{choice_key}-correct"

                # Extract the checkbox value
                is_correct = form.get(checkbox_key, False) == 'on'

                choice_input = 'choice-' + question_key
                if choice_key.startswith(choice_input):

                    # Create a new choice instance associated with the current question
                    new_choice = Choice(text=choice_text, iscorrect=is_correct, questionID=new_question.questionID)

                    # Add the new choice to the database session
                    dbsession.add(new_choice)

        # Commit changes to the database
        dbsession.commit()

        flash("Quiz created successfully", "success")
    except Exception as e:
        dbsession.rollback()
        flash(f"Failed to create quiz: {str(e)}", "error")
        app.logger.error("Failed to create quiz: %s from user: %s", e, session.get("user", "Unknown"))


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
