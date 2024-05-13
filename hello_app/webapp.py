# Entry point for the application.
# pylint: disable=W0611
from . import app    # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.
# pylint: enable=W0611
