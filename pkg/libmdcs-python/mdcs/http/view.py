from http import HTTPStatus

from .json import JSONEncoder
from .response import Response


class View:
    def handle_request(self, request):
        # check if the view supports the method
        handler_name = request.method.lower()
        if not hasattr(self, handler_name):
            return Response(HTTPStatus.METHOD_NOT_ALLOWED)

        # run the method handler
        response = getattr(self, handler_name)(request)

        # return Response objects directly
        if isinstance(response, Response):
            return response

        # create the response from a status code
        if isinstance(response, HTTPStatus):
            return Response(response)

        # create the response from JSON serialized data
        return Response(
            headers={'Content-Type': 'application/json'},
            status_code=HTTPStatus.OK,
            content=JSONEncoder().encode(response))
