#!/usr/bin/env python
from setuptools import setup

setup(
    name='progress_tracker',
    version='1.0.0',
    description='A utility that wraps an Iterable and regularly prints out progress on the processing of that Iterable',
    long_description="A utility that wraps an Iterable and regularly prints out progress on the processing of that Iterable",
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='',
    license='MIT'
)
