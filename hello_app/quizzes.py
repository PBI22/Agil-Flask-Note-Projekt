from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    redirect,
    session,
    url_for
    )

from hello_app.models import Question, Choice
from .auth import login_required
from .utils import create_quiz_post, find_quiz, dbsession, app


quizzes = Blueprint("quizzes", __name__)
NOT_FOUND_MESSAGE = "Note not found"

@quizzes.route("/create/", methods=["GET", "POST"])
@login_required
def create_quiz():
    """
    Create a new quiz.

    This function is a view function that handles the creation of a new quiz. 
    It is associated with the "/create/" route and can be accessed via GET and POST methods.

    Parameters:
        None

    Returns:
        None

    Notes:
        - If the request method is GET, the function renders the "createquiz.html" template.
        - If the request method is POST, 
          the function calls the create_quiz_post function 
          with the form data and redirects the user to the home page.

    Example:
        @quizzes.route("/create/", methods=["GET", "POST"])
        @login_required
        def create_quiz():
            if request.method == "GET":
                return render_template("createquiz.html")
            elif request.method == "POST":
                create_quiz_post(request.form)
                return redirect(url_for("home"))
    """
    if request.method == "GET":
        return render_template("createquiz.html")
    if request.method == "POST":
        # Pass the form data to the create_quiz_post function
        create_quiz_post(request.form)
        return redirect(url_for("home"))

@quizzes.route("/view/<id>")
@login_required
def view_quiz(id=None):
    """
    View a quiz by its ID.

    Args:
        id (str): The ID of the quiz to view.

    Returns:
        flask.Response: The rendered template for the quiz view.

    Raises:
        Exception: If there is an error while viewing the quiz.

    Notes:
        This function is a route handler for the "/view/<id>" URL endpoint.
        It requires the user to be logged in, as indicated by the @login_required decorator.
        The function first attempts to find the quiz by its ID using the find_quiz function.
        If the quiz is not found, an error message is flashed and the user is redirected to the home page.
        If the quiz is found, the function retrieves the associated questions and their choices from the database.
        The questions and choices are then passed to the quiz.html template for rendering.
        If there is an error during the process, an error message is flashed and the user is redirected to the home page.

    Example:
        To view a quiz with ID 1, the URL would be "/view/1".
    """
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
    """
    Edit a quiz.

    This function is a view function that allows the user to edit a quiz. 
    It is decorated with the `@login_required` decorator, 
    which ensures that the user is logged in before accessing this view.

    Parameters:
        None

    Returns:
        redirect: If the user is not logged in, it flashes an error message and redirects the user to the login page. 
        Otherwise, it redirects the user to the home page.

    Notes:
        This function is associated with the "/edit/" route and accepts both GET and POST requests. 
        When accessed via GET request, 
        it simply prints a message indicating that the functionality is not implemented yet. 
        When accessed via POST request, it redirects the user to the home page.

    Example:
        @quizzes.route("/edit/", methods=["GET", "POST"])
        @login_required
        def edit_quiz():
            print("Not made yet")
            return redirect(url_for("home"))
    """
    print("Not made yet")
    return redirect(url_for("home"))

@quizzes.route("/delete/<id>")
@login_required
def delete_quiz(id=None):
    """
    Delete a quiz.

    This function deletes a quiz and all its associated questions and choices from the database.

    Parameters:
        id (int): The ID of the quiz to be deleted.

    Returns:
        redirect: Redirects to the page where the quiz was deleted from.

    Raises:
        Exception: If there is an error while deleting the quiz.

    Notes:
        - This function requires the user to be logged in.
        - If the user is not authorized to delete the quiz, an error message is flashed.
        - If the quiz is not found, an error message is flashed.
        - If the quiz and its components are deleted successfully, a success message is flashed.

    Example:
        @quizzes.route("/delete/<id>")
        @login_required
        def delete_quiz(id=None):
            # Code for deleting the quiz
            pass
    """
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
    return redirect(url_for("home"))

@quizzes.route("/submit/<id>", methods=["POST"])
def submit_quiz(id=None):
    """
    Submit a quiz and calculate the score.

    Parameters:
    - id (str): The ID of the quiz to submit.

    Returns:
    - redirect: Redirects to the quiz page or any other relevant page.

    Raises:
    - Exception: If there is an error while submitting the quiz.

    Description:
    - This function is a route handler for the "/submit/<id>" endpoint.
    - It is triggered when a POST request is made to submit a quiz.
    - It retrieves the submitted form data and initializes the score and total variables.
    - It iterates through the form data to calculate the score.
    - For each question in the form data, it retrieves the corresponding choice object from the database.
    - If the choice exists and is correct, it increments the score.
    - After calculating the score, it flashes a success message with the score and total.
    - If there is an error while submitting the quiz, it flashes an error message and logs the error.
    - Finally, it redirects to the quiz page or any other relevant page.

    Example:
    - submit_quiz("quiz1")
    """
    try:
        # Get the submitted form data
        form_data = request.form
        # Initialize score and total
        score = 0
        total = 0
        # Iterate through form data to calculate the score
        for key, choice_id in form_data.items():
            if key.startswith("question"):
                total += 1
                # Get the corresponding choice object from the database
                choice = dbsession.query(Choice).filter(Choice.choiceID == choice_id).first()
                # Check if the choice exists and is correct
                if choice and choice.iscorrect:
                    score += 1

        flash(f"Din score: {score}/{total}", "success")

    except Exception as e:
        flash(f"Failed to submit quiz: {str(e)}", "error")
        app.logger.error("Failed to submit quiz: %s", e)

    # Redirect to the quiz page or any other relevant page
    return redirect(url_for("quizzes.view_quiz", id=id))
