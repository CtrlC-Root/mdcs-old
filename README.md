# mdcs

The Modular Distributed Control System is a framework and set of components built with the framework for assembling a
soft real-time distributed control system.

## Documentation

There is high-level architecture, framework, and component documentation in the `doc` directory. A good place to start
is the [README.md](doc/README.md). There is also a [project roadmap](ROADMAP.md).

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
* [reactor](pkg/reactor/README.md): event based automation tool
* [remote](pkg/remote/README.md): mobile remote control application

## Quick Start

Make sure you have recent versions of the following software installed:

* VirtualBox
* Vagrant

Provision the Vagrant VMs:

```
$ vagrant up
```
