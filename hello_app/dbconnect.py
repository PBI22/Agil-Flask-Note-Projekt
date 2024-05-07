import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from . import app
from .models import Base
TESTING = os.environ.get("TESTING", False)
# Construct an absolute path to where the database file should be located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "db.sqlite")

def get_engine(testing = False):
    """
    Returns a SQLAlchemy engine object based on the specified configuration.

    Parameters:
        testing (bool): If True, a test database engine will be created. 
        If False, a regular database engine will be created. Default is False.

    Returns:
        engine: A SQLAlchemy engine object.

    Raises:
        Exception: If there is an error connecting to the database.

    Notes:
        - If testing is True, the function will create a test database engine 
          and delete any existing test database file to ensure a fresh structure.
        - If testing is False, the function will create a regular database engine
          using the specified database path.
        - The database path is determined by the BASE_DIR and db_path variables defined in the module.
        - The engine object is created using the create_engine function from the sqlalchemy module.
        - If an error occurs while connecting to the database, 
          an exception will be raised and logged using the app.logger object.

    """
    if testing:
        # Ændrer stien til en specifik test database
        test_db_path = os.path.join(BASE_DIR,"database", "test.db")
        # Sletter test.db filen hvis den eksisterer, for at sikre den bygges på ny og ikke bruger gammel struktur
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            app.logger.debug("Deleted test database, to ensure fresh structure.")
        engine = create_engine(f'sqlite:///{test_db_path}', echo=False)
        Base.metadata.create_all(engine)  # Opretter databasestrukturen baseret på dine modeller
    else:
        try:
            engine = create_engine(f'sqlite:///{db_path}', echo=False)
        except Exception as e:
            app.logger.critical(f"Failed to connect to database: {e}")
            raise
    return engine


Session = scoped_session(sessionmaker(bind=get_engine(TESTING)))
dbsession = Session()
