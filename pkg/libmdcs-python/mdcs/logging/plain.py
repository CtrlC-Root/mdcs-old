import logging


class PlainFormatter(logging.Formatter):
    """
    Plain text formatter for LogRecord objects.
    """

    def __init__(self):
        super().__init__()
