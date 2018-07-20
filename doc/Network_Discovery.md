# Network Discovery

Nodes, registries, and other components can use a common set of plugins in the `mdcs` library for network discovery.
Currently the following plugins are available:

* Multicast (Default)

## Multicast

The Multicast plugin typically listens on UDP port 5512 and uses the group `224.0.0.128`. Because UDP traffic is
connectionless the plugin uses an Avro schema to represent possible message values instead of a protocol definition.

* [Multicast Event Schema](../pkg/libmdcs-python/mdcs/discovery/multicast/event.avsc)
