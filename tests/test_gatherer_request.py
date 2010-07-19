import unittest2

from mtglib.gatherer_request import CardRequest

class WhenInstantiatingCardRequest(unittest2.TestCase):

    def setUp(self):
        self.request = CardRequest({'text': 'first strike'})
        
    def should_be_instance_of_card_request(self):
        assert isinstance(self.request, CardRequest)
        
    def should_store_options(self):
        assert self.request.options == {'text': 'first strike'}

    def should_have_base_url(self):
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
               '?output=spoiler&method=text&')
        self.assertEqual(CardRequest.base_url, url)


class WhenGettingUrl(unittest2.TestCase):

    def should_group_text_in_brackets(self):
        request = CardRequest({'text': 'first strike'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&text=+[first strike]')
        assert request.url == url

    def should_preserve_exact_quotes(self):
        request = CardRequest({'text': '"first strike"'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&text=+["first strike"]')
        assert request.url == url

    def should_parse_logical_or(self):
        request = CardRequest({'text': '|first,|strike'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&text=|[first]|[strike]')
        assert request.url == url

    def should_parse_sharp_comparison_operators(self):
        request = CardRequest({'cmc': '=5', 'power': '<4', 'tough':'>3'})
        assert 'cmc=+=[5]' in request.url
        assert 'power=+<[4]' in request.url
        assert 'tough=+>[3]' in request.url

    def should_parse_comparison_operators(self):
        request = CardRequest({'power': '<=4', 'tough':'>=3'})
        assert 'power=+<=[4]' in request.url
        assert 'tough=+>=[3]' in request.url
        
    def should_separate_name_words(self):
        request = CardRequest({'name': 'sengir,vampire'})
        # this means we'll have to use something like:
        #     name = ','.join(args)
        #     opts['name'] = name
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&name=+[sengir]+[vampire]')
        self.assertEqual(request.url, url)

    def should_parse_not_operator(self):
        request = CardRequest({'text': '!graveyard'})
        assert 'text=+![graveyard]' in request.url
        
    def should_combine_multiple_terms(self):
        options = dict(set='eldrazi', type='instant', color='|r,|w', cmc='=1')
        request = CardRequest(options)
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&color=|[r]|[w]&cmc=+=[1]'
               '&set=+[eldrazi]&type=+[instant]')
        self.assertEqual(request.url, url)
#dict slice
#for a, b in zip(slice, map(x.get, slice)):
#...     y[a] = b

    
class WhenMakingSpecialRequest(unittest2.TestCase):

    def setUp(self):
        self.request = CardRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)
        
    def should_have_special(self):
        assert self.request.special == True

    def should_have_special_fragment(self):
        assert self.request.special_fragment == '&special=true'

    def should_include_special_option_in_url(self):
        request = CardRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=spoiler&method=text&name=+[only]+[blood]+[ends]+[your]'
               '+[nightmares]&special=true')
        self.assertEqual(request.url, url)
