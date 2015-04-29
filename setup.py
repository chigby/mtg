#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup
import sys

import mtglib

if sys.version_info < (2, 7):
    install_requires = ['lxml', 'argparse', 'cssselect']
else:
    install_requires = ['lxml', 'cssselect']

setup(
    name = 'mtg',
    packages = ['mtglib'],
    package_dir = {'mtglib': 'mtglib'},
    scripts = ['bin/mtg'],
    install_requires = install_requires,
    version = mtglib.__version__,
    description = 'Console-based access to the Gatherer Magic Card Database.',
    author = mtglib.__author__,
    author_email = 'cameron.higbynaquin@gmail.com',
    license = 'MIT',
    url = 'https://github.com/chigby/mtg',
    keywords = ['mtg', 'magic', 'gatherer'],
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Utilities',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                   'Topic :: Games/Entertainment'],
    long_description = '''\
Console-based access to the Gatherer Magic Card Database
--------------------------------------------------------

Search for Magic cards from the command line.  Limit your results by
card name, color, type, rules text, converted mana cost, power,
toughness, or expansion set.  Rulings and flavor text also available.
Clean interface and output.
'''
)
