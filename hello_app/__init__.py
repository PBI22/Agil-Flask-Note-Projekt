import os
from flask import Flask
from datetime import timedelta

app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.environ.get('SECRET_KEY', "secret key")

# session cookie settings 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 