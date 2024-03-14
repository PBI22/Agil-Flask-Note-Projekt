from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

def get_database_path():
    # Få den aktuelle filplacering for denne Python-fil
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Konstruér den fulde sti til databasen
    database_path = os.path.join(current_dir, '..', 'artefakter', 'db', 'sqlitetest.sqlite')

    return database_path

engine = create_engine('sqlite:///artefakter/db/sqlitetest.sqlite', echo=True)

Base = declarative_base()

class Role(Base):
    __tablename__ = "role"
    roleid = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Role(id='%s', rolename='%s')>" % (
            self.roleid,
            self.name
        )
    
Session = sessionmaker(bind=engine)
session = Session()

new_role = Role(roleid=2, name="admin")
session.add(new_role)
session.commit()

for instance in session.query(Role).order_by(Role.roleid):
    print(instance.roleid, instance.name)

