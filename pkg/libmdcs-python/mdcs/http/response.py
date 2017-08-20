from http import HTTPStatus


class Response:
    def __init__(self, headers={}, status_code=HTTPStatus.OK, content=None):
        self.headers = headers
        self.status_code = status_code
        self.content = content
