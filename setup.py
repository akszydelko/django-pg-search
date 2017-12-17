#!/usr/bin/env python
from setuptools import setup, find_packages

from pgsearch import __version__

long_description = """
    Django app for making PostgreSQL full text search queries
    
    See more on: https://github.com/akszydelko/django-pg-search
    
    Copyright (c) 2017, Arkadiusz Szydełko All rights reserved.

    Licensed under BSD 3-Clause License
"""

setup(
    name='django-pg-search',
    version=__version__,
    description='Django app for making PostgreSQL full text search queries',
    long_description=long_description,
    url='https://github.com/akszydelko/django-pg-search',
    author='Arkadiusz Szydelko',
    author_email='akszydelko@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    keywords='django postgresql full text search',
    packages=find_packages(),
    install_requires=[
        'django>=1.8',
        'psycopg2>=2.6.1'
    ],
)
