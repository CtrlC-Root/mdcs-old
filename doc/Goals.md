# Goals

## Design

* Modular
  * Components should be small and easy to replace.
  * All control plane functionality should be provided through HTTP APIs.
* Distributed
  * No centralized services. Components should be useful on their own.
  * No inherent single points of failure for the overall system. Components should fail independently.
* Soft Real Time
  * Components make no guarantees about response time. They should handle timeouts gracefully.
  * Frequent timeouts or failures degrade the overall usefulness of the system and should be avoided.

## Implementation

The default component implementations are considered reference implementations.

* Correctness
* Minimal Dependencies
  * TODO: avoid external libraries, stick to OS primitives
  * TODO: avoid external services
* TODO: easy to understand for beginners
  * TODO: simplicity over performance
