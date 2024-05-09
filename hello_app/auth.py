from functools import wraps
from flask import (
    Blueprint,
    render_template,
    request, redirect,
    url_for,
    flash,
    session
    )
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Account, LoginForm, SignUpForm
from .utils import dbsession
from . import app


# importering af auth blueprint med prefix /auth
auth = Blueprint('auth', __name__)

def login_required(f):
    """
    Decorator function that checks if a user is logged in before allowing access to a view function.

    Parameters:
        f (function): The view function to be decorated.

    Returns:
        function: The decorated view function.

    Notes:
        This decorator function checks if the 'user' key is present in the session.
        If not, it flashes an error message and redirects the user to the login page.
        If the 'user' key is present, it calls the original view function.

    Example:
        @login_required
        def my_view_function():
            # Code for the view function
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('You need to be logged in to view this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login functionality for the application.

    Returns:
    - Redirects the user to the home page if the login is successful.
    - Redirects the user back to the login page if the login fails.
    - Renders the login template on GET request.
    """

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        account = dbsession.query(Account).filter_by(username=username).first()
        if account and check_password_hash(account.password, password):
            session.clear()
            # gem bruger id og  role i session.
            session['user'] = account.username
            session['userID'] = account.accountID
            session['userEmail'] = account.email
            session['roleID'] = account.roleID

            flash(f'Login successful for {account.username}', 'success')
            return redirect(url_for('home'))
        else:
            print("3")
            flash('Invalid username or password', 'error')
            app.logger.warning("Failed login attempt from: %s with username: %s", request.remote_addr, form.username.data)
            return render_template("login.html", form=form)

    # If request method is GET or form is not valid, render the login template
    return render_template("login.html", form=form)

@auth.route('/logout')
def logout():
    """
    Logout the current user.

    This function clears the session and redirects the user to the home page.
    It also displays a flash message to notify the user that they have been logged out.

    Returns:
        redirect: A redirect response to the home page.

    """
    user_logout = session['user']
    session.clear()
    flash(f'You have been logged out, {user_logout}', 'success')
    return redirect(url_for('home'))


@auth.route('/signup', methods=['GET', 'POST'])
def create_account():
    """
    Create a new user account.

    This function handles the creation of a new user account.
    It is accessed through the '/signup' route and supports both GET and POST methods.

    Parameters:
        None

    Returns:
        If the request method is GET, it renders the 'signup.html' template.
        If the request method is POST:
            - If the required fields (username, password, email) are not provided,
              it redirects to the 'create_account' route and displays appropriate flash messages.
            - If the username already exists,
              it redirects to the 'auth.create_account' route and displays a flash message.
            - If the account creation is successful,
              it redirects to the 'home' route and displays a success flash message.
            - If an exception occurs during the account creation process,
              it redirects to the 'auth.create_account' route and displays an error flash message.

    Raises:
        None
    """
    form = SignUpForm()
    if form.validate_on_submit(): # already checks for POST in this validate, so no need to check for POST again
        # Create account post logik
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if not username:
            flash('Username is required', 'error')
            return redirect(url_for('create_account'))
        if not email:
            flash('Password is required', 'error')
            return redirect(url_for('create_account'))
        if not password:
            flash('Email is required', 'error')
            return redirect(url_for('create_account'))

        existing_user = dbsession.query(Account).filter_by(username=username).first()
        existing_email = dbsession.query(Account).filter_by(email=email).first()
        # Check if username or email already exists
        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for("auth.create_account"))
        if existing_email:
            flash("Email already registered", "error")
            return redirect(url_for("auth.create_account"))

        try:
            hashed_password = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=16
            )
            new_account = Account(
                username=username,
                password=hashed_password,
                email=email,
                roleID=1,  # default role ID
            )
            dbsession.add(new_account)
            dbsession.commit()

            # Log the user in automatically
            session["user"] = username
            session["userID"] = new_account.accountID
            session["userEmail"] = email
            flash("Account created successfully!", "success")
            return redirect(url_for("home"))

        except Exception as e:
            app.logger.error("Failed to create account: %s from address: %s with username: %s and email: %s", e, request.remote_addr, username, email)
            flash('Error creating account', 'error')
            return redirect(url_for('auth.create_account'))

    
    return render_template("signup.html", form=form)
