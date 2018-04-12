#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='node-console',
    version='0.1',
    description='mdcs node console client',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/node-console',

    packages=find_packages(),
    install_requires=[
        'mdcs >= 0.1'
    ],

    entry_points={
        'console_scripts': [
            'mdcs-nodectl=mdcs_node_console.ctl:main'
        ]
    }
)
