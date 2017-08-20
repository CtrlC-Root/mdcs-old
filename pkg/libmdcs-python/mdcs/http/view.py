from http import HTTPStatus

from .json import JSONEncoder
from .response import Response


class View:
    def __init__(self, context={}):
        self.context = context

    def handle_request(self, request):
        # check if the view supports the method
        handler_name = request.method.lower()
        if not hasattr(self, handler_name):
            return Response(HTTPStatus.METHOD_NOT_ALLOWED)

        # run the method handler
        handler = getattr(self, handler_name)
        response = handler(request, **self.context)

        # create an empty response if necessary
        if response is None:
            return Response()

        # return Response objects directly
        if isinstance(response, Response):
            return response

        # create the response from a status code
        if isinstance(response, HTTPStatus):
            return Response(response)

        # create the response from a tuple of status code and message
        if isinstance(response, tuple) and len(response) == 2:
            return Response(
                headers={'Content-Type': 'text/plain'},
                status_code=response[0],
                content=response[1])

        # create the response from JSON serialized data
        return Response(
            headers={'Content-Type': 'application/json'},
            status_code=HTTPStatus.OK,
            content=JSONEncoder().encode(response))
