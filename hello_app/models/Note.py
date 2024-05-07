from sqlalchemy import Column,ForeignKey, Integer, DateTime, Text, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Note(Base):
    """
    Note class represents a model for notes in the note taking app.

    Attributes:
        noteID (int): The unique identifier for the note.
        title (str): The title of the note.
        text (str): The content of the note.
        created (datetime): The date and time when the note was created.
        lastedited (datetime): The date and time when the note was last edited.
        imagelink (str): The link to an image associated with the note.
        author (int): The foreign key referencing the account that created the note.

    Relationships:
        account (Account): The relationship to the Account model, 
        representing the account that created the note.

    Methods:
        to_isoformat(): Converts the Note object to a dictionary with ISO formatted values.

    Example:
        note = Note()
        note.noteID = 1
        note.title = 'Example Note'
        note.text = 'This is an example note.'
        note.created = datetime(2022, 1, 1, 12, 0, 0)
        note.lastedited = datetime(2022, 1, 1, 13, 0, 0)
        note.imagelink = 'example.jpg'
        note.author = 1

    Note:
        The Note model is linked to the Account model through the author attribute, 
        which represents the account that created the note.
    """
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

    account = relationship(
        "Account",
        primaryjoin="and_(Account.accountID==Note.author)",
        foreign_keys=[author],
    )

    # Konvertere note til iso format vha. Ny funktion
    # Dette bliver gjort fordi JSON skal bruge iso format. Bruges hermed til api
    def to_isoformat(self):
        """
        Converts the Note object to a dictionary with ISO formatted values.

        Returns:
            dict: A dictionary containing the Note object's attributes in ISO format.

        Example:
            note = Note()
            note.to_isoformat()
            # Output: 
            # {
            #     'noteID': 1,
            #     'title': 'Example Note',
            #     'text': 'This is an example note.',
            #     'created': '2022-01-01T12:00:00',
            #     'lastedited': '2022-01-01T13:00:00',
            #     'imagelink': 'example.jpg',
            #     'author': 1
            # }
        """
        return {
            'noteID': self.noteID,
            'title': self.title,
            'text': self.text,
            'created': self.created.isoformat(),
            'lastedited': self.lastedited.isoformat(),
            'imagelink': self.imagelink,
            'author': self.author
        }
class Account(Base):
    """
    Account class represents a model for user accounts in the note taking app.

    Attributes:
        accountID (int): The unique identifier for the account.
        username (str): The username for the account.
        password (str): The password for the account.
        email (str): The email associated with the account.
        roleID (int): The foreign key referencing the role of the account.

    Relationships:
        role (Role): The relationship to the Role model, representing the role of the account.

    Example:
        account = Account()
        account.accountID = 1
        account.username = 'example_user'
        account.password = 'example_password'
        account.email = 'example@example.com'
        account.roleID = 1

    Note:
        The Account model is linked to the Role model through the roleID attribute, which represents the role of the account.
    """
    __tablename__ = "account"

    accountID = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=True)
    roleID = Column(Integer, ForeignKey("role.roleID"), nullable=False)

    role = relationship("Role", primaryjoin="and_(Role.roleID==Account.roleID)", foreign_keys=[roleID])

class Role(Base):
    """
    Role class represents a model for roles in the note taking app.

    Attributes:
        roleID (int): The unique identifier for the role.
        rolename (str): The name of the role.

    Example:
        role = Role()
        role.roleID = 1
        role.rolename = 'admin'

    Note:
        The Role model is used to define the roles of user accounts in the note taking app.
    """
    __tablename__ = "role"

    roleID = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(VARCHAR(255), nullable=False)
