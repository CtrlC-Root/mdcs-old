class NodeConfig:
    """
    Configuration settings for a Node.
    """

    def __init__(self, public_host, bind_host, http_port, tcp_port, discovery, instance={}):
        self._public_host = public_host
        self._http_host = bind_host
        self._http_port = http_port
        self._tcp_host = bind_host
        self._tcp_port = tcp_port
        self._discovery = discovery
        self._instance = instance

    @property
    def public_host(self):
        return self._public_host

    @property
    def http_host(self):
        return self._http_host

    @property
    def http_port(self):
        return self._http_port

    @property
    def tcp_host(self):
        return self._tcp_host

    @property
    def tcp_port(self):
        return self._tcp_port

    @property
    def discovery(self):
        return self._discovery

    @property
    def instance(self):
        return self._instance
