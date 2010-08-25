import re

from dingus import DingusTestCase, Dingus, returner
from nose.tools import assert_raises

import mtglib.card_extractor as mod
from mtglib.card_extractor import CardExtractor, RulingExtractor

class WhenInstantiatingCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_html(self):
        assert hasattr(self.extractor, 'html')

    def should_recognize_fields_per_card(self):
        assert self.extractor.fields_per_card == 6

class WhenExtractingCardsWithBlankLines(DingusTestCase(CardExtractor)):
    
    def setup(self):
        super(WhenExtractingCardsWithBlankLines, self).setup()
        self.extractor = CardExtractor('<html></html>')
        self.table = mod.BeautifulSoup.BeautifulSoup().table
        self.table.findAll.return_value = [Dingus()] * 13
        all_tags = []
        for i in range(26):
            tag = Dingus()
            tag.contents = [Dingus()] * 3
            tag['href'] = 'http://www.com'
            if i % 2 != 0:
                for contents in tag.contents:                    
                    contents.string = u'\r\n string\r\n'
            else:
                all_contents = []
                for i in range(3):
                    contents = Dingus()
                    if i == 1:
                        contents.string = u'||'
                    else:
                        contents.string = u'\n'
                    all_contents.append(contents)
                tag.contents = all_contents
            all_tags.append(tag)
        self.table.findAll.return_value = all_tags
        self.extracted = self.extractor.extract()

    def should_remove_blank_lines(self):
        fragment = '\r\n string\r\n'
        assert self.extracted == [((fragment*3,)*2,)*6] 

class WhenExtractingCards(DingusTestCase(CardExtractor)):

    def setup(self):
        super(WhenExtractingCards, self).setup()
        self.extractor = CardExtractor('<html></html>')
        self.table = mod.BeautifulSoup.BeautifulSoup().table
        self.table.findAll.return_value = [Dingus()] * 13
        for tag in self.table.findAll():
            tag.contents = [Dingus()] * 3
            tag['href'] = 'http://www.com'
            for contents in tag.contents:
                contents.string = u'\r\n string\r\n'
        self.extracted = self.extractor.extract()

    def should_be_false_if_empty(self):
        assert not CardExtractor('').extract()
        
    def should_get_card_urls_if_asked(self):
        self.extractor.extract(get_card_urls=True)
        assert mod.BeautifulSoup.BeautifulSoup().table.calls('findAll', 'a')

    def should_add_card_urls_to_content(self):
        extracted = self.extractor.extract(get_card_urls=True)
        fragment = '\r\n string\r\n'
        expected = [( ('url', 'http://www.com'), (fragment*3,)*2, 
                      (fragment*3,)*2, (fragment*3,)*2, (fragment*3,)*2, 
                      (fragment*3,)*2, (fragment*3,)*2,)]
        assert extracted == expected

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

class DescribeRulingExtractor(object):

    def should_accept_html(self):
        self.extractor = RulingExtractor('<html></html>')
        assert self.extractor.html == '<html></html>'

    def should_replace_autocard_tags_with_its_content(self):
        self.extractor = RulingExtractor('<html></html>')
        self.extractor.extract()
        for tag in mod.BeautifulSoup.BeautifulSoup().findAll():
            assert tag.calls('replaceWith', tag.string)


class WhenExtractingRulings(DingusTestCase(RulingExtractor)):

    def setup(self):
        super(WhenExtractingRulings, self).setup()
        self.extractor = RulingExtractor('<html></html>')
        self.soup = mod.BeautifulSoup.BeautifulSoup()
        
        def compile_(string):
            return string
        mod.re.compile = compile_

        def findAll(attrs):
            all_tags = [Dingus()] *3 
            for tag in all_tags:
                if attrs == 'autocard':
                    tag.string = 'autocard'
                elif 'rulingText$' in attrs.values():
                    tag.contents = 'This is a ruling'
                elif 'rulingDate$' in attrs.values():
                    tag.contents = '2010-08-23'
            return all_tags
        self.soup.findAll = findAll
        self.extracted = self.extractor.extract()        

    def should_return_false_if_no_html(self):
        self.extractor = RulingExtractor('')
        assert self.extractor.extract() == False

    def should_parse_html(self):
        assert mod.BeautifulSoup.calls('BeautifulSoup', '<html></html>').once()

    def should_combine_ruling_contents(self):
        print self.extracted
        assert self.extracted == [('2010-08-23', 'This is a ruling'), 
                                  ('2010-08-23', 'This is a ruling'), 
                                  ('2010-08-23', 'This is a ruling')]

