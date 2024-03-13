from flask import Flask  # Import the Flask class
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore
from models import User, Role



app = Flask(__name__)    # Create an instance of the class for our use
app.secret_key = 'secret_key' 

#'alchemy instance'
db = SQLAlchemy()
db.init_app(app)

#load users and roles for session
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
Security = Security(app, user_datastore)
app.app_context().push()