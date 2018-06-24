from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# create the application
application = Flask('mdcs_reactor', instance_relative_config=True)
application.config['DATABASE_URI'] = 'sqlite:///reactor.db'


# create the database engine and session factory
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session
database_engine = create_engine(application.config['DATABASE_URI'], convert_unicode=True)
database_session_factory = sessionmaker(bind=database_engine)


# create and finalize a database session
# http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/
@application.before_request
def create_db_session():
    g.db = database_session_factory()


@application.teardown_request
def finalize_db_session(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


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
# disable the pycodestyle E402 warning for this one line since we know what we're doing
# https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes
from .views import *  # noqa
