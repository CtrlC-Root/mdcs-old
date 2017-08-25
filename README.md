# mdcs

The Modular Distributed Control System is a framework and set of components built with the framework for assembling a soft real-time distributed control system.

## Framework

Reusable libraries for implementing components.

* `libmdcs-python`: common library for Python services and clients

## Components

Standalone components.

* `node`: general purpose node with plugin system
* `node-console`: console client for nodes
* `node-web`: web interface for nodes
* `bridge-hue`: bridge node for Philips Hue lights

## Quick Start

Create a virtualenv and install the desired packages and their requirements.

```
$ virtualenv --python=$(which python3) mdcs
$ pushd pkg/libmdcs-python
$ make reqs
$ popd
$ pushd pkg/bridge-hue
$ make reqs
$ popd
$ pushd pkg/node-console
$ make reqs
$ popd
```

Start the Hue bridge.

```
$ mdcs-bridge-hue --bridge 192.168.X.X --user 'bridge_api_username_here'
```

Retrieve a list of devices, retrieve device attributes, read an attribute value, and write an attribute value.

```
$ mdcsctl list-devices
$ mdcsctl show-device hue-AABBCCDDEEFF-group-0
$ mdcsctl read hue-AABBCCDDEEFF-group-0 name
$ mdcsctl write hue-AABBCCDDEEFF-group-0 on true
```
