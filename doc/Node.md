# Node

Nodes are responsible for interfacing with local hardware and software. Bridges, which are specialized nodes, are
responsible for interfacing with remote network services. Nodes provide an HTTP API for management and optionally a
TCP API for high performance data access.

## HTTP API

The HTTP API is typically available over TCP port 5510. It's a RESTful JSON API with CORS support and can be consumed
directly from web browsers.

TODO: document with swagger

## TCP API

The TCP API is typically available over TCP port 5511. It only supports data access operations such as reading or
writing attribute values and running actions. It uses Avro to encode messages and data values to binary for
correctness and better performance.

* [Avro Documentation](http://avro.apache.org/docs/current/spec.html#Protocol+Declaration)
* [TCP API Protocol](../pkg/libmdcs-python/mdcs/tcp/api.avpr)

## Network Discovery

Nodes use the Multicast plugin for network discovery.

* [Network Discovery](Network_Discovery.md)
