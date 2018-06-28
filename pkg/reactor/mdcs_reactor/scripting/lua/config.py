from mdcs_reactor.scripting.generic import ScriptConfig

from .backend import LuaScriptBackend


class LuaScriptConfig(ScriptConfig):
    """
    Lua script backend configuration settings.
    """

    def __init__(self, registry_url):
        """
        Create a configuration object.
        """

        self.registry_url = registry_url

    @classmethod
    def define_args(cls, parser):
        """
        Add backend specific command line arguments to an argparse ArgumentParser instance.
        """

        parser.add_argument(
            '--registry-url',
            type=str,
            default='http://localhost:5520/',
            help="registry url")

    @classmethod
    def from_args(cls, args):
        """
        Create a configuration object from parsed command line arguments.
        """

        return cls(registry_url=args.registry_url)

    def create_backend(self):
        """
        Create an instance of the discovery backend with this configuration.
        """

        return LuaScriptBackend(self)

    def to_json(self):
        """
        Get settings in a dictionary suitable for JSON serialization.
        """

        return {'registryUrl': self.registry_url}
