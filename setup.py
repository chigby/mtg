#!/usr/bin/env python

from distutils.core import setup
#from setuptools import setup
import mtglib

setup(
    name = 'mtg',
    packages = ['mtglib'],
    package_dir = {'mtglib': 'mtglib'},
    scripts = ['bin/mtg.py'],
    version = mtglib.__version__,
    description = 'Console-based access to the Gatherer Magic Card Database.',
    author = mtglib.__author__,
    author_email = 'cameron.higbynaquin@gmail.com',
    url = 'http://bitbucket.org/procyon/mtg/',
    keywords = ['mtg', 'magic', 'gatherer'],
    classifiers = [],
    long_description = ''
)
