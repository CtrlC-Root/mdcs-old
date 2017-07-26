#!/usr/bin/env python

import sys
import json
import argparse
from http import HTTPStatus

import requests


def register_user(args):
    """
    Register a new user on the Hue bridge.
    """

    # contact the bridge
    response = requests.get('http://{0}/description.xml'.format(args.bridge))
    if response.status_code != HTTPStatus.OK:
        print("could not contact the bridge!")
        sys.exit(1)

    # register a new user
    while True:
        # request a new user
        request_data = {'devicetype': '{0}#{1}'.format(args.application, args.device)}
        response = requests.post('http://{0}/api'.format(args.bridge), data=json.dumps(request_data))

        if response.status_code != HTTPStatus.OK:
            print("error contacting bridge: {0}".format(response))
            sys.exit(1)

        response_data = response.json()[0]

        # user was created
        if 'success' in response_data:
            username = response_data['success']['username']
            break

        # retrieve error details
        error_type = response_data['error']['type']
        error_description = response_data['error']['description']

        # check if the link button needs to be pressed
        if error_type == 101:
            input("Press the link button on the bridge and hit any key to continue...")
            continue

        # print the error and give up
        print("error creating new user: {0}".format(error_description))
        sys.exit(1)

    # print username
    print("username: {0}".format(username))


def unregister_user(args):
    """
    Unregister an existing user on the Hue bridge.
    """

    # remove the user
    response = requests.delete('http://{0}/api/{1}/config/whitelist/{1}'.format(args.bridge, args.username))
    if response.status_code != HTTPStatus.OK:
        print("failed to delete user: {0}".format(response))
        sys.exit(1)

    # success
    print("user removed")


def main():
    """
    Run the Hue console utility.
    """

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge', type=str, required=True, help="hue bridge IP address or hostname")

    subparsers = parser.add_subparsers()
    parser_register = subparsers.add_parser('register')
    parser_register.set_defaults(handler=register_user)
    parser_register.add_argument('--application', type=str, default='mdcs', help="application to register")
    parser_register.add_argument('--device', type=str, default='bridge', help="device to register")

    parser_unregister = subparsers.add_parser('unregister')
    parser_unregister.set_defaults(handler=unregister_user)
    parser_unregister.add_argument('--username', type=str, required=True, help="username to unregister")

    args = parser.parse_args()

    # run the subcommand's handler
    args.handler(args)
