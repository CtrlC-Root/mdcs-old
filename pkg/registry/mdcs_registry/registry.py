#!/usr/bin/env python

import argparse

from mdcs.discovery import MulticastDiscoveryConfig
from mdcs.logging import LoggingConfig

from .config import RegistryDaemonConfig
from .daemon import RegistryDaemon


def main():
    """
    Run the registry daemon.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help="bind to IP address or hostname")
    parser.add_argument('--http-port', type=int, default=5520, help="HTTP API port")
    MulticastDiscoveryConfig.define_args(parser)
    LoggingConfig.define_args(parser)

    parser.add_argument('--daemon', action='store_true', help="run as daemon in background")

    args = parser.parse_args()

    # configure logging
    logging_config = LoggingConfig.from_args(args)
    logging_config.apply()

    # create the registry daemon
    config = RegistryDaemonConfig(
        public_host=args.host,
        bind_host=args.host,
        http_port=args.http_port,
        logging=logging_config,
        discovery=MulticastDiscoveryConfig.from_args(args),
        background=args.daemon)

    daemon = RegistryDaemon(config=config)

    # run the daemon
    daemon.run()
