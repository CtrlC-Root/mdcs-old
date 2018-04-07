import os.path

import avro.schema
import pkg_resources

EVENT_SCHEMA = avro.schema.Parse(
    pkg_resources.resource_string('mdcs', os.path.join('discovery', 'multicast', 'event.avsc')))
