import re
import textwrap

class Card(object):

    def __init__(self):
        self.name = ''
        self.mana_cost = ''
        self.types = ''
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


class CardRenderer(object):

    def __init__(self, card, rulings=False, reminders=True, flavor=False,
                 printings=True):
        self.card = card
        self.rulings = rulings
        self.reminders = reminders
        self.flavor = flavor
        self.printings = printings

    def render(self):
        card_format = [u'{0.name} {0.mana_cost}',
                       u'{0.types}',
                       ]

        card_data = [line.format(self.card) for line in card_format]

        card_data.extend(self.render_rules_text())
        if self.flavor and self.card.flavor_text:
            card_data.extend(self.render_flavor_text())
        if self.printings: card_data.extend(self.render_printings())
        if self.rulings: card_data.extend(self.render_rulings())
        return card_data

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
        lines = textwrap.wrap(rules_text_format.format(self.card, rules_text))
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