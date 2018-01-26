#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs-node',
    version='0.1',
    description='mdcs node',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/node-python',

    packages=find_packages(),
    install_requires=[
        'mdcs >= 0.1',
        'psutil >= 5.2.0',
        'python-daemon >= 2.0.0'
    ],

    entry_points={
        'console_scripts': [
            'mdcs-node=mdcs_node.node:main'
        ]
    }
)
