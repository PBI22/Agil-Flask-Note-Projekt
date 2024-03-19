import os
from datetime import datetime
from flask import render_template, send_from_directory, request
from . import app
from .utils import *
from .auth import auth, login_required
from .API import api
from .log_config import setup_app_logging
from .notes import notes

#Blueprints
app.register_blueprint(auth, url_prefix='/auth')

app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(notes, url_prefix='/notes')

#Setup af logging til appen
setup_app_logging(app)

@app.route("/")
def home():
    app.logger.info("Home page requested from: %s", request.remote_addr)
    return render_template("home.html", notes = updateList(), datetime = datetime.now())

@app.route('/robots.txt')
def robots_txt():
    try:
        root_dir = os.path.abspath(os.path.dirname(__file__))
        folder_path = os.path.join(root_dir, 'static')
        app.logger.info("robots.txt requested from: %s", request.remote_addr)
        return send_from_directory(app.static_folder, 'robots.txt')
    except Exception as e:
        app.logger.error(f"Failed to serve robots.txt: {e}")
        raise