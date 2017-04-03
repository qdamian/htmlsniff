#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'attrs==16.3.0',
    'six==1.10.0',
    'contextlib2==0.5.4',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='htmlvis',
    version='0.1.0',
    description="HTML visualization for Python",
    long_description=readme + '\n\n' + history,
    author="Damian Quiroga",
    author_email='qdamian@gmail.com',
    url='https://github.com/qdamian/htmlvis',
    packages=[
        'htmlvis',
    ],
    package_dir={'htmlvis': 'htmlvis'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='htmlvis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements)
