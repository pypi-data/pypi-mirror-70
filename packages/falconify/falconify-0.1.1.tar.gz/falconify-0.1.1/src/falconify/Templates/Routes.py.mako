from .${module}RequestHandler import \
    ${module}CollectionRequestHandler
from .${module}RequestHandler import \
    ${module}ItemRequestHandler


class ${module}Routes:

    _version = '/v1/'

    def define(self, route):
        route.add_route(
            self._version + "${moduleRoute}s",
            ${module}CollectionRequestHandler())

        route.add_route(
            self._version + "${moduleRoute}s/{uuid}",
            ${module}ItemRequestHandler())
