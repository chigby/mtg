import unittest2

from mtglib.gatherer_request import CardRequest

class GathererRequestTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def test_class(self):
        request = CardRequest({'text': 'first strike'})
        self.assertTrue(request)
        self.assertEqual(request.options, {'text': 'first strike'})

    def test_base_url(self):
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
               '?output=spoiler&method=text')
        self.assertEqual(CardRequest.base_url, url)

    def test_url_fragment_name(self):
        request = CardRequest({'text': 'first strike'})
        self.assertEqual(request.url_fragments, ['+[sengir]+[vampire]'])

#dict slice
#for a, b in zip(slice, map(x.get, slice)):
#...     y[a] = b

    
