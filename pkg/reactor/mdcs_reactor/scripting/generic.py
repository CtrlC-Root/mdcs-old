from abc import ABCMeta, abstractmethod


class ScriptConfig(metaclass=ABCMeta):
    """
    Abstract base class for script backend configuration.
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
        Create an instance of the script backend with this configuration.
        """

        raise NotImplementedError()


class ScriptBackend(metaclass=ABCMeta):
    """
    A base class for script backends.
    """

    @abstractmethod
    def run(self, script):
        """
        Run a script.
        """

        raise NotImplementedError()
