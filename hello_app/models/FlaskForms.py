# pylint: disable=C0103
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """
    Form for handling user login with username and password fields.

    Attributes:
        username (StringField): Field for entering the username.
        password (PasswordField): Field for entering the password.
        submit (SubmitField): Button for submitting the login form.
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    """
    Form for handling user sign up with username, email, password, and confirm password fields.

    Attributes:
        username (StringField): Field for entering the username.
        email (EmailField): Field for entering the email.
        password (PasswordField): Field for entering the password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Button for submitting the sign up form.
    """

    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class NoteForm(FlaskForm):
    """
    Form for creating a new note with title, text, and optional image link fields.

    Attributes:
        title (StringField): Field for entering the title of the note.
        text (TextAreaField): Field for entering the text content of the note.
        imagelink (HiddenField): Field for storing the optional image link of the note.
        submit (SubmitField): Button for submitting the note form.
    """

    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Note", validators=[DataRequired()])
    imagelink = HiddenField()  # Handling this as hidden for now; modify as needed
    submit = SubmitField("Create Note")


class EditNoteForm(FlaskForm):
    """
    Form for editing an existing note with title, text, and optional image link fields.

    Attributes:
        title (StringField): Field for entering the updated title of the note.
        text (TextAreaField): Field for entering the updated text content of the note.
        imagelink (HiddenField): Field for storing the updated optional image link of the note.
        submit (SubmitField): Button for submitting the edited note form.
    """

    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Note", validators=[DataRequired()])
    imagelink = HiddenField()
    submit = SubmitField("Edit Note")
