from abc import ABCMeta, abstractmethod


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
