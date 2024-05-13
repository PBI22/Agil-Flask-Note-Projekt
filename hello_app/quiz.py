from flask import Blueprint, render_template, request, redirect, url_for
from .auth import login_required
from .utils import create_quiz_post

quiz = Blueprint("quiz", __name__)
NOT_FOUND_MESSAGE = "Note not found"

@quiz.route("/create/", methods=["GET", "POST"])
@login_required
def create_quiz():

    if request.method == "GET":
        return render_template("createquiz.html")

    create_quiz_post()
    return redirect(url_for("home"))
