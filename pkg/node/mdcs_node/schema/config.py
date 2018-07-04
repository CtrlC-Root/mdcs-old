from marshmallow import Schema, post_load, pre_dump
from marshmallow.fields import String, Int, Dict

from mdcs.discovery.multicast import MulticastDiscoveryConfig

from mdcs_node.node import NodeConfig


class NodeConfigSchema(Schema):
    """
    Serialization schema for a Node configuration.
    """

    public_host = String()
    http_port = Int()
    tcp_port = Int()
    discovery = Dict()
    instance = Dict()

    @post_load
    def create_config(self, data):
        # XXX: create the appropriate config object based on data['discovery'] contents
        discovery = MulticastDiscoveryConfig(
            public_host=data['discovery']['host'],
            group=data['discovery']['group'],
            port=data['discovery']['port'])

        return NodeConfig(
            public_host=data['public_host'],
            bind_host=None,  # XXX: we don't export this setting, maybe we should?
            http_port=data['http_port'],
            tcp_port=data['tcp_port'],
            discovery=discovery,
            instance=data['instance'])

    @pre_dump
    def jsonify_config(self, config):
        return {
            'public_host': config.public_host,
            'http_port': config.http_port,
            'tcp_port': config.tcp_port,
            'discovery': config.discovery.to_json(),
            'instance': config.instance}
