#!/usr/bin/env python

import sys
import daemon
import signal
import argparse

import greenstalk


class WorkerDaemon:
    def __init__(self, database, queue):
        self._database = database
        self._queue = queue
        self._interrupted = False

    def process_signal(self, signal_number, stack_frame):
        self._interrupted = True

    def _process_job(self, job):
        """
        Process one job.
        """

        print("JOB {0}: {1}".format(job.id, job.body))

    def run(self):
        """
        Process queued jobs.
        """

        # process jobs until asked to stop
        while not self._interrupted:
            try:
                job = self._queue.reserve(timeout=1)
                self._process_job(job)
                self._queue.delete(job)

            except greenstalk.TimedOutError:
                # try again
                continue


def main():
    """
    Run the node daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.01', help="beanstalk host")
    parser.add_argument('--port', type=int, default=11300, help="beanstalk port")
    parser.add_argument('--db-uri', type=str, help="database uri")
    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # TODO: connect to the database

    # connect to beanstalkd
    queue = greenstalk.Client(host=args.host, port=args.port)

    # create the worker
    worker = WorkerDaemon(database=None, queue=queue)

    # create the daemon context
    context = daemon.DaemonContext(
        files_preserve=[queue._sock],
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
        print("running...")
        worker.run()
