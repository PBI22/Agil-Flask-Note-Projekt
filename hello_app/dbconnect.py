import os
from . import app
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

# Construct an absolute path to where the database file should be located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "db.sqlite")

def get_engine():
    
    if os.getenv("TESTING"):
        # Ændrer stien til en specifik test database
        test_db_path = os.path.join(BASE_DIR,"database", "test.db")
        engine = create_engine(f'sqlite:///{test_db_path}', echo=True)
        Base.metadata.create_all(engine)  # Opretter databasestrukturen baseret på dine modeller
    else:
        try:
            engine = create_engine(f'sqlite:///{db_path}', echo=True)
        except Exception as e:
            app.logger.critical(f"Failed to connect to database: {e}")
            raise
    return engine
    
Session = scoped_session(sessionmaker(bind=get_engine()))
dbsession = Session()
