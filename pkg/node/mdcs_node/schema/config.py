from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Int, Dict


class NodeConfigSchema(Schema):
    """
    Serialization schema for a Node configuration.
    """

    public_host = String()
    http_port = Int()
    tcp_port = Int()
    discovery = Dict()
    instance = Dict()

    @pre_dump
    def jsonify_config(self, config):
        return {
            'public_host': config.public_host,
            'http_port': config.http_port,
            'tcp_port': config.tcp_port,
            'discovery': config.discovery.to_json(),
            'instance': config.instance}
