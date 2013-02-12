import unittest

from mtglib.constants import base_url, card_flags

class DescribeConstants(unittest.TestCase):

    def should_have_base_url(self):
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
               '?output=standard&')
        assert base_url == url

    def should_have_card_flags(self):
        assert card_flags == ['text', 'color', 'subtype', 'type', 'set', 'cmc',
                              'power', 'tough', 'rarity', 'name', 'block']