from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/db.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()