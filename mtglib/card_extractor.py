import re
import textwrap

from lxml.html import parse

from mtglib.card_renderer import Card
from mtglib.functions import is_string

__all__ = ['CardExtractor', 'Card']


attribute_map = {
    'card_#': 'collector_number',
    'card_name': 'name',
    'expansion': 'printings',
    'all_sets': 'printings',
    'card_text': 'rules_text'
}


def clean_dashes(text):
    return text.replace(u'\xe2\x80\x94', u'\u2014').replace(u'  ', u' ')


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

        # prevent reminder text from getting too close to mana symbols
        return ''.join(result).replace('}(', '} (')

    @property
    def document(self):
        if getattr(self, '_document') is None:
            self._document = parse(self.card_source).getroot()
        return self._document

    @property
    def cards(self):
        if 'Card Search' in self.document.cssselect('title')[0].text_content():
            return self.extract_many()
        else:
            return self.extract()

    def text_field(self, container, css):
        return container.cssselect(css)[0].text_content().strip()

    def box_field(self, container, css, separator):
        return separator.join(map(self._flatten, container.cssselect(css)))

    def symbol_field(self, container, css):
        symbols = container.cssselect(css)
        return u''.join([Symbol(img.attrib['alt']).short for img in symbols])

    def extract_many(self):
        cards = []

        for item in self.document.cssselect('tr.cardItem'):
            for c in item.cssselect('div.cardInfo'):
                card = Card()
                card.name = self.text_field(c, '.cardTitle')
                card.mana_cost = self.symbol_field(c, '.manaCost img')
                typeline = self.text_field(c, '.typeLine')
                t = [l.strip() for l in typeline.split('\n') if l.strip()]
                card.types = t.pop(0)
                if t:
                    number = t.pop(0).strip('()')
                    if '/' in number:
                        card.power, card.toughness = number.split('/')
                    else:
                        card.loyalty = number
                card.types = clean_dashes(card.types)
                card.rules_text = self.box_field(c, 'div.rulesText p', ' ; ')
                card.printings = self.printings(item, 'td.rightCol img')
            cards.append(card)
        return cards

    def pow_tgh(self, element):
        matches = re.match(r'\s*(\S+)\s*/\s*(\S+)\s*', element.text_content())
        if matches:
            return matches.groups()

    def printings(self, element, css):
        printings = []
        for img in element.cssselect(css):
            matches = re.match('([^(]+) \(([^)]+)\)', img.attrib['alt'])
            if matches:
                printings.append(matches.groups())
        return printings

    def extract(self):
        cards = []

        for component in self.document.cssselect('td.cardComponentContainer'):
            if not component.getchildren():
                continue # do not parse empty components
            labels = component.cssselect('div.label')
            values = component.cssselect('div.value')
            pairs = zip(labels, values)
            card = Card()
            attributes = {}
            for (label, value) in pairs:
                attr = label.text_content().strip(': \n\r') \
                    .replace(' ', '_').lower()
                attr = attribute_map.get(attr) or attr
                if attr == 'p/t':
                    attributes['power'], attributes['toughness'] = \
                        self.pow_tgh(value)
                elif attr == 'rules_text':
                    attributes[attr] = self.box_field(value,
                                                      'div.cardtextbox', ' ; ')
                elif attr == 'printings':
                    attributes[attr] = self.printings(value, 'img')
                elif attr == 'rarity':
                    continue
                elif attr == 'flavor_text':
                    attributes[attr] = self.box_field(value,
                                                      'div.cardtextbox', '\n')
                elif attr == 'mana_cost':
                    attributes[attr] = self.symbol_field(value, 'img')
                else:
                    attributes[attr] = value.text_content().strip()

            for a, v in attributes.items():
                if is_string(v):
                    v = clean_dashes(v)
                setattr(card, a, v)
            for ruling in component.cssselect('tr.post'):
                date, text = ruling.cssselect('td')
                card.ruling_data.append((date.text_content(),
                                         text.text_content()))
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