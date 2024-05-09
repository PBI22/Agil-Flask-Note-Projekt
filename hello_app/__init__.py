"""Module initialization for a Flask application.

This module sets up a Flask app with configurations for security and session management. 
It includes setting a secret key from environment variables, enabling HTTP-only session cookies, 
setting the SameSite attribute for cookies, and defining a session lifetime. """

import os
from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)  # Create an instance of the class for our use

# Set secret_key before adding CSRF protection
app.secret_key = os.environ.get("SECRET_KEY", "secret_key")

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Session cookie settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
