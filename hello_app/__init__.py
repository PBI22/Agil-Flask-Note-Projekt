import os
from flask import Flask
from datetime import timedelta

#app = Flask(__name__)    # Create an instance of the class for our use
#app.secret_key = 'secret_key' 
app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.environ.get('SECRET_KEY',"secret_key") # sætter "secret_key" som default hvis ikke der er en SECRET_KEY i environment variablerne

# session cookie settings 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 