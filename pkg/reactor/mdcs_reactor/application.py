from flask import Flask


# create the application
application = Flask('mdcs_reactor', instance_relative_config=True)


# register top-level utility views
@application.route('/')
def index():
    """
    Index route that provides some useful information about the web application.
    """

    return 'MDCS Reactor HTTP API'


@application.route('/health')
def health():
    """
    Check the health of the web application.
    """

    # XXX: anything to do here?
    return "healthy"


# import views after the application object exists to avoid a circular import error
from .views import *
