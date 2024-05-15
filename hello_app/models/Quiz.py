from datetime import datetime, timezone
from sqlalchemy import Boolean, Column,ForeignKey, Integer, DateTime, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Quiz(Base):
    """
    A class representing a Quiz.

    Attributes:
        quizID (int): The ID of the quiz.
        name (str): The name of the quiz.
        created (datetime): The datetime when the quiz was created.
        lastedited (datetime): The datetime when the quiz was last edited.
        accountID (int): The ID of the account associated with the quiz.
        account (Account): The account associated with the quiz.
        questions (list of Question): The questions associated with the quiz.
    """

    __tablename__ = 'quiz'

    quizID = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(255))
    created = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    lastedited = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))
    accountID = Column(Integer, ForeignKey("account.accountID"), nullable=False)

    account = relationship(
        "Account",
        primaryjoin="and_(Account.accountID==Quiz.accountID)",
        foreign_keys=[accountID],
    )

    questions = relationship("Question", backref="quiz", cascade="all, delete-orphan")

# Duplicate code from Note.py (due to time constraints and issues this will have to do, otherwise import from Note or something)
class Account(Base): # Gets accountid and username from Account
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

class Question(Base):
    """
    A class representing a question in a quiz.

    Attributes:
        questionID (int): The unique identifier for the question.
        text (str): The text of the question.
        quizID (int): The ID of the quiz that the question belongs to.
    """
    __tablename__ = 'question'

    questionID = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(VARCHAR(255))
    quizID = Column(Integer, ForeignKey('quiz.quizID'))

    choices = relationship("Choice", backref="question", cascade="all, delete-orphan")

class Choice(Base):
    """
    The Choice class represents a choice for a question in a quiz.

    Attributes:
        choiceID (int): The unique identifier for the choice.
        text (str): The text of the choice.
        iscorrect (bool): Indicates whether the choice is correct or not.
        questionID (int): The foreign key referencing the question that the choice belongs to.
    """
    __tablename__ = 'choice'

    choiceID = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(VARCHAR(255))
    iscorrect = Column(Boolean)
    questionID = Column(Integer, ForeignKey('question.questionID'))
