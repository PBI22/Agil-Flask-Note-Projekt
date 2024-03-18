import os
import logging
from logging.handlers import TimedRotatingFileHandler


"""
Logging niveauer:
    DEBUG: Detailed information, typically of interest only when diagnosing problems.
    INFO: Confirmation that things are working as expected.
    WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
    ERROR: Due to a more serious problem, the software has not been able to perform some function.
    CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
    
    f.eks:
    app.logger.debug("This is a debug message")
    app.logger.info("This is an info message")
    app.logger.warning("This is a warning message")
    app.logger.error("This is an error message")
    app.logger.critical("This is a critical message")
"""

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
        log_file_path = os.path.join(logs_dir, 'app.log')

        # Opretter en daglig rotation
        file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=30)
        file_handler.setLevel(logging.INFO)  # Angiv logningsniveauet for filhåndtereren
        
        # Definer formatet for logbeskeder
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s')
        file_handler.setFormatter(formatter)

        # Tilføj file_handler til Flask-appens logger
        app.logger.addHandler(file_handler)

        # Da Flask-appens logger som standard er indstillet til WARNING, sættes den til INFO for at fange flere begivenheder
        app.logger.setLevel(logging.INFO)
