from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# Kan bruges til senere at arbejde med password hashing og check af dette
#from werkzeug.security import generate_password_hash, check_password_hash
from .models import Account
from .utils import dbsession
from functools import wraps

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

        # Query the database for the account with provided username and password
        account = dbsession.query(Account).filter_by(username=username, password=password).first()
        if account:   

            session['user'] = account.username

            flash(f'Login successful for {account.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # If request method is GET, render the login template
    return render_template('login.html')

@auth.route('/logout')
def logout():
    user_logout = session['user']
    session.pop('user', None) 
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
            return redirect(url_for('create_account'))
        
        try:
            dbsession.add(Account(username = request.form['username'], password = request.form['password'], email = request.form['email']))
            dbsession.commit()
            flash('Account created successfully!', 'success')
            
        except:
            flash('Error creating account', 'error')
            return redirect(url_for('create_account'))
        return redirect(url_for('home'))
        
    else:
        return render_template("signup.html")