from abc import ABCMeta, abstractmethod

from .registry import Registry


class DiscoveryConfig(metaclass=ABCMeta):
    """
    Abstract base class for network discovery backend configuration.
    """

    @classmethod
    @abstractmethod
    def define_args(cls, parser):
        """
        Add backend specific command line arguments to an argparse ArgumentParser instance.
        """

        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_args(cls, args):
        """
        Create a configuration object from parsed command line arguments.
        """

        raise NotImplementedError()

    @abstractmethod
    def create_backend(self):
        """
        Create an instance of the discovery backend with this configuration.
        """

        raise NotImplementedError()

    @abstractmethod
    def to_json(self):
        """
        Get settings in a dictionary suitable for JSON serialization.
        """

        raise NotImplementedError()


class DiscoveryBackend(metaclass=ABCMeta):
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

    @abstractmethod
    def create_publish_task(self):
        """
        Create a task to publish the contents of a registry.
        """

        raise NotImplementedError()

    @abstractmethod
    def create_subscribe_task(self):
        """
        Create a task to discover nodes and devices.
        """

        raise NotImplementedError()
