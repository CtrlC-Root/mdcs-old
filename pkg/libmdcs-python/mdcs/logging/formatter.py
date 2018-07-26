import json
import logging
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    """
    JSON encoder for LogRecord object data.
    """

    def default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()

        return super().default(value)


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for LogRecord objects.
    """

    def __init__(self):
        super().__init__()
        self._encoder = JSONEncoder()

    def format(self, record):
        """
        Format a record into a JSON encoded dictionary.
        """

        record_data = {
            'message': record.getMessage(),
            'timestamp': datetime.fromtimestamp(record.created),

            'logger': record.name,
            'function': record.funcName,
            'level': record.levelname,
            'line': record.lineno,

            # only if record.pathname is available
            'module': record.module,
            'path': record.pathname,
            'file': record.filename,

            'pid': record.process,
            'tid': record.thread,
            'process': record.processName,
            'thread': record.threadName,
        }

        # record created with dictionary as single argument, expose arguments
        if record.args and isinstance(record.args, dict):
            record_data['args'] = record.args

        # remove keys for absent values
        for key, value in record_data.items():
            if value is None:
                del record_data[key]

        # optional fields
        if record.exc_info:
            record_data['exception'] = self.formatException(record.exc_info)

        if record.stack_info:
            # TODO: maybe we should store this as an array of dictionaries?
            record_data['stack'] = self.formatStack(record.stack_info)

        # return a JSON formatted dictionary
        return self._encoder.encode(record_data)
