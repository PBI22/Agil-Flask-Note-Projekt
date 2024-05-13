"""
Gør vores models mappe til en package, så vi har alle vores models i.
"""

from .Note import Note, Account, Role, Base
from .FlaskForms import LoginForm, SignUpForm, NoteForm, EditNoteForm
