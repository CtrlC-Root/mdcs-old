class NodeDaemonConfig:
    """
    Configuration settings for a Node daemon.
    """

    def __init__(self, public_host, bind_host, http_port, tcp_port, discovery, background):
        self._public_host = public_host

        # HTTP API
        self._http_host = bind_host
        self._http_port = http_port

        # TCP API
        self._tcp_host = bind_host
        self._tcp_port = tcp_port

        # Discovery
        self._discovery = discovery

        # Daemon
        self._background = background

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
    def background(self):
        return self._background

    def to_json(self):
        """
        Get settings in a dictionary suitable for JSON serialization.
        """

        return {
            'host': self.public_host,
            'httpPort': self.http_port,
            'tcpPort': self.tcp_port,
            'discovery': self.discovery.to_json()}
