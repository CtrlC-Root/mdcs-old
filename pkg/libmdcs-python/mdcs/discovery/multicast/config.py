from mdcs.discovery.generic import DiscoveryConfig

from .backend import MulticastDiscoveryBackend


class MulticastDiscoveryConfig(DiscoveryConfig):
    """
    Multicast network discovery configuration settings.
    """

    def __init__(self, public_host, group, port):
        """
        Create a configuration object.
        """

        self.public_host = public_host
        self.group = group
        self.port = port

    @classmethod
    def define_args(cls, parser):
        """
        Add backend specific command line arguments to an argparse ArgumentParser instance.
        """

        parser.add_argument(
            '--discovery-mcast-host',
            type=str,
            default='0.0.0.0',
            help="Multicast discovery listen address")

        parser.add_argument(
            '--discovery-mcast-port',
            type=int,
            default=5512,
            help="Multicast discovery port")

        parser.add_argument(
            '--discovery-mcast-group',
            type=str,
            default='224.0.0.128',
            help="Multicast discovery group address")

    @classmethod
    def from_args(cls, args):
        """
        Create a configuration object from parsed command line arguments.
        """

        return cls(public_host=args.mcast_host, group=args.mcast_group, port=args.mcast_port)

    def create_backend(self):
        """
        Create an instance of the discovery backend with this configuration.
        """

        return MulticastDiscoveryBackend(self)
