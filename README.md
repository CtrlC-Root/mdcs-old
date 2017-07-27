# mdcs

The Modular Distributed Control System is a framework and set of components built with the framework for assembling a soft real-time distributed control system.

## Framework

TODO

## Components

TODO

* `bridge-hue`: bridge node for Philips Hue lights

## Quick Start

Create a virtualenv and install packages and their requirements.

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
