#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs-registry',
    version='0.1',
    description='mdcs node and device registry',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/registry',

    packages=find_packages(),
    install_requires=[
        'mdcs >= 0.1',
        'python-daemon >= 2.0.0'
    ],

    entry_points={
        'console_scripts': [
            'mdcs-registry=mdcs_registry.registry:main'
        ]
    }
)
