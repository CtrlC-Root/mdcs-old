from http import HTTPStatus

from .json import JSONEncoder
from .response import Response


class View:
    """
    A class that represents an HTTP application view.
    """

    HTTP_METHODS = ['OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'DELETE']

    def __init__(self, context={}):
        self.context = context

    @property
    def allowed_methods(self):
        """
        A list of HTTP methods this view supports.
        """

        allowed_methods = []
        for method in self.HTTP_METHODS:
            handler_name = method.lower()
            if hasattr(self, handler_name):
                allowed_methods.append(method)

        return allowed_methods

    def options(self, request, **kwargs):
        """
        Default implementation of the HTTP OPTIONS method.
        """

        return Response(
            headers={'Allow': ','.join(self.allowed_methods)},
            status_code=HTTPStatus.OK)

    def handle_request(self, request):
        """
        Process a single HTTP request and return the response.
        """

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
