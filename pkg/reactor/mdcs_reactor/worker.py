#!/usr/bin/env python

import argparse

import greenstalk
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import mdcs.task
import mdcs.daemon

from .models import Action, Task
from .scripting import LuaScriptBackend


class WorkerTask(mdcs.task.Task):
    def __init__(self, session_factory, queue_client):
        super().__init__(
            name='Reactor Worker',
            run=self._run,
            start=self._start,
            stop=self._stop,
            files=[queue_client._sock])

        self._session = session_factory
        self._queue = queue_client

        self._backend = LuaScriptBackend()
        self._running = False

    def _process_job(self, session, job):
        print("======== JOB {0} ========".format(job.id))
        task = session.query(Task).filter(Task.uuid == job.body).one()
        self._backend.run(task.action.content)

    def _start(self):
        self._running = True

    def _stop(self):
        self._running = False

    def _run(self):
        # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#using-thread-local-scope-with-web-applications
        # http://docs.sqlalchemy.org/en/rel_0_9/orm/session_basics.html#session-frequently-asked-questions

        while self._running:
            session = None

            try:
                job = self._queue.reserve(timeout=1)
                session = self._session()

                self._process_job(session, job)

                session.commit()
                self._queue.delete(job)

            except greenstalk.TimedOutError:
                # try again
                continue

            except Exception as e:
                print("EXC: {0}".format(e))

                # abort
                session.rollback()
                self._queue.bury(job)

            finally:
                # close the database session
                if session is not None:
                    session.close()


class WorkerDaemon(mdcs.daemon.TaskDaemon):
    def __init__(self, beanstalk_host, beanstalk_port, database_uri, background):
        super().__init__()

        # create the database engine and session factory
        self._db_engine = create_engine(database_uri, convert_unicode=True)
        self._db_session_factory = sessionmaker(bind=self._db_engine)

        # connect to the beanstalk queue
        self._queue_client = greenstalk.Client(host=beanstalk_host, port=beanstalk_port)

        # create tasks
        self.add_task(WorkerTask(
            session_factory=self._db_session_factory,
            queue_client=self._queue_client))

    def initialize_context(self):
        super().initialize_context()

        # release any open database connections and open new ones as needed
        # this is to work around not being able to specify the connection sockets
        # to the daemon context so it can keep them open when entering it
        self._db_engine.dispose()


def main():
    """
    Parse command line arguments and run the worker daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--bs-host', type=str, default='127.0.0.1', help="beanstalk host")
    parser.add_argument('--bs-port', type=int, default=11300, help="beanstalk port")
    parser.add_argument('--db-uri', type=str, help="database uri")
    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # create and run the daemon
    daemon = WorkerDaemon(
        beanstalk_host=args.bs_host,
        beanstalk_port=args.bs_port,
        database_uri=args.db_uri,
        background=args.daemon)

    daemon.run()
