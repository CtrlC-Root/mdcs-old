from abc import ABCMeta


class DiscoveryConfig(metaclass=ABCMeta):
    """
    Abstract base class for network discovery backend configuration.
    """

    @classmethod
    def define_args(cls, parser):
        """
        Add backend specific command line arguments to an argparse ArgumentParser instance.
        """

        raise NotImplementedError()

    @classmethod
    def from_args(cls, args):
        """
        Create a configuration object from parsed command line arguments.
        """

        raise NotImplementedError()

    def create_backend(self):
        """
        Create an instance of the discovery backend with this configuration.
        """

        raise NotImplementedError()

    def to_json(self):
        """
        Get settings in a dictionary suitable for JSON serialization.
        """

        raise NotImplementedError()


def DiscoveryBackend(metaclass=ABCMeta):
    """
    Abstract base class for network discovery backends.
    """

    def __init__(self, config):
        # store the config
        self.config = config

        # create a registry for nodes and devices we want to publish
        self.publish = Registry()

        # create a registry for nodes and devices we have discovered
        self.discovered = Registry()

    def create_publish_task(self):
        """
        Create a task to publish the contents of a registry.
        """

        raise NotImplementedError()

    def create_subscribe_task(self):
        """
        Create a task to discover nodes and devices.
        """

        raise NotImplementedError()
