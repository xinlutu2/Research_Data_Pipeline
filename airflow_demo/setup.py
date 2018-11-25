#!/usr/bin/env python
import os
from setuptools import setup


def read(fname):
    """ Reads a file; Used everywhere.

    :param fname: The name of a file relative to the root path
    :return: The string contents of the file
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Data Engineer - Ariflow',
    version='1.0',
    description='Data Engineer Airflow Demo',
    long_description=read('README.md'),
    author='Xinlu Tu',
    author_email='xinlutu2@illinois.edu',
    url='https://github.com/xinlutu2',
    packages=['dags'],
    install_requires=read('requirements.txt'),
    setup_requires=read('requirements-setup.txt'),
)
