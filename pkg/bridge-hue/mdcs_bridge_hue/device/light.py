#!/usr/bin/env python

from http import HTTPStatus

import json
import requests

from mdcs.generic import Device, AttributeFlags, DelegatedAttribute


class LightDevice(Device):
    """
    A Philips Hue light connected to a bridge.
    """

    def __init__(self, name, bridge, user, light):
        super().__init__(name, {'bridge': bridge, 'user': user, 'light': light})

        # create attributes and actions
        self.add_attribute(DelegatedAttribute(
            'name',
            AttributeFlags.READ | AttributeFlags.WRITE,
            {'type': 'string'},
            self.read_name,
            self.write_name))

        self.add_attribute(DelegatedAttribute(
            'manufacturer',
            AttributeFlags.READ,
            {'type': 'string'},
            self.read_manufacturer,
            None))

        self.add_attribute(DelegatedAttribute(
            'model',
            AttributeFlags.READ,
            {'type': 'string'},
            self.read_model,
            None))

        self.add_attribute(DelegatedAttribute(
            'firmware',
            AttributeFlags.READ,
            {'type': 'string'},
            self.read_firmware,
            None))

        self.add_attribute(DelegatedAttribute(
            'reachable',
            AttributeFlags.READ,
            {'type': 'boolean'},
            self.read_reachable,
            None))

        self.add_attribute(DelegatedAttribute(
            'on',
            AttributeFlags.READ | AttributeFlags.WRITE,
            {'type': 'boolean'},
            self.read_on,
            self.write_on))

        self.add_attribute(DelegatedAttribute(
            'brightness',
            AttributeFlags.READ | AttributeFlags.WRITE,
            {'type': 'int'},
            self.read_brightness,
            self.write_brightness))

    @property
    def hue_url(self):
        return 'http://{bridge}/api/{user}/lights/{light}'.format(**self.config)

    def get_data(self):
        """
        Get all data for the light.
        """

        response = requests.get(self.hue_url)
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error requesting data from bridge: {0}".format(response))

        return response.json()

    def set_data(self, state):
        """
        Set configuration settings for the light.
        """

        response = requests.put(self.hue_url, data=json.dumps(state))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error updating data on bridge: {0}".format(response))

        # XXX: validate return value?

    def get_state(self):
        """
        Get the state of the light.
        """

        # there is no way to directly get the light state
        data = self.get_data()
        return data['state']

    def set_state(self, state):
        """
        Set the state of the light.
        """

        response = requests.put("{0}/state".format(self.hue_url), data=json.dumps(state))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error updating data on bridge: {0}".format(response))

        # XXX: validate return value?

    def read_name(self):
        data = self.get_data()
        return data['name']

    def write_name(self, value):
        if len(value) == 0 or len(value) > 32:
            raise RuntimeError("name must be between 1 and 32 characters long")

        self.set_data({'name': value})

    def read_manufacturer(self):
        data = self.get_data()
        return data['manufacturername']

    def read_model(self):
        data = self.get_data()
        return data['modelid']

    def read_firmware(self):
        data = self.get_data()
        return data['swversion']

    def read_reachable(self):
        state = self.get_state()
        return state['reachable']

    def read_on(self):
        state = self.get_state()
        return state['on']

    def write_on(self, value):
        self.set_state({'on': value})

    def read_brightness(self):
        state = self.get_state()
        return state['bri']

    def write_brightness(self, value):
        if value < 1 or value > 254:
            raise RuntimeError("brightness must be within (1, 254) inclusive")

        self.set_state({'bri': value})
