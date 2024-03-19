import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def init_database(app):
    engine = create_engine(get_database_uri(app.config.get('TESTING', False)), echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

def get_database_uri(testing=False):
    if testing:
        return "sqlite:///:memory:"
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "database", "db.sqlite")
        return f'sqlite:///{db_path}'