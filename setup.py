#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.0.1'

readme = open('README.rst').read()


setup(
    name='django-raptor',
    version=version,
    description="""A tool to import data from CSV files into your database""",
    long_description=readme,
    author='Martín Gaitán',
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/django-raptor',
    packages=[
        'raptor',
    ],
    include_package_data=True,
    install_requires=['unicodecsv',
    ],
    license="BSD",
    zip_safe=False,
    keywords=['django-raptor', 'adaptor', 'csv'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)