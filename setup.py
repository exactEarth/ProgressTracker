#!/usr/bin/env python
# From https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "1.0.0"


def readme() -> str:
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self) -> None:
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name='progress_tracker',
    version=VERSION,
    description='A utility that wraps an Iterable and regularly prints out progress on the processing of that Iterable',
    long_description=readme(),
    author='exactEarth Ltd.',
    author_email='open-source@exactearth.com',

    packages=['progress_tracker'],
    package_data={
        'progress_tracker': ['py.typed']
    },

    test_suite='tests',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='',
    license='MIT',
    python_requires='>=3.6',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
