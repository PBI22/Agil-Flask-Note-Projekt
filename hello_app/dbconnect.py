import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from . import app

Base = declarative_base()

# funktion til at hente database URI , baseret på om vi er i testmode eller ej
def get_database_uri(testing=False):
    if testing:
        return "sqlite:///:memory:"  # Brug in-memory database under testing
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "database", "db.sqlite")
        return f'sqlite:///{db_path}'

try:
    # Tilføj en parameter til din app's konfiguration for at angive testmode
    engine = create_engine(get_database_uri(app.config.get('TESTING', False)), echo=True)

    Session = sessionmaker(bind=engine)
    dbsession = Session()
    
except Exception as e:
    app.logger.critical(f"Failed to connect to database: {e}")
    raise
