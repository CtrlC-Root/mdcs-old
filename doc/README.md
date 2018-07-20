# Documentation

## Design

* [Goals](Goals.md)
* [Architecture](Architecture.md)

## Components

* Control: components that interface with hardware or software
  * [Node](Node.md): A daemon that exposes devices for local hardware or software.
  * [Bridge](Node.md): A specialized node daemon that exposes devices for a remote service.
* Data Storage: components that record device attribute values
* Automation: components that automate tasks using devices
  * [Reactor](Reactor.md): An event-based automation tool.
* Monitoring: components that monitor devices
  * [Registry](Registry.md): A daemon that keeps track of online nodes and devices.
* Clients:
  * Remote: Mobile remote control application.
