import lupa
import requests
import urllib.parse

from mdcs.discovery import Registry
from mdcs_remote.scripting.generic import ScriptBackend

from .registry import RegistryProxy


class LuaScriptBackend(ScriptBackend):
    """
    A Lua script backend.
    """

    def __init__(self, config):
        self._config = config
        self._registry = Registry()

    def _sync_registry(self):
        """
        Fetch nodes and devices from the remote registry.
        """

        self._registry.clear()

        # fetch nodes
        response = requests.get(urllib.parse.urljoin(self._config.registry_url, 'n'))
        if response.status_code != 200:
            raise RuntimeError('failed to retrieve registry nodes: {0}'.format(response))

        for node_name, node_config in response.json().items():
            self._registry.add_node(
                name=node_name,
                host=node_config['host'],
                http_port=node_config['httpPort'],
                tcp_port=node_config['tcpPort'])

        # fetch devices
        response = requests.get(urllib.parse.urljoin(self._config.registry_url, 'd'))
        if response.status_code != 200:
            raise RuntimeError('failed to retrieve registry devices: {0}'.format(response))

        for device_name, device_config in response.json().items():
            self._registry.add_device(
                name=device_name,
                node=device_config['node'])

    def run(self, script):
        self._sync_registry()

        runtime = lupa.LuaRuntime(unpack_returned_tuples=True)
        globals = runtime.globals()
        globals['registry'] = RegistryProxy(runtime, self._registry)

        runtime.execute(script)
