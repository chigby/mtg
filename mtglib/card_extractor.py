import re
import textwrap

import BeautifulSoup
from lxml.html import parse

from mtglib.gatherer_request import CardRequest

__all__ = ['CardExtractor', 'SingleCardExtractor', 'Card']

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, card_source):
        self.card_source = card_source
        self._document = None

    def _flatten(self, element):
        """Recursively enter and extract text from all child
        elements."""
        result = [ (element.text or '') ]
        if element.attrib.get('alt'):
            result.append(Symbol(element.attrib.get('alt')).textbox)
        for sel in element:
            result.append(self._flatten(sel))
            result.append(sel.tail or '')
        return ''.join(result)

    @property
    def document(self):
        if getattr(self, '_document') is None:
            self._document = parse(self.card_source).getroot()
        return self._document

    @property
    def cards(self):
        print 'doing card search'
        if 'Card Search' in self.document.cssselect('title')[0].text_content():
            print 'many'
            return self.extract_many()
        else:
            print 'one'
            return self.extract()

    def extract_many(self):
        cards = []

        for item in self.document.cssselect('tr.cardItem'):
            for c in item.cssselect('div.cardInfo'):
                card = Card()
                card.name = c.cssselect('span.cardTitle')[0].text_content().strip()
                for img in c.cssselect('span.manaCost img'):
                    setattr(card, 'mana_cost', Symbol(img.attrib['alt']).short)
                regex = '\([^/]+/[^)]+\)'
                typeline = c.cssselect('span.typeLine')[0].text_content()
                m = re.search(regex, typeline)
                if m:
                    card.pow_tgh = m.group(0)
                    card.types = re.sub(regex, '', typeline).strip()
                else:
                    card.types = typeline.strip()
                card.types = card.types.replace(u'\xe2\x80\x94', u'\u2014')
                card.card_text = self._flatten(c.cssselect('div.rulesText')[0]).strip()

            set_rarity = ', '.join([img.attrib['alt'] for img in
                                    item.cssselect('td.rightCol img')])
            setattr(card, 'set_rarity', set_rarity)
            cards.append(card)
        return cards

    def extract(self):
        cards = []

        for component in self.document.cssselect('td.cardComponentContainer'):
            if not component.getchildren():
                continue # do not parse empty components
            labels = component.cssselect('div.label')
            values = component.cssselect('div.value')
            pairs = zip(labels, values)
            card = Card()
            for (label, value) in pairs:
                l = label.text_content().strip().replace(' ', '_') \
                    .replace(':', '').lower().replace('#', 'number')

                if l == 'card_text':
                    v = ' ; '.join(map(self._flatten,
                                       value.cssselect('div.cardtextbox')))
                else:
                    v = u''
                    if l == 'mana_cost':
                        for img in value.cssselect('img'):
                            v += Symbol(img.attrib['alt']).short
                    if l == 'all_sets':
                        v += ', '.join([img.attrib['alt'] for img in
                                        value.cssselect('img')])

                    v += value.text_content().strip()
                setattr(card, l, v.replace(u'\xe2\x80\x94', u'\u2014'))
            cards.append(card)
        return cards


class Symbol(object):

    def __init__(self, text):
        self.text = text
        self.specials = {'Untap': 'Q',
                         'Blue': 'U',
                         'Snow': 'S}i',
                         'Variable Colorless': 'X',
                         'Two': '2'}

    @property
    def short(self):
        if self.text in self.specials.keys():
            return self.specials[self.text]
        elif self.is_hybrid:
            return self.hybrid
        elif self.is_phyrexian:
            return self.phyrexian
        elif self.text.isdigit():
            return self.text
        return self.text[:1]

    @property
    def is_phyrexian(self):
        return 'Phyrexian ' in self.text

    @property
    def phyrexian(self):
        return '({0}/P)'.format(
            Symbol(self.text.replace('Phyrexian ', '')).short)

    @property
    def is_hybrid(self):
        return ' or ' in self.text

    @property
    def hybrid(self):
        return '({0})'.format('/'.join(
                Symbol(l).short for l in self.text.split(' or ')))

    @property
    def textbox(self):
        base = '{{{0}}}'.format(self.short)
        if '/' in base: return base.lower()
        else: return base


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
        self.card_name = ''
        self.mana_cost = ''
        self.types = ''
        self.card_text = ''
        self.set_rarity = ''
        self.loyalty = ''
        self.pow_tgh = ''
        self.ruling_data = []
        self.flavor_text = ''
        self.card_template = (u"{0.card_name} {0.mana_cost}\n"
                              u"{0.types}\nText: {0.number} {0.card_text}\n"
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
        self.types = self.types.replace('  ', ' ')
        self.set_rarity = textwrap.fill(self.set_rarity)
        self._format_card_text(reminders)

    def _format_card_text(self, reminders):
        if not reminders:
            self.card_text = self.replace_reminders(self.card_text)
        self.card_text = self.card_text.replace(self.card_name, '~this~')
        self.card_text = self.formatted_wrap(self.card_text)

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
