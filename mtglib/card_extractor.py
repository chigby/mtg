import re
import textwrap

import BeautifulSoup

from mtglib.gatherer_request import CardRequest

__all__ = ['CardExtractor', 'SingleCardExtractor', 'Card']

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
            return []
        for tag in soup.findAll('br'):
            tag.replaceWith('||')

        td_tags = soup.table.findAll('td')
        
        # Get rulings hrefs here.
        if get_card_urls:
            a_tags = soup.table.findAll('a')
            card_urls = [tag['href'] for tag in a_tags]
            
        content_lists = [tag.contents for tag in td_tags]
        unified_content = []
        cards = []
        for lst in content_lists:
            unified_content.append(''.join([item.string or u'' for item in lst]))
        
        unified_content = [item for item in unified_content if item != u'\n||\n']
        unified_content = self._group(unified_content, 2)
        unified_content = self._group(unified_content, data_fields)
        
        for block in unified_content:
            card = Card.from_block(block)
            if get_card_urls:
                card.url = card_urls.pop(0)
            cards.append(card)
        return cards


class SingleCardExtractor(object):

    def __init__(self, html):
        self.html = html

    def _parse_html(self):
        if not self.html:
            return False
                
    def extract_flavor(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        flavor_text = soup.findAll(attrs={'id': re.compile('FlavorText$')})
        if flavor_text:
            flavor_text = flavor_text[0].findAll('i')[0].contents[0]
        else:
            flavor_text = ''
        return flavor_text        

    def extract(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        for tag in soup.findAll('autocard'):
            tag.replaceWith(tag.string)
        rulings_text = soup.findAll(attrs={'id' : re.compile('rulingText$')})
        rulings_date = soup.findAll(attrs={'id' : re.compile('rulingDate$')})
        rulings_text = [''.join(tag.contents) for tag in rulings_text]
        rulings_date = [''.join(tag.contents) for tag in rulings_date]
        return zip(rulings_date, rulings_text)


class Card(object):

    def __init__(self):
        self.name = ''
        self.cost = ''
        self.type = ''
        self.rules_text = ''
        self.set_rarity = ''
        self.loyalty = ''
        self.pow_tgh = ''
        self.url = ''
        self.ruling_data = []
        self.flavor_text = ''
        self.card_template = (u"{0.name} {0.cost}\n"
                              u"{0.type}\nText: {0.number} {0.rules_text}\n"
                              u"{0.flavor}{0.set_rarity}{0.rulings}")

    @classmethod
    def from_block(cls, block):
        card = cls()
        for line in block:
            setattr(card, Card.prettify_attr(line[0]), Card.prettify_text(line[1]))
        return card

    def show(self, reminders=False, rulings=False, flavor=False):
        self._format_fields(reminders)
        if rulings:
            self.ruling_data = \
                SingleCardExtractor(CardRequest(self.url).send()).extract()
        if flavor:
            self.flavor_text = \
                SingleCardExtractor(CardRequest(self.url).send()).extract_flavor()
            
        return self.card_template.format(self)

    def _format_fields(self, reminders):
        self.type = self.type.replace('  ', ' ')
        self.set_rarity = textwrap.fill(self.set_rarity)
        self._format_rules_text(reminders)

    def _format_rules_text(self, reminders):
        if not reminders:
            self.rules_text = self.replace_reminders(self.rules_text)
        self.rules_text = self.rules_text.replace(self.name, '~this~')
        self.rules_text = self.formatted_wrap(self.rules_text)
    
    @property
    def number(self):
        return self.pow_tgh or self.loyalty

    @property
    def rulings(self):
        if not self.ruling_data:
            return ''
        return u'\n' + u'\n'.join([textwrap.fill(u'{0}: {1}'.format(date, text))
                                   for date, text in self.ruling_data])

    @property
    def flavor(self):
        return self.flavor_text and textwrap.fill(self.flavor_text) + '\n' or ''
    
    @classmethod
    def formatted_wrap(cls, text):
        return textwrap.fill(u'            {0}'.format(text)).strip()

    @classmethod
    def replace_reminders(cls, text):
        """Remove reminder text from cards (complete sentences enclosed in
        parentheses)."""
        return re.sub(r'(\A|\ )\(.*?\.\)', '', text)    

    @classmethod
    def prettify_text(cls, text):
        """Removes formatting and escape sequences from card text"""
        return text.strip('\r\n ').replace('||', '').replace('\n', ' ; ')

    @classmethod
    def prettify_attr(cls, attr):
        """Removes formatting and escape sequences card attrbutes"""
        return attr.strip(':\r\n ').replace(' ', '_').replace('/', '_').lower()
