# Node

Nodes are responsible for interfacing with local hardware and software. Bridges, which are specialized nodes, are
responsible for interfacing with remote network services. Nodes provide an HTTP API for management and optionally a
TCP API for high performance data access.

## HTTP API

The HTTP API is typically available over TCP port 5510.

TODO: document with swagger

## TCP API

The TCP API is typically available over TCP port 5511. It only supports data access operations such as reading or
writing attribute values and running actions. It uses the Avro binary serialization format for requests and responses.
The complete request and response syntax is documented with Avro syntax files in the `libmdcs-python` package.

### Attributes

Read an attribute value request and response:

```json
{
    "name": "read",
    "type": "record",
    "doc": "read device attribute value",
    "fields": [
        {"name": "device", "type": "string"},
        {"name": "attribute", "type": "string"}
    ]
}
```

```json
{
      "name": "value",
      "type": "record",
      "doc": "device attribute value",
      "fields": [
          {"name": "when", "type": "long", "logicalType": "timestamp-millis"},
          {"name": "value", "type": "bytes"}
      ]
  }
```

Write an attribute value request and response:

```json
{
    "name": "write",
    "type": "record",
    "doc": "write device attribute value",
    "fields": [
        {"name": "device", "type": "string"},
        {"name": "attribute", "type": "string"},
        {"name": "value", "type": "bytes"}
    ]
}
```

```json
{
    "name": "confirm",
    "type": "record",
    "doc": "device attribute write confirmation",
    "fields": [
        {"name": "when", "type": "long", "logicalType": "timestamp-millis"}
    ]
}
```

### Actions

Run an action request and response:

```json
{
      "name": "run",
      "type": "record",
      "doc": "run device action",
      "fields": [
          {"name": "device", "type": "string"},
          {"name": "action", "type": "string"},
          {"name": "input", "type": "bytes"}
      ]
  }
```

```json
{
    "name": "result",
    "type": "record",
    "doc": "device action result",
    "fields": [
        {"name": "when", "type": "long", "logicalType": "timestamp-millis"},
        {"name": "output", "type": "bytes"}
    ]
}
```
