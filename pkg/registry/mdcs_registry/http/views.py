from http import HTTPStatus

from mdcs.http.view import View


class RegistryDetail(View):
    def get(self, request, config, registry):
        return {'config': config.to_json()}


class RegistryHealth(View):
    def get(self, request, config, registry):
        # TODO: implement this (compatible with HAProxy)
        return HTTPStatus.OK


class Nodes(View):
    def get(self, request, config, registry):
        return dict(map(
            lambda n: (n.name, {'host': n.host, 'httpPort': n.http_port, 'tcpPort': n.tcp_port}),
            registry.nodes.values()))


class Devices(View):
    def get(self, request, config, registry):
        return dict(map(
            lambda d: (d.name, {'node': d.node}),
            registry.devices.values()))
