from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """
    Form for handling user login with username and password fields.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class NoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Note", validators=[DataRequired()])
    imagelink = HiddenField()  # Handling this as hidden for now; modify as needed
    submit = SubmitField("Create Note")


class EditNoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Note", validators=[DataRequired()])
    imagelink = HiddenField()
    submit = SubmitField("Edit Note")
