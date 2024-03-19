import os
from flask import Flask
from datetime import timedelta

<<<<<<< HEAD
app = Flask(__name__)    # Create an instance of the class for our use
app.secret_key = 'secret_key' 
=======
#app = Flask(__name__)    # Create an instance of the class for our use
#app.secret_key = 'secret_key' 
app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.get.environ('SECRET_KEY')
>>>>>>> b4f2c461131d9ea4c6917e1921e3e676690c1d00

# session cookie settings 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)