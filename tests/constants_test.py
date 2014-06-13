import unittest

from nose.tools import eq_

from mtglib.constants import base_url

class DescribeConstants(unittest.TestCase):

    def should_have_base_url(self):
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
               '?action=advanced&')
        eq_(base_url, url)
