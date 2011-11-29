import unittest2
import httplib2
import urllib
from nose.tools import assert_raises
from dingus import DingusTestCase, exception_raiser

import mtglib.gatherer_request as mod
from mtglib.gatherer_request import SearchRequest, CardRequest

class WhenInstantiatingSearchRequest(unittest2.TestCase):

    def setUp(self):
        self.request = SearchRequest({'text': 'first strike'})

    def should_be_instance_of_card_request(self):
        assert isinstance(self.request, SearchRequest)

    def should_store_options(self):
        assert self.request.options == {'text': 'first strike'}


class WhenGettingUrl(unittest2.TestCase):

    def should_be_idempotent_for_color(self):
        request = SearchRequest({'color': 'w,b'})
        assert request.url == request.url

    def should_be_idempotent_for_text(self):
        request = SearchRequest({'text': 'destroy all creatures'})
        assert request.url == request.url

    def should_group_text_in_brackets(self):
        request = SearchRequest({'text': 'trample'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&text=+[trample]')
        assert request.url == url

    def should_assume_exact_quote_if_spaces(self):
        request = SearchRequest({'text': 'first strike'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&text=+["first strike"]')
        assert request.url == url

    def should_parse_logical_or(self):
        request = SearchRequest({'text': '|first,|strike'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&text=|[first]|[strike]')
        assert request.url == url

    def should_parse_logical_or_for_sets(self):
        request = SearchRequest({'set': '|worldwake,|zendikar'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&set=|[worldwake]|[zendikar]')
        assert request.url == url

    def should_assume_logical_or_for_sets(self):
        request = SearchRequest({'set': 'worldwake,zendikar'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&set=|[worldwake]|[zendikar]')
        assert request.url == url

    def should_parse_sharp_comparison_operators(self):
        request = SearchRequest({'cmc': '=5', 'power': '<4', 'tough':'>3'})
        assert 'cmc=+=[5]' in request.url
        assert 'power=+<[4]' in request.url
        assert 'tough=+>[3]' in request.url

    def should_use_equality_as_default_comparison_operators(self):
        request = SearchRequest({'cmc': '5', 'power': '4', 'tough':'3'})
        assert 'cmc=+=[5]' in request.url
        assert 'power=+=[4]' in request.url
        assert 'tough=+=[3]' in request.url

    def should_parse_comparison_operators(self):
        request = SearchRequest({'power': '<=4', 'tough':'>=3'})
        assert 'power=+<=[4]' in request.url
        assert 'tough=+>=[3]' in request.url

    def should_separate_name_words(self):
        request = SearchRequest({'name': 'sengir,vampire'})
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&name=+[sengir]+[vampire]')
        self.assertEqual(request.url, url)

    def should_allow_color_exclusion_with_logical_or(self):
        request = SearchRequest({'color': 'w,u'}, exclude_other_colors=True)
        assert '&color=+@([w]|[u])' in request.url

    def should_parse_not_operator(self):
        request = SearchRequest({'text': '!graveyard'})
        assert 'text=+![graveyard]' in request.url

    def should_assume_and_when_color_has_no_comma(self):
        request = SearchRequest({'color': 'wu'})
        assert 'color=+[w]+[u]' in request.url

    def should_assume_or_when_comma_separated_color(self):
        request = SearchRequest({'color': 'w,u'})
        assert 'color=|[w]|[u]' in request.url

    def should_correctly_handle_not(self):
        request = SearchRequest({'color': '!b'})
        print request.url
        assert 'color=+![b]' in request.url

    def should_correctly_handle_both_not_and_or(self):
        request = SearchRequest({'color': '!b,r'})
        print request.url
        assert 'color=+![b]|[r]' in request.url

    def should_send_type(self):
        options = dict(type='land')
        request = SearchRequest(options)
        assert 'type=+[land]' in request.url

    def should_recognize_creature_type_as_subtype(self):
        options = dict(type='dryad')
        request = SearchRequest(options)
        assert 'subtype=+[dryad]' in request.url
        assert '&type=+[dryad]' not in request.url

    def should_separate_type_and_subtypes(self):
        options = dict(type='land,dryad')
        request = SearchRequest(options)
        assert 'subtype=+[dryad]' in request.url
        assert '&type=+[land]' in request.url

    def should_separate_type_and_subtypes_artifacts(self):
        options = dict(type='artifact,bird')
        request = SearchRequest(options)
        assert 'subtype=+[bird]' in request.url
        assert '&type=+[artifact]' in request.url

    def should_ignore_case_on_types(self):
        options = dict(type='ARTIFACT,Bird')
        request = SearchRequest(options)
        assert 'subtype=+[bird]' in request.url
        assert '&type=+[artifact]' in request.url

    def should_separate_many_types(self):
        options = dict(type='creature,land,dryad,forest')
        request = SearchRequest(options)
        assert 'subtype=+[dryad]+[forest]' in request.url
        assert '&type=+[creature]+[land]' in request.url

    def should_separate_many_types_with_not_modifier(self):
        options = dict(type='legendary,artifact,!equipment,!creature')
        request = SearchRequest(options)
        assert 'subtype=+![equipment]' in request.url
        assert '&type=+[legendary]+[artifact]+![creature]' in request.url

    def should_separate_many_types_with_or_modifier(self):
        options = dict(type='eldrazi,|instant,|creature')
        request = SearchRequest(options)
        assert 'subtype=+[eldrazi]' in request.url
        assert '&type=|[instant]|[creature]' in request.url


class WhenMakingSpecialRequest(unittest2.TestCase):

    def setUp(self):
        self.request = SearchRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)

    def should_have_special(self):
        assert self.request.special == True

    def should_have_special_fragment(self):
        assert self.request.special_fragment == '&special=true'

    def should_include_special_option_in_url(self):
        request = SearchRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)
        url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx?'
               'output=standard&name=+[only]+[blood]+[ends]+[your]'
               '+[nightmares]&special=true')
        self.assertEqual(request.url, url)


class DescribeCardRequest(DingusTestCase(CardRequest)):

    def should_accept_url(self):
        request = CardRequest('http://www.com')
        assert request.url == 'http://www.com'

    def should_open_url(self):
        request = CardRequest('http://www.com')
        request.send()
        assert mod.urllib2.calls('urlopen', 'http://www.com').once()

    def should_read_from_url(self):
        request = CardRequest('http://www.com')
        request.send()
        assert mod.urllib2.urlopen().calls('read')

    def should_fix_relative_urls(self):
        request = CardRequest('../Card/Details.aspx?multiverseid=212635')
        fixed_url = ('http://gatherer.wizards.com/Pages/Card/Details.aspx'
                     '?multiverseid=212635')
        request.send()
        assert mod.urllib2.calls('urlopen', fixed_url)
