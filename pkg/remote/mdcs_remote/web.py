import greenstalk
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# create the application
application = Flask('mdcs_remote', instance_relative_config=True)
application.config.update({
    'DATABASE_URI': 'sqlite:///remote.db',
    'BEANSTALKD_HOST': 'localhost',
    'BEANSTALKD_PORT': 11300,
})

application.config.from_envvar('MDCS_REMOTE_CONFIG', silent=True)

# TODO: http://flask.pocoo.org/docs/1.0/config/#APPLICATION_ROOT

# wrap the WSGI application with a middleware to work with relative
# request paths when the application is behind a reverse proxy
# http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    '''
    Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme

        return self.app(environ, start_response)


application.wsgi_app = ReverseProxied(application.wsgi_app)

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
from .views import Index, Health   # noqa
from .views import ControlSetList, ControlSetDetail, ControlSetApply  # noqa
from .views import ControlList, ControlDetail  # noqa
from .views import TaskList, TaskDetail  # noqa

application.add_url_rule('/', view_func=Index.as_view('index'))
application.add_url_rule('/health', view_func=Health.as_view('health'))

application.add_url_rule('/controlset/', view_func=ControlSetList.as_view('controlset_list'))
application.add_url_rule('/controlset/<uuid>', view_func=ControlSetDetail.as_view('controlset_detail'))
application.add_url_rule('/controlset/<uuid>/apply', view_func=ControlSetApply.as_view('controlset_apply'))

application.add_url_rule('/control/', view_func=ControlList.as_view('control_list'))
application.add_url_rule('/control/<uuid>', view_func=ControlDetail.as_view('control_detail'))

application.add_url_rule('/task/', view_func=TaskList.as_view('task_list'))
application.add_url_rule('/task/<uuid>', view_func=TaskDetail.as_view('task_detail'))
