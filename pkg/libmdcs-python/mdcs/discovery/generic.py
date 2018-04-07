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
