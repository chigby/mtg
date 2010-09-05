#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(
    name = 'mtg',
    packages = ['mtglib'],
    scripts = ['bin/mtg.py'],
    version = '0.0.1',
    description = 'Console-based access to the Gatherer Magic Card Database.',
    author = 'Cameron Higby-Naquin',
    author_email = 'cameron.higbynaquin@gmail.com',
    url = 'http://bitbucket.org/procyon/mtg/',
    keywords = ['mtg', 'magic', 'gatherer'],
    classifiers = [],
    long_description = ''
)
