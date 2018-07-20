# registry

A node and device registry. Listens to network traffic and keeps track of active nodes and devices. Exposes an HTTP API
that can be used to locate node connection information or which node a device is connected to.

## Roadmap

- [ ] Node and device TTLs. Mark them OFFLINE after a while.
- HTTP API:
  - [ ] Check if the registry is healthy (HAProxy or ELB compatible).
