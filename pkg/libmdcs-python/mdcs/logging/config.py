import sys
import logging

from .formatter import JSONFormatter


class LoggingConfig:
    """
    Logging configuration.
    """

    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    def __init__(self, log_level=logging.INFO):
        self._log_level = log_level
        self._output_stream = sys.stdout

    @classmethod
    def define_args(cls, parser):
        """
        Add logging specific command line arguments to an argparse ArgumentParser instance.
        """

        parser.add_argument(
            '--log-level',
            type=str,
            default='info',
            choices=list(cls.LOG_LEVELS.keys()),
            help="minimum log level")

    @classmethod
    def from_args(cls, args):
        """
        Create a logging configuration object from parsed command line arguments.
        """

        return LoggingConfig(log_level=cls.LOG_LEVELS.get(args.log_level))

    @property
    def files(self):
        """
        Open file descriptors.
        """

        return [self._output_stream]

    def apply(self):
        """
        Apply the logging configuration to the root logger.
        """

        # create the handler
        # https://docs.python.org/3.6/howto/logging.html#useful-handlers
        # https://docs.python.org/3.6/library/logging.handlers.html#logging.StreamHandler
        root_handler = logging.StreamHandler(stream=self._output_stream)
        root_handler.setFormatter(JSONFormatter())

        # configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self._log_level)
        root_logger.addHandler(root_handler)
