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
               '?output=spoiler&method=text&')
        self.assertEqual(CardRequest.base_url, url)

    def test_url_fragment_text(self):
        request = CardRequest({'text': 'first strike'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&text=+[first strike]')
        self.assertEqual(request.url, url)

    def test_url_name(self):
        request = CardRequest({'name': 'sengir,vampire'})
        # this means we'll have to use something like:
        #     name = ','.join(args)
        #     opts['name'] = name
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&name=+[sengir]+[vampire]')
        self.assertEqual(request.url, url)

    def test_url_complex(self):
        options = dict(set='eldrazi', type='instant', color='|r,|w', cmc='=1')
        request = CardRequest(options)
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&color=|[r]|[w]&cmc=+=[1]'
               '&set=+[eldrazi]&type=+[instant]')
        self.assertEqual(request.url, url)
#dict slice
#for a, b in zip(slice, map(x.get, slice)):
#...     y[a] = b

    
