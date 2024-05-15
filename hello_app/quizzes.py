from flask import (
    Blueprint,
    flash, 
    render_template, 
    request, 
    redirect,
    session, 
    url_for
    )

from hello_app.models import Quiz, Question, Choice
from .auth import login_required
from .utils import create_quiz_post, find_quiz, dbsession, app


quizzes = Blueprint("quizzes", __name__)
NOT_FOUND_MESSAGE = "Note not found"

@quizzes.route("/create/", methods=["GET", "POST"])
@login_required
def create_quiz():
    if request.method == "GET":
        return render_template("createquiz.html")
    elif request.method == "POST":
        # Pass the form data to the create_quiz_post function
        create_quiz_post(request.form)
        return redirect(url_for("home"))
    
@quizzes.route("/view/<id>")
@login_required
def view_quiz(id=None):
    try:
        # Find the quiz by ID
        quiz = find_quiz(id)
        if quiz is None:
            flash("Quiz not found", "error")
            return redirect(url_for("home"))
        # Retrieve the questions associated with the quiz
        questions = dbsession.query(Question).filter(Question.quizID == id).all()

        # For each question, retrieve its choices
        for question in questions:
            choices = dbsession.query(Choice).filter(Choice.questionID == question.questionID).all()
            # Assuming you want to associate choices with each question, you can add them to the question object
            question.choices = choices

        # Render the view with quiz details, questions, and choices
        return render_template("quiz.html", quiz=quiz, questions=questions)

    except Exception as e:
        flash(f"Failed to view quiz: {str(e)}", "error")
        app.logger.error("Failed to view quiz: %s from user: %s", e, session.get("user"))

        # Redirect to the home page or an error page
        return redirect(url_for("home"))
    
@quizzes.route("/edit/", methods=["GET", "POST"])
@login_required
def edit_quiz():
    print("Not made yet")
    return redirect(url_for("home"))

@quizzes.route("/delete/<id>")
@login_required
def delete_quiz(id=None):
    try:
        quiz = find_quiz(id)

        if quiz is None:
            flash(NOT_FOUND_MESSAGE, "error")
        else:
            if session["roleID"] == 2 or session["userID"] == quiz.accountID:
                # Delete all questions associated with the quiz
                questions = dbsession.query(Question).filter_by(quizID=quiz.quizID).all()
                for question in questions:
                    # Delete all choices associated with the question
                    dbsession.query(Choice).filter_by(questionID=question.questionID).delete()
                # Now delete the questions
                dbsession.query(Question).filter_by(quizID=quiz.quizID).delete()

                # Delete the quiz itself
                dbsession.delete(quiz)
                dbsession.commit()
                flash("Quiz and its components deleted successfully!", "success")
            else:
                flash("You are not authorized to delete this quiz", "error")

    except Exception as e:
        flash(f"Failed to delete quiz: {str(e)}", "error")
        app.logger.error(
            "Failed to delete quiz: %s from user: %s", e, session.get("user")
        )

    # Redirect to the page where the quiz was deleted from
    return redirect(request.referrer or url_for("home"))

@quizzes.route("/submit/<id>", methods=["POST"])
def submit_quiz(id=None):
    try:
        # Get the submitted form data
        form_data = request.form
        
        # Initialize score
        score = 0
        # Iterate through form data to calculate the score
        for key, choice_id in form_data.items():
            print(choice_id)
            print(key)
            if key.startswith("question"):
                # Get the corresponding choice object from the database
                choice = dbsession.query(Choice).filter(Choice.choiceID == choice_id).first()
                
                # Check if the choice exists and is correct
                if choice and choice.iscorrect:
                    score += 1

        # Optionally, you can store the score in the database or perform any other actions

        # Flash the score message
        flash(f"Your score: {score}", "success")

    except Exception as e:
        flash(f"Failed to submit quiz: {str(e)}", "error")
        app.logger.error("Failed to submit quiz: %s", e)

    # Redirect to the quiz page or any other relevant page
    return redirect(url_for("quizzes.view_quiz", id=id))