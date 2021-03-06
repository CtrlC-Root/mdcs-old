#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs-bridge-hue',
    version='0.1',
    description='mdcs bridge node for philips hue lights',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/bridge-hue',

    packages=find_packages(),
    install_requires=[
        'mdcs >= 0.1',
        'mdcs-node >= 0.1',
        'requests >= 2.18.0'
    ],

    entry_points={
        'console_scripts': [
            'mdcs-bridge-hue=mdcs_bridge_hue.bridge:main',
            'mdcs-hue=mdcs_bridge_hue.utility:main'
        ]
    }
)
