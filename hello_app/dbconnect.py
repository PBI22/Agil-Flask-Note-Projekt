import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import app
# Construct an absolute path to where the database file should be located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "db.sqlite")
try:
    engine = create_engine(f'sqlite:///{db_path}', echo=True)

    Session = sessionmaker(bind=engine)
    dbsession = Session()
    
except Exception as e:
    app.logger.critical(f"Failed to connect to database: {e}")
    raise
