import re

import BeautifulSoup

__all__ = ['CardExtractor', 'RulingExtractor']

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html
        self.fields_per_card = 6

    def _group(self, lst, n):
        newlist = []
        for i in range(0, len(lst), n):
            val = lst[i:i+n]
            if len(val) == n:
                newlist.append(tuple(val))
        return newlist

    def extract(self, get_card_urls=False):
        data_fields = self.fields_per_card
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        if not soup.table:
            raise Exception('Bad format for cards.')
        for tag in soup.findAll('br'):
            tag.replaceWith('||')

        td_tags = soup.table.findAll('td')
        
        # Get rulings hrefs here.
        if get_card_urls:
            data_fields = data_fields + 1
            a_tags = soup.table.findAll('a')
            #print a_tags
            card_urls = [tag['href'] for tag in a_tags]
            print card_urls

        content_lists = [tag.contents for tag in td_tags]
        unified_content = []
        for i, lst in enumerate(content_lists):
            #if lst == [u'\n', u'||', u'\n']:
            if get_card_urls and i % (7 * 2) == 0 and i != len(content_lists):
                print 'Adding the URL HERE'
                unified_content.append('url')
                unified_content.append(card_urls.pop(0))
            print u'{0}: "{1}"'.format(i, u''.join([item.string or u'' for item in lst])).replace('  ', '').replace('\r', '').replace('\n', '')
            unified_content.append(''.join([item.string or u'' for item in lst]))
        
        unified_content = [item for item in unified_content if item != u'\n||\n']
        unified_content = self._group(unified_content, 2)
        unified_content = self._group(unified_content, data_fields)
        
        return unified_content


class RulingExtractor(object):

    def __init__(self, html):
        self.html = html

    def extract(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        for tag in soup.findAll('autocard'):
            print tag
            print tag.string
            tag.replaceWith(tag.string)
        rulings_text = soup.findAll(attrs={'id' : re.compile('rulingText$')})
        rulings_date = soup.findAll(attrs={'id' : re.compile('rulingDate$')})
        rulings_text = [''.join(tag.contents) for tag in rulings_text]
        rulings_date = [''.join(tag.contents) for tag in rulings_date]
        return zip(rulings_date, rulings_text)
