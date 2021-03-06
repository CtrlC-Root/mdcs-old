import json
import urllib.parse


class Request:
    """
    An HTTP request.
    """

    def __init__(self, url='', headers={}, method='GET', data=None):
        # parse url
        url_parts = urllib.parse.urlparse(url)
        self.scheme = url_parts.scheme
        self.path = url_parts.path
        self.host, *extra = url_parts.netloc.split(':')
        self.port = int(extra[0]) if extra else 80
        self.method = method

        # parse query paramters
        self.params = {}
        if url_parts.params:
            for query_arg in url_parts.query.split(','):
                key, value = query_arg.split('=')
                request.params[key] = value

        # store headers
        self.headers = headers

        # initialize cached values
        self._json_data = None

    @property
    def content_type(self):
        if 'Content-Type' not in self.headers:
            return None

        return self.headers['Content-Type']

    @property
    def json(self):
        # corner case: already parsed the request data into JSON
        if self._json_data:
            return self._json_data

        # XXX there has to be a better way
        if not self.content_type.startswith('application/json'):
            raise RuntimeError("request does not contain JSON data")

        # parse, cache, and return the request data as JSON
        self._json_data = json.loads(self.data)
        return self._json_data
