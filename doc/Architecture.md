# Architecture

## Goals

* Modular.
  * Components should be small and easy to replace.
  * All control plane functionality should be provided through HTTP APIs.
* Distributed.
  * No centralized services. Components should be useful on their own.
  * No single points of failure for the overall system. Components should fail independently.
* Soft Real Time
  * Components make no guarantees about response time. They should handle timeouts gracefully.
  * Frequent failures degrade the overall system performance and should be avoided.

## Device Tree

All connected hardware and software is represented using named device objects. A device has some internal state
which is represented using one or more named attributes and can be modified by manipulating these attributes or running
named actions. Attribute and action names exist in a flat namespace and must be unique within each device. They may
contain dots as hints for how they should be logically grouped. Attributes have a value that can usually be read or
written to retrieve or manipulate the state they represent. Actions have input and output values that can be used to
change their behavior or retrieve computed results.

* Device: represents hardware or software connected to the control system
  * Name: human readable name, unique to a node
* Attribute: represents part of the device's internal state
  * Name: human readable name, unique to a device (including action names)
  * Flags: one or more flags that describe the attribute's capabilities
    * `READ`: the attribute value can be read
    * `WRITE`: the attribute value can be written (modified)
  * Schema: defines the attribute value's data type (Avro schema syntax)
* Action: represents a function the device is capable of performing
  * Name: human readable name, unique to a device (including attribute names)
  * Input Schema: defines the input value's data type (Avro schema syntax)
  * Output Schema: defines the output value's data type (Avro schema syntax)

Here's an example using some common household items:

* Device: living-room-light
  * Attribute: brightness
    * Flags: `READ`, `WRITE`
    * Schema: `{'type': 'integer'}`
  * Action: toggle
    * Input Schema: `{'type': 'null'}`
    * Output Schema: `{'type': 'null'}`
* Device: bathroom-scale
  * Attribute: units
    * Flags: `READ`, `WRITE`
    * Schema: `{'type': 'enum', 'symbols': ['lbs', 'kgs']}`
  * Action: measure
    * Input Schema: `{'type': 'null'}`
    * Output Schema: `{'type': 'record', 'fields': [{'name': 'weight', 'type': 'float'}]}`

## Components

The control system is made up of smaller components that work together. Most of the components share common libraries
and schema definitions.

* Control: components that interface with hardware or software
  * Node: A daemon that exposes devices for locally connected hardware.
  * Bridge: A daemon that exposes devices for a remote service.
* Data Storage: TODO
* Automation: TODO
* Monitoring: TODO
