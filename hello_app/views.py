from datetime import datetime
from flask import render_template
from . import app
from .utils import *
from .log_config import setup_app_logging
from .notes import notes
from .auth import auth

#Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(notes, url_prefix='/notes')

#Setup af logging til appen
setup_app_logging(app)

@app.route("/")
def home():
    app.logger.info("Home page requested")
    return render_template("home.html", notes = updateList(), datetime = datetime.now())
