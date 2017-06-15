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

## Components

* Control
  * Node: TODO
  * Bridge: TODO
* Data Storage
  * Archive: TODO
* Automation
  * TODO: what?
* User Interface
  * TODO: something on the web
  * TODO: voice controlled assistant

TODO: diagram
