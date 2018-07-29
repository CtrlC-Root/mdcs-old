#!/usr/bin/env python

import logging
import argparse

import greenstalk
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import mdcs.task
import mdcs.daemon
from mdcs.logging import LoggingConfig

from .models import Action, Task, TaskState
from .scripting.lua import LuaScriptConfig


class WorkerTask(mdcs.task.Task):
    def __init__(self, session_factory, queue_client, script_backend):
        super().__init__(
            name='Reactor Worker',
            run=self._run,
            start=self._start,
            stop=self._stop,
            files=[queue_client._sock]) # XXX: any way not to access private property?

        self._session = session_factory
        self._queue = queue_client
        self._backend = script_backend
        self._running = False

        self.logger = logging.getLogger(__name__)

    def _process_job(self, session, job):
        self.logger.info("processing job {job_id}: {job_body}", {'job_id': job.id, 'job_body': job.body})

        task = session.query(Task).filter(Task.uuid == job.body).one()
        if task.state != TaskState.PENDING:
            self.logger.info("skipping {task_state} task", {'task_state': task.state.name})
            return

        task.state = TaskState.RUNNING
        session.add(task)
        session.commit()

        try:
            self._backend.run(task.action.content)

        except Exception as e:
            task.state = TaskState.FAILED
            task.output = str(e)
            raise

        else:
            task.state = TaskState.COMPLETED

        finally:
            session.add(task)
            session.commit()

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
                self._queue.delete(job)

            except greenstalk.TimedOutError:
                # try again
                continue

            # XXX: catch more specific exceptions
            except Exception as e:
                self.logger.error("error while running job {job_id}", {'job_id': job.id}, exc_info=e)
                self._queue.bury(job)

            finally:
                # close the database session
                if session is not None:
                    session.rollback()
                    session.close()


class WorkerDaemon(mdcs.daemon.Daemon):
    def __init__(self, beanstalk_host, beanstalk_port, database_uri, script_config, logging_config, background):
        super().__init__(logging_config=logging_config, background=background)

        # create the database engine and session factory
        self._db_engine = create_engine(database_uri, convert_unicode=True)
        self._db_session_factory = sessionmaker(bind=self._db_engine)

        # connect to the beanstalk queue
        self._queue_client = greenstalk.Client(host=beanstalk_host, port=beanstalk_port)

        # create tasks
        self.add_task(WorkerTask(
            session_factory=self._db_session_factory,
            queue_client=self._queue_client,
            script_backend=script_config.create_backend()))

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
    LuaScriptConfig.define_args(parser)
    LoggingConfig.define_args(parser)

    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # configure logging
    logging_config = LoggingConfig.from_args(args)
    logging_config.apply()

    # create and run the daemon
    daemon = WorkerDaemon(
        beanstalk_host=args.bs_host,
        beanstalk_port=args.bs_port,
        database_uri=args.db_uri,
        script_config=LuaScriptConfig.from_args(args),
        logging_config=logging_config,
        background=args.daemon)

    daemon.run()
