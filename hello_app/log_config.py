"""
This module configures logging for a Flask application. 
It sets up a file-based log handler that rotates every day.
It is keeping logs for the last 30 days. 
Logging is only enabled when is not in debug mode to avoid logging during development. 
The logs include timestamps, log levels, logger names, and messages.

Functions:
    setup_app_logging(app): Configures logging for the provided Flask application object.
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_app_logging(app):
    """
    Set up logging for the Flask application.

    Args:
        app: The Flask application object.

    Returns:
        None
    """

    if not app.debug:  # Bruger ikke log i debug tilstand

        # Sørg for at log-mappe eksisterer
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Sti til logfil
        log_file_path = os.path.join(logs_dir, "app.log")

        # Opretter en daglig rotation
        file_handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=30
        )
        file_handler.setLevel(logging.INFO)  # Angiv logningsniveauet for filhåndtereren

        # Definer formatet for logbeskeder
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s: %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Tilføj file_handler til Flask-appens logger
        app.logger.addHandler(file_handler)

        # Da Flask-appens logger som standard er indstillet til WARNING
        # sættes den til INFO for at fange flere begivenheder
        app.logger.setLevel(logging.INFO)
