import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Construct an absolute path to where the database file should be located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "db.sqlite")

engine = create_engine(f'sqlite:///{db_path}', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
