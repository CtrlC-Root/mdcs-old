import re
from collections import namedtuple


class InvalidRoutePattern(RuntimeError):
    pass


class RoutePattern:
    """
    A route pattern that matches URLs and can include dynamic variables.
    """

    VariableType = namedtuple('Type', ['regex', 'function'])

    PATTERN_SEPARATOR = '/'
    PATTERN_VARIABLE = re.compile(r"<(?P<name>[a-zA-Z0-9]+)(:(?P<type>[a-zA-Z0-9]+))?>")
    PATTERN_TYPES = {
        'int': VariableType(r"[0-9]+", int),
        'str': VariableType(r"[0-9a-zA-Z_\.\-]+", str)
    }

    @classmethod
    def parse_pattern(cls, pattern):
        """
        Parse a pattern into a regular expression object and a dictionary of variable (name, type) pairs.
        """

        parts = []
        variables = {}

        # process pattern components
        for part in pattern.split(cls.PATTERN_SEPARATOR):
            # ignore empty parts
            if not part:
                continue

            # pass non-variable parts through
            match = cls.PATTERN_VARIABLE.match(part)
            if not match:
                parts.append(part)
                continue

            # retrieve variable name and type
            groups = match.groupdict()
            var_name = groups['name']
            var_type = groups['type'] or 'str'

            if var_type not in cls.PATTERN_TYPES:
                raise InvalidRoutePattern("invalid variable type: {0}".format(var_type))

            # substitue a part that will extract the variable value
            parts.append("(?P<{0}>{1})".format(var_name, cls.PATTERN_TYPES[var_type].regex))
            variables[var_name] = cls.PATTERN_TYPES[var_type]

        # return the combined regular expression and variable map
        regex = re.compile("^/{0}$".format(cls.PATTERN_SEPARATOR.join(parts)))
        return regex, variables

    def __init__(self, pattern):
        self.pattern = pattern
        self.regex, self.variables = self.parse_pattern(self.pattern)

    def parse(self, url):
        """
        Parse the given URL and return a dict of variable values. If the URL does not match the pattern return None.
        """

        # match the url
        match = self.regex.match(url)
        if not match:
            return None

        raw_values = match.groupdict()

        # parse variable values
        values = {}
        for var_name, var_type in self.variables.items():
            values[var_name] = var_type.function(raw_values[var_name])

        # return type cast variable values
        return values
