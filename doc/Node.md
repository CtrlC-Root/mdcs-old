# Node

Nodes are responsible for interfacing with local hardware and software. Bridges, which are specialized nodes, are
responsible for interfacing with remote network services. Nodes provide an HTTP API for management and a TCP API for
high performance data access.

## HTTP API

The HTTP API is typically available over TCP port 5510.

### Node

TODO: config, health

### Devices

TODO

### Attributes

TODO

### Actions

TODO

## TCP API

The TCP API is typically available over TCP port 5511. It only supports data access operations such as reading or
writing attribute values and running actions.

### Attributes

TODO: read, write

### Actions

TODO: run
