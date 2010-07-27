from dingus import DingusTestCase
from nose.tools import assert_raises

import mtglib.card_extractor as mod
from mtglib.card_extractor import CardExtractor

class WhenInstantiatingCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_html(self):
        assert hasattr(self.extractor, 'html')


class WhenExtractingCards(DingusTestCase(CardExtractor)):

    def should_be_false_if_empty(self):
        assert not CardExtractor('').extract()
        
    def should_parse_html(self):
        CardExtractor('<html></html>').extract()
        assert mod.BeautifulSoup.calls('BeautifulSoup', '<html></html>').once()

    def should_raise_exception_if_bad_format(self):
        soup = mod.BeautifulSoup.BeautifulSoup()
        soup.table = False
        assert_raises(Exception, CardExtractor('<html></html>').extract)
       
    def should_replace_br_tags_with_pipes(self):
        soup = mod.BeautifulSoup.BeautifulSoup()
        CardExtractor('<html></html>').extract()
        soup = mod.BeautifulSoup.BeautifulSoup()
        for tag in soup.findAll():
            assert tag.calls('replaceWith', '||')
        assert soup.calls('findAll', 'br').once()
        
        
        
