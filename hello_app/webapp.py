"""
This code snippet is not a class, function, or method.
It is a block of code that serves as an entry point for an application.
It imports the 'app' module for application discovery by the 'flask' command
and the 'views' module for import side-effects of setting up routes. 
"""

# pylint: disable=W0611
from . import app  # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

# pylint: enable=W0611
