import lupa

from mdcs_reactor.scripting.generic import ScriptBackend


class LuaScriptBackend(ScriptBackend):
    """
    A Lua script backend.
    """

    def __init__(self):
        self._registry_proxy = RegistryProxy('http://localhost:5520') # XXX pass in as config

    def run(self, script):
        self._registry_proxy.refresh()

        runtime = lupa.LuaRuntime(unpack_returned_tuples=True)
        globals = runtime.globals()

        self._registry_proxy.set_runtime(runtime) # TODO remove this, debugging only
        globals['registry'] = self._registry_proxy

        runtime.execute(script)
