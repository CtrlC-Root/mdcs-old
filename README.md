# mdcs

The Modular Distributed Control System is a framework and set of components built with the framework for assembling a
soft real-time distributed control system.

## Documentation

There is high-level architecture, framework, and component documentation in the `doc` directory. A good place to start
is the [architecture documentation](doc/Architecture.md). There is also a [project roadmap](ROADMAP.md) that shows
what functionality has been already implemented and what still needs to be done.

## Framework

Reusable libraries for implementing components.

* [libmdcs-python](pkg/libmdcs-python/README.md): common library for Python services and clients

## Components

Standalone components.

* [node](pkg/node/README.md): general purpose node with plugin system
* [node-console](pkg/node-console/README.md): console client for nodes
* [node-web](pkg/node-web/README.md): web interface for nodes
* [bridge-hue](pkg/bridge-hue/README.md): bridge node for Philips Hue lights
* [registry](pkg/registry/README.md): node and device registry

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
