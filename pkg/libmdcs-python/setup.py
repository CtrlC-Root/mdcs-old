#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mdcs',
    version='0.1',
    description='mdcs common library',
    author='Alexandru Barbur',
    author_email='root.ctrlc@gmail.com',
    url='https://github.com/mdcs/pkg/libmdcs-python',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'avro-python3 >= 1.8.0',
        'python-daemon >= 2.0.0'
    ]
)
