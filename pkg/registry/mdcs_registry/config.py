class RegistryDaemonConfig:
    """
    Configuration settings for a Registry daemon.
    """

    def __init__(self, public_host, bind_host, http_port, logging, discovery, background):
        self._public_host = public_host
        self._http_host = bind_host
        self._http_port = http_port

        self._logging = logging
        self._discovery = discovery
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
    def logging(self):
        return self._logging

    @property
    def discovery(self):
        return self._discovery

    @property
    def background(self):
        return self._background

    def to_json(self):
        """
        Configuration settings in a dictionary suitable for JSON serialization.
        """

        return {
            'host': self.public_host,
            'httpPort': self.http_port,
            'discovery': self.discovery.to_json()}
