from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Account
from .utils import dbsession
from functools import wraps
from . import app


# importering af auth blueprint med prefix /auth
auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('You need to be logged in to view this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        account = dbsession.query(Account).filter_by(username=username).first()
        if account and check_password_hash(account.password, password):  
            session.clear()
            #gem bruger id og  role i session.
            session['user'] = account.username
            session['userID'] = account.accountID
            session['userEmail'] = account.email
            session['roleID'] = account.roleID

            flash(f'Login successful for {account.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            app.logger.warning(f"Failed login attempt from: {request.remote_addr} with username: {username}")
            return redirect(url_for('auth.login'))

    # If request method is GET, render the login template
    return render_template('login.html')

@auth.route('/logout')
def logout():
    user_logout = session['user']
    session.clear() 
    flash(f'You have been logged out, {user_logout}', 'success')
    return redirect(url_for('home'))


@auth.route('/signup', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        # Create account post logik
  
        if not request.form['username']:
            flash('Username is required', 'error')
            return redirect(url_for('create_account'))
        if not request.form['password']:
            flash('Password is required', 'error')
            return redirect(url_for('create_account'))
        if not request.form['email']:
            flash('Email is required', 'error')
            return redirect(url_for('create_account'))
        
        # Check if username already exists
        if dbsession.query(Account).filter_by(username=request.form['username']).first() is not None:
            flash('Username already exists', 'error')
            return redirect(url_for('auth.create_account'))
        
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            roleID = 1
            hashed_password = generate_password_hash(password, method='pbkdf2', salt_length=16)
            
            dbsession.add(Account(username = username, password = hashed_password, email = email, roleID = roleID))
            dbsession.commit()
            flash('Account created successfully!', 'success')
            # Logger automatisk brugeren ind efter oprettelse
            session.clear()
            account = dbsession.query(Account).filter_by(username=username).first()
            session['user'] = account.username
            session['userID'] = account.accountID
            session['userEmail'] = account.email
            return redirect(url_for('home'))
            
        except Exception as e:
            app.logger.error(f"Failed to create account: {e} from address: {request.remote_addr} with username: {username} and email: {email}")
            flash('Error creating account', 'error')
            return redirect(url_for('auth.create_account'))
        
        
    else:
        return render_template("signup.html")