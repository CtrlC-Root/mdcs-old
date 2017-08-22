#!/usr/bin/env python

from http import HTTPStatus

import json
import requests

from mdcs.generic import Device, AttributeFlags, DelegatedAttribute


class GroupDevice(Device):
    """
    A Philips Hue light group on a bridge.
    """

    def __init__(self, name, bridge, user, group):
        super().__init__(name, {'bridge': bridge, 'user': user, 'group': group})

        # create attributes and actions
        self.add_attribute(DelegatedAttribute(
            'name',
            AttributeFlags.READ | AttributeFlags.WRITE,
            'string',
            self.read_name,
            self.write_name))

        self.add_attribute(DelegatedAttribute(
            'type',
            AttributeFlags.READ,
            {
                'name': 'type',
                'type': 'enum',
                'symbols': [
                    'Luminaire',
                    'LightSource',
                    'LightGroup',
                    'Room'
                ]
            },
            self.read_type,
            None))

        self.add_attribute(DelegatedAttribute(
            'class',
            AttributeFlags.READ,
            {
                'name': 'class',
                'type': 'enum',
                'symbols': [
                    'Living room',
                    'Kitchen',
                    'Dining',
                    'Bedroom',
                    'Kids bedroom',
                    'Bathroom',
                    'Nursery',
                    'Recreation',
                    'Office',
                    'Gym',
                    'Hallway',
                    'Toilet',
                    'Front door',
                    'Garage',
                    'Terrace',
                    'Garden',
                    'Driveway',
                    'Carport',
                    'Other'
                ]
            },
            self.read_class,
            None))

        self.add_attribute(DelegatedAttribute(
            'on',
            AttributeFlags.READ | AttributeFlags.WRITE,
            'boolean',
            self.read_on,
            self.write_on))

        self.add_attribute(DelegatedAttribute(
            'brightness',
            AttributeFlags.READ | AttributeFlags.WRITE,
            'int',
            self.read_brightness,
            self.write_brightness))

    @property
    def hue_url(self):
        return 'http://{bridge}/api/{user}/groups/{group}'.format(**self.config)

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

    def get_action(self):
        """
        Get the state of the light.
        """

        # there is no way to directly get the light action data
        data = self.get_data()
        return data['action']

    def set_action(self, state):
        """
        Set the state of the light.
        """

        response = requests.put("{0}/action".format(self.hue_url), data=json.dumps(state))
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

    def read_type(self):
        data = self.get_data()
        return data['type']

    def read_class(self):
        data = self.get_data()
        data.setdefault('class', 'Other') # TODO: group 0 doesn't provide a class???
        return data['class']

    def read_on(self):
        state = self.get_action()
        return state['on']

    def write_on(self, value):
        self.set_action({'on': value})

    def read_brightness(self):
        state = self.get_action()
        return state['bri']

    def write_brightness(self, value):
        if value < 1 or value > 254:
            raise RuntimeError("brightness must be within (1, 254) inclusive")

        self.set_action({'bri': value})
