import os
from . import app
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
TESTING = os.environ.get("TESTING", False)
# Construct an absolute path to where the database file should be located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "db.sqlite")

def get_engine(Testing = False):

    if Testing:
        # Ændrer stien til en specifik test database
        test_db_path = os.path.join(BASE_DIR,"database", "test.db")
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