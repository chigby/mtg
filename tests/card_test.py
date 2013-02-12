import unittest

from dingus import DingusTestCase, Dingus

import mtglib.card_extractor as mod
from mtglib.card_extractor import Card, CardExtractor

class DescribeCard(object):

    def setUp(self):
        self.card = Card()

    def should_have_name(self):
        assert hasattr(self.card, 'card_name')

    def should_have_cost(self):
        assert hasattr(self.card, 'mana_cost')

    def should_have_type(self):
        assert hasattr(self.card, 'types')

    def should_have_rules_text(self):
        assert hasattr(self.card, 'card_text')

    def should_prioritize_all_sets_for_display_sets(self):
        self.card.all_sets = 'All sets'
        assert self.card.display_set == self.card.all_sets


class WhenPrintingCard(object):

    def setup(self):
        self.extractor = CardExtractor(open('tests/_data/acorn_harvest.html'))
        self.extracted = self.extractor.extract()
        self.card = self.extracted[0]

    def should_include_name(self):
        assert self.card.card_name in self.card.show()

    def should_include_mana_cost(self):
        assert self.card.mana_cost in self.card.show()

    def should_include_types(self):
        assert self.card.types in self.card.show()


class WhenRemovingReminderText(unittest.TestCase):
    """When Removing Reminder Text"""

    def should_delete_reminder_text(self):
        text = 'Flying (Can only be blocked by creatures with flying.)'
        assert Card.replace_reminders(text) == 'Flying'

    def should_remove_hybrid_mana_reminders(self):
        text = '({(g/w)} can be paid with either {G} or {W}.) ; Other ' \
            'permanents you control can\'t be the targets of spells or' \
            ' abilities your opponents control.'
        replaced_text =  ' ; Other permanents you control can\'t be the' \
            ' targets of spells or abilities your opponents control.'
        assert Card.replace_reminders(text) == replaced_text

    def should_preserve_hybrid_activation_costs(self):
        text = '{(g/u)}: ~this~ gains shroud until end of turn. ;'
        assert Card.replace_reminders(text) == text

    def should_remove_level_up_reminder(self):
        text = ('Level up {W} ({W}: Put a level counter on this. Level up'
                ' only as a sorcery.) ;')
        replaced_text = 'Level up {W} ;'
        assert Card.replace_reminders(text) == replaced_text

    def should_preserve_multi_hybrid_activations(self):
        text = ('{(r/w)}: ~this~ becomes a 2/2 Kithkin Spirit. ;'
                '{(r/w){(r/w){(r/w)}: If ~this~ is a Spirit, it becomes a 4/4 '
                'Kithkin Spirit Warrior. ; {(r/w){(r/w){(r/w){(r/w){(r/w)'
                '{(r/w)}: If ~this~ is a Warrior, it becomes an 8/8 Kithkin'
                ' Spirit Warrior Avatar with flying and first strike.')
        assert Card.replace_reminders(text) == text

    def should_preserve_hybrid_activations_with_reminders(self):
        text = 'Cycling {(w/u)} ({(w/u)}, Discard this card: Draw a card.)'
        replaced = 'Cycling {(w/u)}'
        assert Card.replace_reminders(text) == replaced

    def should_handle_multiple_reminders_with_mana_costs(self):
        text = ('Kicker {2}{B} (You may pay an additional {2}{B} as you'
                ' cast this spell.) ; Target creature gets +3/+0 until end of'
                ' turn. If ~this~ was kicked, that creature gains lifelink '
                'until end of turn. (Damage dealt by the creature also causes '
                'its controller to gain that much life.)')
        replaced_text = ('Kicker {2}{B} ; Target creature gets +3/+0 until '
                         'end of turn. If ~this~ was kicked, that creature '
                         'gains lifelink until end of turn.')
        assert Card.replace_reminders(text) == replaced_text

    def should_handle_quotation_marks(self):
        text = ('Change the text of target permanent by replacing all '
                'instances of one color word or basic land type with another '
                'until end of turn. (For example, you may change "nonred '
                'creature" to "nongreen creature" or "plainswalk" to '
                '"swampwalk.")')
        repl = ('Change the text of target permanent by replacing all '
                'instances of one color word or basic land type with another '
                'until end of turn.')
        assert Card.replace_reminders(text) == repl
