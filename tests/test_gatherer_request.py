import unittest2
import httplib2 
import urllib
from dingus import DingusTestCase

import mtglib.gatherer_request as mod
from mtglib.gatherer_request import CardRequest

PARAMS = {'ctl00$ctl00$MainContent$SearchControls$CardSearchBoxParent'
          '$CardSearchBox':'Search Terms...',
          'ctl00$ctl00$MainContent$SearchControls$SearchCardName':'on', 
          'ctl00$ctl00$MainContent$SubContent$AutoComplete':
              'EnableAutoComplete',
          'ctl00$ctl00$MainContent$SubContent$CardLinkAction':'SameWindow',
          'ctl00$ctl00$MainContent$SubContent$GroupBy':'None',
          'ctl00$ctl00$MainContent$SubContent$HintText':'EnableHintText',
          'ctl00$ctl00$MainContent$SubContent$ResultsPerPage':'100',
          'ctl00$ctl00$MainContent$SubContent$ResultsView':'SpoilerView',
          'ctl00$ctl00$MainContent$SubContent$Save':'Save',
          'ctl00$ctl00$MainContent$SubContent$SelectingCard':'NavigatesToCard',
          'ctl00$ctl00$MainContent$SubContent$cardRulings':'on',
          'ctl00$ctl00$MainContent$SubContent$languagePreferenceSelector'
          '$LanguageGroup':'en-US',
          '__EVENTVALIDATION': '/wEWKwK75+DFAQLevrmxAQL998wLAszrof8GAqS1kKUNAs'
          'eQ9aYKArHA+agHAtuiyI8KAuW4lukEAtL65/MEAt2f/Z4CAvDTh/UIAriI5sIBAtvjr'
          'rcEAvq+4Y0KApT4iwMC5OKZxggCq/jh3QUC76eDBALT5/SDBQKV+emYAwKGm+HlBALq'
          'yuj+BALZvOTwDwKMgbNSAuDnzLIOAp70x7sEAvLXn6QKArCK6dYHAuPs49oPApCO0FQ'
          'CwdvMhgsCj/XJ2QYC5P/93QQCnf7J5AkC5fat2woCl/rZiQgCgviplAIC7/a91ggC8P'
          'mhkQEC/PSBnQEC2f/drAMC+JCPwAlYnqtQQxfeLziePLQKzhRQ535I5Q==',
          '__VIEWSTATE': '/wEPDwUKMTA0MjI1NTI4M2QYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFiMFNWN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmROYW1lBTZjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTZWFyY2hDb250cm9scyRTZWFyY2hDYXJkVHlwZXMFNWN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmRUZXh0BS9jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFN0YW5kYXJkVmlldwUuY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDb21wYWN0VmlldwUwY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDaGVja2xpc3RWaWV3BS5jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFNwb2lsZXJWaWV3BS9jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JEltYWdlT25Ib3ZlcgU1Y3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRFbmFibGVBdXRvQ29tcGxldGUFNmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkRGlzYWJsZUF1dG9Db21wbGV0ZQVIY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRFbmFibGVBdXRvQ29tcGxldGVFdmVuSWZOYW1lVW5jaGVja2VkBTFjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JEVuYWJsZUhpbnRUZXh0BTJjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JERpc2FibGVIaW50VGV4dAU/Y3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDbG9zZURldGFpbHNPbkNhcmRJbWFnZUNsaWNrBUVjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFJlZGlyZWN0VG9EZXRhaWxzUGFnZVdpdGhPbmVSZXN1bHQFMmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkZmVlZGJhY2tNZXNzYWdlBTljdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGZyb250UGFnZVNlYXJjaE9wdGlvbnMFOmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkb3RoZXJQYWdlc1NlYXJjaE9wdGlvbnMFN2N0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkc2VhcmNoUmVzdWx0c09wdGlvbnMFLmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkY2FyZFJ1bGluZ3MFMmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkcG9wdWxhckNvbW1lbnRzBTFjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JHJlY2VudENvbW1lbnRzBT1jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGRpc2N1c3Npb25QcmludGluZ3NXYXJuaW5nBS5jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGNvbW1lbnRGb3JtBTVjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGZvcm1hdE5vdGlmaWNhdGlvbgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzMwVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAyOAVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMjA1MgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzNgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0MQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0OQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMzA4MgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0MAVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzMQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMjA3MKbhIzf0+FFOPMtewwL7KqW90P6P'
          }

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

    def should_have_settings_url(self):
        settings_url = 'http://gatherer.wizards.com/Pages/Settings.aspx'
        assert CardRequest.settings_url == settings_url

    def should_have_settings_headers(self):
        header =  {'Content-type': 'application/x-www-form-urlencoded'}
        assert CardRequest.settings_header == header

    def should_have_settings_params(self):
        assert CardRequest.params == PARAMS

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

class WhenSendingRequest(DingusTestCase(CardRequest, exclude=['urllib', 'get_url_fragments', 'get_modifiers'])):

    def setup(self):
        super(WhenSendingRequest, self).setup()
        self.request = CardRequest({'text': '"first strike"'})
        self.http = mod.httplib2.Http()
        self.http.request.return_value = ({'set-cookie':'cookiedata'}, 'foo')
        
    def should_send_settings_request(self):
        self.request.send()
        http_args = self.http.calls('request')[0].args
        http_kwargs = self.http.calls('request')[0].kwargs
        assert http_args[0] == self.request.settings_url
        assert http_args[1] == 'POST'
        assert http_kwargs['headers'] == self.request.settings_header
        assert http_kwargs['body'] == urllib.urlencode(self.request.params)

    def should_send_card_request(self):
        self.request.send()
        http_args = self.http.calls('request')[1].args
        http_kwargs = self.http.calls('request')[1].kwargs
        assert http_args[0] == self.request.url
        assert http_args[1] == 'GET'
        assert http_kwargs['headers'] == {'Cookie': 'cookiedata'}
