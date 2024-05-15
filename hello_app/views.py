import os
from datetime import datetime
from flask import render_template, send_from_directory, request
from flask_swagger_ui import get_swaggerui_blueprint
from . import app, csrf
from .utils import update_list, update_quiz_list
from .auth import auth
from .api import api
from .log_config import setup_app_logging
from .notes import notes
from .oauth import oauth, oauth_bp
from .quizzes import quizzes

# inits til vores app
oauth.init_app(app)
app.register_blueprint(oauth_bp, url_prefix='/oauth')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')
csrf.exempt(api) # csrf is disabled for api, cause we are using jwt for validation
app.register_blueprint(notes, url_prefix='/notes')
app.register_blueprint(quizzes, url_prefix='/quizzes')
csrf.exempt(quizzes) # Disabled for testing environment
setup_app_logging(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Note API"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    """
    Render the home page.

    This function is responsible for rendering the home page of the application. 
    It logs the IP address of the requester and passes the list of notes and the 
    current datetime to the home.html template for rendering.

    Returns:
        str: The rendered HTML content of the home page.

    """
    app.logger.info("Home page requested from: %s", request.remote_addr)
    return render_template("home.html", notes = update_list(), quiz = update_quiz_list(), datetime = datetime.now())

@app.route('/robots.txt')
def robots_txt():
    """
    Serve the 'robots.txt' file.

    This function is a route handler for the '/robots.txt' endpoint. 
    It serves the 'robots.txt' file located in the 'static' folder of the Flask application.

    Returns:
        Response: The response object containing the 'robots.txt' file.

    Raises:
        Exception: If there is an error while serving the 'robots.txt' file.

    """
    try:
        app.logger.info("robots.txt requested from: %s", request.remote_addr)
        return send_from_directory(app.static_folder, 'robots.txt')
    except Exception as e:
        app.logger.error(f"Failed to serve robots.txt: {e}")
        raise
