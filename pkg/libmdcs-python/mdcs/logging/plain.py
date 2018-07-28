import logging


class PlainFormatter(logging.Formatter):
    """
    Plain text formatter for LogRecord objects.
    """

    def __init__(self):
        super().__init__(
            fmt='[%(asctime)-15s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            style='%')
