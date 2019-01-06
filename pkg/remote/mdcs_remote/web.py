import greenstalk
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# create the application
application = Flask('mdcs_remote', instance_relative_config=True)
# XXX application.config.from_envvar('REMOTE_CONFIG')

# XXX: local development
application.config['DATABASE_URI'] = 'sqlite:///remote.db'
application.config['BEANSTALKD_HOST'] = '127.0.0.1'
application.config['BEANSTALKD_PORT'] = 11300

# create the database engine and session factory
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session
database_engine = create_engine(application.config['DATABASE_URI'], convert_unicode=True)
database_session_factory = sessionmaker(bind=database_engine)


# manage the session database and queue connections
# http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/
# https://github.com/mayhewj/greenstalk#getting-started
@application.before_request
def initialize_session():
    g.db = database_session_factory()
    g.queue = greenstalk.Client(
        host=application.config['BEANSTALKD_HOST'],
        port=application.config['BEANSTALKD_PORT'])


@application.teardown_request
def finalize_session(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

    queue = getattr(g, 'queue', None)
    if queue is not None:
        queue.close()



# import views after the application object exists to avoid a circular import error
# disable the pycodestyle E402 warning for these lines since we know what we're doing
# https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes
from .views import Index, Health  # noqa

application.add_url_rule('/', view_func=Index.as_view('index'))
application.add_url_rule('/health', view_func=Health.as_view('health'))