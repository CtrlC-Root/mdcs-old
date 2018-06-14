from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mdcs.http import HTTPServer

from .views import ReactorDetail, ReactorHealth
from .views import ActionList, ActionDetail


class ReactorHTTPServer(HTTPServer):
    """
    A server that provides the HTTP API for interacting with a Reactor daemon.
    """

    def __init__(self, config):
        super().__init__(config.http_host, config.http_port)
        self._config = config

        # register routes
        routes = (
            ('reactor_detail', '/',       ReactorDetail),
            ('reactor_health', '/health', ReactorHealth),

            ('action_list',    '/a',        ActionList),
            ('action_detail',  '/a/<uuid>', ActionDetail)
        )

        for name, pattern, view in routes:
            self.register_route(name, pattern, view)

    def server_activate(self):
        """
        Activate the server and connect to the database.
        """

        super().server_activate()
        self._database_engine = create_engine(self._config.database_url)
        self._session_factory = sessionmaker(bind=self._database_engine)

    def create_context(self, request):
        return {'config': self._config, 'session': self._session_factory()}

    def finalize_context(self, context):
        # if we do not explicitly close the session here it will be garbage collected later but potentially in a
        # different thread which will throw an exception. this is because the Session object is not thread-safe.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#is-the-session-thread-safe
        context['session'].close()
