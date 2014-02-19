# -*- coding: utf-8 -*-
import re
import textwrap

from lxml.html import parse

from mtglib.card_renderer import Card
from mtglib.constants import RARITY_PATTERN
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
        p = [t for t in self.document.cssselect('td') if not t.get('colspan')]
        card = Card()
        for label, value in zip(p[0::2], p[1::2]):
            attr = label.text_content().strip(': \n\r') \
                                       .replace(' ', '_').lower()
            if attr == 'name':
                card.name = value.text_content().strip()
            if attr == 'type':
                card.types, card.subtypes = self.types(value.text_content().strip())
            if attr == 'cost':
                card.mana_cost = value.text_content().strip()
            if attr == 'loyalty':
                card.loyalty = value.text_content().strip(' \n\r()')
            if attr == 'pow/tgh' and value.text_content().strip('\n\r() '):
                card.power, card.toughness = self.split_pow_tgh(value.text_content().strip('\n\r() '))
            if attr == 'rules_text':
                card.rules_text = value.text_content().strip().replace('\n', ' ; ')
            if attr == 'set/rarity':
                card.printings = self.printings_text(value)

                # kind of a hack, set/rarity is always last.
                cards.append(card)
                card = Card()
        return cards

    def split_pow_tgh(self, text):
        """Split a power/toughness string on the correct slash.

        Correctly accounts for curly braces to denote fractions.
        E.g., '2/2' --> ['2', '2']
        '3{1/2}/3{1/2}' --> ['3{1/2}', '3{1/2}']

        """
        return [n for n in re.split(r"/(?=([^{}]*{[^{}]*})*[^{}]*$)", text)
                if n is not None][:2]

    def pow_tgh(self, element):
        matches = re.match(r'\s*(\S+)\s*/\s*(\S+)\s*', element.text_content())
        if matches:
            return matches.groups()

    def types(self, text):
        typeline = clean_dashes(text)
        if u'\u2014' in typeline:
            typeline, sub = typeline.split(u'\u2014')
            sub = sub.strip().split(' ')
        else:
            sub = []
        typ = typeline.strip().split(' ')
        return typ, sub

    def printings_text(self, element):
        printings = []
        for t in element.text_content().strip().split(', '):
            match = re.search(RARITY_PATTERN, t)
            if match:
                expansion, rarity = match.groups()[0:2]
                printings.append((expansion, rarity))
        return printings

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
                elif attr == 'types':
                    attributes['types'], attributes['subtypes'] = self.types(value.text_content().strip())
                elif attr == 'community_rating':
                    attributes['community_rating'] = self.text_field(
                        value, 'span.textRatingValue')
                    attributes['community_votes'] = self.text_field(
                        value, 'span.totalVotesValue')
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
                         'Snow': 'S',
                         'Variable Colorless': 'X',
                         'Two': '2',
                         'Infinite': u'∞',
                         '500': '(Half W)'}

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
        elif self.is_half:
            return self.half
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
    def is_half(self):
        return 'Half' in self.text

    @property
    def hybrid(self):
        return '({0})'.format('/'.join(
                Symbol(l).short for l in self.text.split(' or ')))

    @property
    def half(self):
        return 'Half {0}'.format(Symbol(self.text.split(' ')[-1]).short)

    @property
    def textbox(self):
        base = u'{{{0}}}'.format(self.short)
        if '/' in base: return base.lower()
        else: return base