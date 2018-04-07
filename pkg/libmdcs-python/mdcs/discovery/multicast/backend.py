from mdcs.task import Task

from .publish import MulticastPublishServer
from .subscribe import MulticastSubscribeServer


def MulticastDiscoveryBackend(DiscoveryBackend):
    """
    Multicast network discovery backend.
    """

    def __init__(self, config):
        super().__init__(config)

    def create_publish_task(self):
        """
        Create a task to publish the contents of a registry.
        """

        server = MulticastPublishServer(self.config, self.publish)
        return Task("Multicast Discovery Publish", server.run, stop=server.shutdown, files=[server.socket])

    def create_subscribe_task(self):
        """
        Create a task to discover nodes and devices.
        """

        server = MulticastSubscribeServer(self.config, self.discovered)
        return Task("Multicast Discovery Subscribe", server.run, stop=server.shutdown, files=[server.socket])
