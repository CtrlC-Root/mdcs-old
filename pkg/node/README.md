# node

A control system node daemon.

## Documentation

Relevant links to project documentation for this component:

* [Node](../../doc/Node.md)

## Roadmap

- [ ] More robust error handling.
- HTTP API:
  - [ ] Check if the node is healthy (HAProxy or ELB compatible).
  - [ ] Serialize attribute values using Avro JSON.
  - [ ] Validate attribute values using their Avro schema.
  - [ ] Run actions.
  - [ ] Document with Swagger.
- TCP API:
  - [ ] Run actions.
  - [ ] Add support for multiple requests over one socket.
- [ ] Investigate Python plugins.
  * https://stackoverflow.com/a/37233643/937006
- [ ] Investigate Python udev and evdev libraries for hotplug.
  * https://stackoverflow.com/a/28890654/937006
  * https://pyudev.readthedocs.io/en/latest/
  * https://python-evdev.readthedocs.io/en/latest/
