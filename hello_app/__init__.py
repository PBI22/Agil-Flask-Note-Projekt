import os
from flask import Flask
from datetime import timedelta
from .dbconnect import init_database, Base

#app = Flask(__name__)    # Create an instance of the class for our use
#app.secret_key = 'secret_key' 
def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is not None:
        app.config.update(test_config)
    
    # Initialiser database sessionen efter konfigurationen er sat
    dbsession = init_database(app)

    with app.app_context():
        Base.metadata.create_all(bind=dbsession.bind)  # Opret database schema, hvis nødvendigt

    return app
app = create_app()
app.secret_key = os.environ.get('SECRET_KEY',"secret_key") # sætter "secret_key" som default hvis ikke der er en SECRET_KEY i environment variablerne

# session cookie settings 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 