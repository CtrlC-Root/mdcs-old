# Roadmap

- [ ] Python Common Library:
  - [x] Device, Attribute, and Action base classes.
  - [x] Node server base class.
  - [ ] Node server structured logging.
  - [ ] Node server robust exception handling.
  - [ ] Node server HTTP API interface:
    - [x] Retrieve node name and configuration.
    - [ ] Check if the node is healthy (HAProxy or ELB compatible).
    - [x] Retrieve a list of devices.
    - [x] Retrieve a list of device attributes and actions.
    - [x] Retrieve information about an attribute.
    - [x] Retrieve information about an action.
    - [x] Read an attribute value.
    - [x] Write an attribute value.
    - [ ] Validate attribute values using Avro schema.
    - [ ] Run an action.
  - [ ] Node server TCP API interface:
    - [x] Read an attribute value.
    - [x] Write an attribute value.
    - [ ] Run an action.
    - [ ] Investigate using Avro IPC framework?
  - [ ] Node server Multicast UDP interface:
    - [ ] Design the protocol.
- [ ] Python Node:
  - [ ] Investigate Python plugins.
    * https://stackoverflow.com/a/37233643/937006
  - [ ] Investigate Python udev and evdev libraries.
    * https://stackoverflow.com/a/28890654/937006
    * https://pyudev.readthedocs.io/en/latest/
    * https://python-evdev.readthedocs.io/en/latest/
  - [ ] Design the architecture.
- [ ] Console Client:
  - [ ] Retrieve a list of devices.
  - [ ] Retrieve a list of device attributes and actions.
  - [ ] Retrieve information about an attribute.
  - [ ] Retrieve information about an action.
  - [ ] Read an attribute value.
  - [ ] Write an attribute value.
  - [ ] Run an action.
- [ ] Web Client:
  - [x] Retrieve a list of devices.
  - [x] Retrieve a list of device attributes and actions.
  - [x] Show information about an attribute.
  - [x] Show information about an action.
  - [x] Read an attribute value.
  - [x] Write an attribute value.
  - [ ] Run an action.
