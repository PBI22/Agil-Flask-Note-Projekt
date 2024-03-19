from sqlalchemy import Column, String,ForeignKey, Integer, DateTime, Text, VARCHAR
from sqlalchemy.orm import declarative_base, relationship
""""
I want to make a model for my note taking app, first im making the model "Note", which has the following fields:
- id INT
- title VARCHAR(255)
- text TEXT
- created DATETIME
- LastEdited DATETIME 
- imagelink VARCHAR(255)
- account_ID INT (FK)
"""

Base = declarative_base()

class Note(Base):
    # Tabel navn i database
    __tablename__ = "note"
    
    # Kolonner i database
    noteID = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(VARCHAR(255), nullable=False)
    text = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    lastedited = Column(DateTime, nullable=True)
    imagelink = Column(VARCHAR(255), nullable=True)
    author = Column(Integer, ForeignKey("account.accountID"), nullable=False)

    account = relationship("Account", primaryjoin="and_(Account.accountID==Note.author)", foreign_keys=[author])


    #Konvertere note til iso format vha. Ny funktion
    #Dette bliver gjort fordi JSON skal bruge iso format. Bruges hermed til api
    def to_isoformat(self):
        return {
            'noteID': self.noteID,
            'title': self.title,
            'text': self.text,
            'created': self.created.isoformat(),
            'lastedited': self.lastedited.isoformat() if self.lastedited else None,
            'imagelink': self.imagelink,
            'author': self.author
        }
class Account(Base):
    __tablename__ = "account"

    accountID = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False)

class Role(Base):
    __tablename__ = "role"

    roleID = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(VARCHAR(255), nullable=False)

class AccountRole(Base):
    __tablename__ = "accountrole"

    id = Column(Integer, primary_key=True, autoincrement=True)
    accountID = Column(Integer, ForeignKey("account.accountID"), nullable=False)
    roleID = Column(Integer, ForeignKey("role.roleID") ,nullable=False)

    account = relationship("Account", foreign_keys=[accountID])
    role = relationship("Role", foreign_keys=[roleID])
