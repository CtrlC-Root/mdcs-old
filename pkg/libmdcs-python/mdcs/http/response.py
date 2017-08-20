from http import HTTPStatus


class Response:
    def __init__(self, status_code=HTTPStatus.OK, headers={}, content=None):
        self.status_code = status_code
        self.headers = headers
        self.content = content

        # shortcut for creating a generic response from an HTTP status code
        if not self.content:
            self.headers['Content-Type'] = 'text/plain'
            self.content = self.status_code.phrase
