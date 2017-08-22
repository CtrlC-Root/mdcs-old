import os.path

import avro.protocol
import pkg_resources

API_PROTOCOL = avro.protocol.Parse(pkg_resources.resource_string('mdcs', os.path.join('tcp', 'api.avpr')))
