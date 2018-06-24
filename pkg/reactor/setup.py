#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs-reactor',
    version='0.1',
    description='mdcs event based automation tool',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/reactor',

    packages=find_packages(),
    install_requires=[
        'Flask >= 1.0.0',
        'SQLAlchemy >= 1.2.0',
        'alembic >= 0.9.0',
        'shortuuid >= 0.5.0',
        'marshmallow >= 2.15.0'
    ],
)
