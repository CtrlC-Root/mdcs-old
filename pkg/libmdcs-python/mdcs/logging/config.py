import sys
import logging

from .json import JSONFormatter
from .plain import PlainFormatter


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

    LOG_FORMATTERS = {
        'plain': PlainFormatter,
        'json': JSONFormatter,
    }

    def __init__(self, level=logging.INFO, format='plain'):
        self._level = level
        self._format = format
        self._output_stream = sys.stdout

        if self._level not in self.LOG_LEVELS.keys():
            raise ValueError("{0} is not a valid log level".format(self._level))

        if self._format not in self.LOG_FORMATTERS.keys():
            raise ValueError("{0} is not a valid format".format(self._format))

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

        format_flags = parser.add_mutually_exclusive_group()

        format_flags.add_argument(
            '--log-plain',
            dest='log_format',
            action='store_const',
            const='plain',
            help='use plain text formatting')

        format_flags.add_argument(
            '--log-json',
            dest='log_format',
            action='store_const',
            const='json',
            help='use JSON formatting')

    @classmethod
    def from_args(cls, args):
        """
        Create a logging configuration object from parsed command line arguments.
        """

        return LoggingConfig(
            level=args.log_level,
            format=(args.log_format if args.log_format else 'plain'))

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

        # create the formatter
        formatter_class = self.LOG_FORMATTERS[self._format]
        formatter = formatter_class()

        # create the handler
        # https://docs.python.org/3.6/howto/logging.html#useful-handlers
        # https://docs.python.org/3.6/library/logging.handlers.html#logging.StreamHandler
        root_handler = logging.StreamHandler(stream=self._output_stream)
        root_handler.setFormatter(formatter)

        # configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.LOG_LEVELS[self._level])
        root_logger.addHandler(root_handler)
