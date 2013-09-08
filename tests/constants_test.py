import unittest

from nose.tools import eq_

from mtglib.constants import base_url, card_flags

class DescribeConstants(unittest.TestCase):

    def should_have_base_url(self):
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
               '?output=standard&action=advanced&')
        eq_(base_url, url)

    def should_have_card_flags(self):
        eq_(card_flags, ['text', 'color', 'subtype', 'type', 'set', 'cmc',
                         'power', 'tough', 'rarity', 'name', 'block'])