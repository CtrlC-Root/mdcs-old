#!/usr/bin/env python

import sys
import daemon
import signal
import argparse

import greenstalk
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Action, Task


class WorkerDaemon:
    def __init__(self, session_factory, queue_client):
        self._session = session_factory
        self._queue = queue_client
        self._interrupted = False

    def process_signal(self, signal_number, stack_frame):
        self._interrupted = True

    def _process_job(self, session, job):
        """
        Process one job.
        """

        print("JOB {0}: {1}".format(job.id, job.body))

        task = session.query(Task).filter(Task.uuid == job.body).one()
        print(">> Task: {0}".format(task))
        print(">> Action: {0}".format(task.action))

    def run(self):
        """
        Process queued jobs.
        """

        # process jobs until asked to stop
        while not self._interrupted:
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

            except:
                # abort
                session.rollback()
                self._queue.bury(job)

            finally:
                # close the database session
                if session is not None:
                    session.close()


def main():
    """
    Run the node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--bs-host', type=str, default='127.0.0.1', help="beanstalk host")
    parser.add_argument('--bs-port', type=int, default=11300, help="beanstalk port")
    parser.add_argument('--db-uri', type=str, help="database uri")
    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # connect to the database
    database_engine = create_engine(args.db_uri, convert_unicode=True)
    database_session_factory = sessionmaker(bind=database_engine)

    # connect to beanstalkd
    queue_client = greenstalk.Client(host=args.bs_host, port=args.bs_port)

    # create the worker
    worker = WorkerDaemon(
        session_factory=database_session_factory,
        queue_client=queue_client)

    # create the daemon context
    context = daemon.DaemonContext(
        files_preserve=[queue_client._sock],
        signal_map={
            signal.SIGTERM: worker.process_signal,
            signal.SIGINT: worker.process_signal
        })

    if not args.daemon:
        # run the process in the foreground
        context.detach_process = False

        # preserve standard file descriptors
        context.stdin = sys.stdin
        context.stdout = sys.stdout
        context.stderr = sys.stderr

    # run the worker in the daemon context
    with context:
        # release any open database connections and open new ones as needed
        # this is to work around not being able to specify the connection sockets
        # to the daemon context
        database_engine.dispose()

        # run the worker
        print("running...")
        worker.run()
