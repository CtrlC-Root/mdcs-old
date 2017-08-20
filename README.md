# mdcs

The Modular Distributed Control System is a framework and set of components built with the framework for assembling a soft real-time distributed control system.

## Framework

Reusable libraries for implementing components.

* `libmdcs-python`: common library for Python services and clients

## Components

Standalone components.

* `bridge-hue`: bridge node for Philips Hue lights
* `node`: general node with plugins for hardware
* `mdcs-console`: console client for nodes
* `mdcs-web`: web interface for nodes

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
$ pushd pkg/mdcs-console
$ make reqs
$ popd
```

Start the Hue bridge.

```
$ mdcs-bridge-hue
```

Run the console client.

```
$ mdcsctl
```
