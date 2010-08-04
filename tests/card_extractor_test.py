from dingus import DingusTestCase, Dingus, returner
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

    def setup(self):
        super(WhenExtractingCards, self).setup()
        self.extractor = CardExtractor('<html></html>')
        self.table = mod.BeautifulSoup.BeautifulSoup().table
        self.table.findAll.return_value = [Dingus()] * 13 
        for tag in self.table.findAll():
            tag.contents = [Dingus()] * 3
            for contents in tag.contents:
                contents.string = u'\r\n string\r\n'
        self.extracted = self.extractor.extract()

    def should_be_false_if_empty(self):
        assert not CardExtractor('').extract()
        
    def should_parse_html(self):
        assert mod.BeautifulSoup.calls('BeautifulSoup', '<html></html>').once()

    def should_raise_exception_if_bad_format(self):
        mod.BeautifulSoup.BeautifulSoup().table = False
        assert_raises(Exception, CardExtractor('<html></html>').extract)
       
    def should_replace_br_tags_with_pipes(self):
        soup = mod.BeautifulSoup.BeautifulSoup()
        for tag in soup.findAll():
            assert tag.calls('replaceWith', '||')
        assert soup.calls('findAll', 'br').once()
        
    def should_find_all_td_tags(self):
        assert self.table.calls('findAll', 'td').once()

    def should_extract_and_group_text_from_tags(self):
        fragment = '\r\n string\r\n'
        # assert self.extracted == \
        #     [u'\r\n string\r\n\r\n string\r\n\r\n string\r\n'] * 13
        assert self.extracted == [((fragment*3,)*2,)*6]
