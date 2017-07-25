#!/usr/bin/env python

import os.path

import avro.schema
import pkg_resources

REQUEST_SCHEMA = avro.schema.Parse(
    pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'request.json')))

RESPONSE_SCHEMA = avro.schema.Parse(
    pkg_resources.resource_string('mdcs', os.path.join('tcp', 'schema', 'response.json')))
