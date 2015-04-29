import re
import textwrap
import json

from mtglib.constants import separator
from mtglib.colors import ColoredManaSymbol

class Card(object):

    def __init__(self):
        self.name = ''
        self.mana_cost = ''
        self.types = []
        self.subtypes = []
        self.rules_text = ''
        self.loyalty = ''
        self.power = ''
        self.toughness = ''
        self.all_sets = ''
        self.printings = []
        self.ruling_data = []
        self.flavor_text = ''
        self.color_indicator = ''


def remove_reminders(text):
        """Remove reminder text from a string.

        Reminder text, as defined by magic cards, consists of complete
        sentences enclosed in parentheses.

        """
        return re.sub(r'(\A|\ )\(.*?\.\"?\)+', '', text)


class CardList(object):

    def __init__(self, cards, rulings=False, reminders=True, flavor=False,
                 printings=True, json=False, colourize=False):
        self.cards = cards
        self.json = json
        self.renderer = CardRenderer(Card(), rulings, reminders, flavor,
                                     printings, json, colourize)

    def render(self):
        if self.json:
            return self.render_json().split('\n')
        elif len(self.cards) < 1:
            return ['No results found.']
        else:
            return self.render_human()

    def num_results(self):
        num = len(self.cards)
        if num != 1:
            plural_char = 's'
        else:
            plural_char = ''
        message = '\n{0} result{1} found.'.format(num, plural_char)
        if num == 25:
            message += '\nNote: more matching cards may exist; try refining your search.'
        return message

    def render_human(self):
        lines = []
        for card in self.cards:
            lines.append(separator)
            self.renderer.card = card
            lines.extend(self.renderer.render())
        lines.append(self.num_results())
        return lines

    def render_json(self):
        card_dicts = [dict((k,v) for k,v in c.__dict__.items() if v) for c in
                      self.cards]
        return json.dumps(card_dicts, sort_keys=True, indent=4,
                          separators=(',', ': '))


class CardRenderer(object):

    def __init__(self, card, rulings=False, reminders=True, flavor=False,
                 printings=True, json=False, colourize=False):
        self.card = card
        self.rulings = rulings
        self.reminders = reminders
        self.flavor = flavor
        self.printings = printings
        self.json = json
        self.colourize = colourize

    def render(self):
        if self.colourize:
            card_format = [u'{0.name}']
            card_data = [line.format(self.card) for line in card_format]
            card_data[0] += ' ' + ColoredManaSymbol().color(self.card.mana_cost)
        else:
            card_format = [u'{0.name} {0.mana_cost}']
            card_data = [line.format(self.card) for line in card_format]

        if self.json:
            return self.render_json()

        card_data.extend(self.render_types())
        card_data.extend(self.render_rules_text())
        if self.flavor and self.card.flavor_text:
            card_data.extend(self.render_flavor_text())
        if self.printings:
            card_data.extend(self.render_printings())
        if self.rulings:
            card_data.extend(self.render_rulings())

        return card_data

    def render_json(self):
        json_data = {}
        for field in dir(self.card):
            if '__' in field or not getattr(self.card, field):
                continue
            else:
                json_data[field] = getattr(self.card, field)

        j_string = json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))
        return j_string.split('\n')

    def render_flavor_text(self):
        flavor_text = [u'* * *']
        for line in self.card.flavor_text.split('\n'):
            flavor_text.extend(textwrap.wrap(line))
        return flavor_text

    def render_printings(self):
        set_format = u'%s (%s)'
        return textwrap.wrap(u', '.join(
            [set_format % p for p in self.card.printings]))

    def render_rules_text(self):
        rules_text_format = u'Text: '
        if self.card.power and self.card.toughness:
            rules_text_format += u'({0.power}/{0.toughness}) '
        rules_text_format += u'{1}'
        if self.reminders:
            rules_text = self.card.rules_text
        else:
            rules_text = remove_reminders(self.card.rules_text).strip(' ;')
        lines = []
        for line in rules_text_format.format(self.card, rules_text).split('\n'):
            lines.extend(textwrap.wrap(line))

        if self.card.loyalty:
            lines.append(u'Loyalty: {0.loyalty}'.format(self.card))
        if self.card.color_indicator:
            lines.append(u'Color: {0.color_indicator}'.format(self.card))
        return lines

    def render_rulings(self):
        rulings = []
        for r in self.card.ruling_data:
            rulings.extend(textwrap.wrap(u'%s: %s' % r))
        return rulings

    def render_types(self):
        if not self.card.subtypes:
            return [' '.join(self.card.types)]
        return [u'{0} \u2014 {1}'.format(' '.join(self.card.types),
                                         ' '.join(self.card.subtypes))]
