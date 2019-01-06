#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs-remote',
    version='0.1',
    description='mdcs remote control',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/remote',

    packages=find_packages(),
    install_requires=[
        'Flask >= 1.0.0',
        'SQLAlchemy >= 1.2.0',
        'alembic >= 0.9.0',
        'shortuuid >= 0.5.0',
        'marshmallow >= 2.15.0',
        'greenstalk >= 0.5.0',
        'lupa >= 1.6'
    ],

    entry_points={
        'console_scripts': [
            'mdcs-remote-worker=mdcs_remote.worker:main'
        ]
    }
)
