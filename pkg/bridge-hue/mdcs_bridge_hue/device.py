#!/usr/bin/env python

from http import HTTPStatus

import json
import requests

from mdcs.generic import Device, StoredAttribute, DelegatedAttribute, Action
from mdcs.generic import AttributeFlags as AF


class HueDevice(Device):
    """
    A Philips Hue light connected to a bridge.
    """

    def __init__(self, bridge, user, light):
        super().__init__("light-{0}".format(light))

        # store configuration settings
        self.config = {'bridge': bridge, 'user': user, 'light': light}

        # create attributes and actions
        self.add_attribute(DelegatedAttribute(
            'name',
            AF.READ,
            {'type': 'string'},
            self.read_name,
            self.write_name))

        self.add_attribute(DelegatedAttribute(
            'brightness',
            AF.READ | AF.WRITE,
            {'type': 'int'},
            self.read_brightness,
            self.write_brightness))

    @property
    def hue_url(self):
        return 'http://{bridge}/api/{user}/lights/{light}'.format(**self.config)

    def get_data(self):
        response = requests.get(self.hue_url)
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error requesting data from bridge: {0}".format(response))

        return response.json()

    def set_data(self, state):
        response = requests.put(self.hue_url, data=json.dumps(state))
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError("error updating data on bridge: {0}".format(response))

        # XXX: validate return value?

    def set_state(self, state):
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

    def read_brightness(self):
        data = self.get_data()
        return data['state']['bri']

    def write_brightness(self, value):
        if value < 1 or value > 254:
            raise RuntimeError("brightness must be within (1, 254) inclusive")

        self.set_state({'bri': value})
