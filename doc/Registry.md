# Registry

Registries are responsible for monitoring the local network for Nodes and connected Devices. Registries provide an
HTTP API for retrieving the currently available nodes and devices.

## HTTP API

The HTTP API is typically available over TCP port 5520. It's a RESTful JSON API with CORS support and can be consumed
directly from web browsers.

TODO: document with swagger

## Network Discovery

Registries use the Multicast plugin for network discovery.

* [Network Discovery](Network_Discovery.md)
