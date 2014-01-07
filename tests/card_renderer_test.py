# -*- coding: utf-8 -*-
from unittest import TestCase

from mtglib.card_renderer import Card, CardRenderer, remove_reminders

class DescribeCardRenderer(TestCase):

    def setUp(self):
        self.card = Card()
        self.card.name = u'Name'
        self.card.mana_cost = u'2UUU'
        self.card.types = u'Legendary Creature — Human Wizard'
        self.card.power = 3
        self.card.toughness = 4
        self.card.rules_text = u'Rules Text (This is just an example.)'
        self.card.flavor_text = u'"Flavor text"'
        self.card.printings = [(u'Time Spiral', u'Rare')]
        self.card.ruling_data = [(u'9/25/2006', u'Ruling Text'),
                                 (u'9/25/2006', u'Ruling Two')]

    def should_render_cards(self):
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'Time Spiral (Rare)'])

    def should_wrap_long_rules_text(self):
        self.card.rules_text = u'If Floral Spuzzem attacks an opponent and is not blocked, then Floral Spuzzem may choose to destroy a target artifact under that opponent\'s control and deal no damage.'
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) If Floral Spuzzem attacks an opponent and is not blocked,',
             u'then Floral Spuzzem may choose to destroy a target artifact under that',
             "opponent's control and deal no damage.",
             u'Time Spiral (Rare)'])

    def should_wrap_printings(self):
        self.card.printings = [
            (u'Limited Edition Alpha', u'Common'),
            (u'Limited Edition Beta', u'Common'),
            (u'Unlimited Edition', u'Common'),
            (u'Revised Edition', u'Common'),
            (u'Fourth Edition', u'Common')]
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'Limited Edition Alpha (Common), Limited Edition Beta (Common),',
             u'Unlimited Edition (Common), Revised Edition (Common), Fourth Edition',
             u'(Common)'])

    def should_render_rulings(self):
        output = CardRenderer(self.card, rulings=True).render()
        for line in CardRenderer(self.card, rulings=True).render_rulings():
            self.assertTrue(line in output)

    def should_format_rulings(self):
        self.assertEqual(
            CardRenderer(self.card, rulings=True).render_rulings(),
            [u'9/25/2006: Ruling Text',
             u'9/25/2006: Ruling Two'])

    def should_wrap_rulings(self):
        self.card.ruling_data = [
            (u'12/1/2004', u'If you Fork a Spliced spell, the spliced text is added during the announcement of the original spell, and therefore is fully copied by Fork.'),
            (u'5/1/2009', u'The copy will have the same mana cost as the original spell, but will be red rather than whatever color that mana cost would have made it.')]
        self.assertEqual(
            CardRenderer(self.card, rulings=True).render_rulings(),
            [u'12/1/2004: If you Fork a Spliced spell, the spliced text is added',
             u'during the announcement of the original spell, and therefore is fully',
             u'copied by Fork.',
             u'5/1/2009: The copy will have the same mana cost as the original spell,',
             u'but will be red rather than whatever color that mana cost would have',
             u'made it.'])

    def should_remove_reminders(self):
        self.assertEqual(
            CardRenderer(self.card, reminders=False).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text',
             u'Time Spiral (Rare)'])

    def should_render_flavor_text(self):
        self.assertEqual(
            CardRenderer(self.card, flavor=True).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'* * *',
             u'"Flavor text"',
             u'Time Spiral (Rare)'])

    def should_render_multiline_flavor_text(self):
        self.card.flavor_text = u'"Flavor text"\n-- Jaya Ballard, Task Mage'
        self.assertEqual(
            CardRenderer(self.card, flavor=True).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'* * *',
             u'"Flavor text"',
             u'-- Jaya Ballard, Task Mage',
             u'Time Spiral (Rare)'])

    def should_not_render_flavor_text_if_none(self):
        self.card.flavor_text = u''
        self.assertEqual(
            CardRenderer(self.card, flavor=True).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'Time Spiral (Rare)'])

    def should_hide_printings(self):
        self.assertEqual(
            CardRenderer(self.card, printings=False).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)'])

    def should_print_color_indicator_if_present(self):
        self.card.color_indicator = 'Green'
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: (3/4) Rules Text (This is just an example.)',
             u'Color: Green',
             u'Time Spiral (Rare)'])

    def should_print_loyalty_on_planeswalkers(self):
        self.card.types = u'Planeswalker — Gideon'
        self.card.power = u''
        self.card.toughness = u''
        self.card.loyalty = 5
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Planeswalker — Gideon',
             u'Text: Rules Text (This is just an example.)',
             u'Loyalty: 5',
             u'Time Spiral (Rare)'])

    def should_not_print_numbers_on_instants(self):
        self.card.types = u'Instant'
        self.card.power = u''
        self.card.toughness = u''
        self.assertEqual(
            CardRenderer(self.card).render(),
            [u'Name 2UUU',
             u'Instant',
             u'Text: Rules Text (This is just an example.)',
             u'Time Spiral (Rare)'])

    def should_strip_semicolons(self):
        self.card.rules_text = (u"({T}: Add {W} or {B} to your mana pool.) ; As Godless Shrine enters the battlefield, you may pay 2 life. If you don't, Godless Shrine enters the battlefield tapped.")
        self.card.power = u''
        self.card.toughness = u''
        self.assertEqual(
            CardRenderer(self.card, reminders=False).render(),
            [u'Name 2UUU',
             u'Legendary Creature — Human Wizard',
             u'Text: As Godless Shrine enters the battlefield, you may pay 2 life. If',
             u"you don't, Godless Shrine enters the battlefield tapped.",
             u'Time Spiral (Rare)'])


class WhenRemovingReminderText(TestCase):
    """When Removing Reminder Text"""

    def should_delete_reminder_text(self):
        text = u'Flying (Can only be blocked by creatures with flying.)'
        self.assertEqual(remove_reminders(text), u'Flying')

    def should_remove_hybrid_mana_reminders(self):
        text = u'({(g/w)} can be paid with either {G} or {W}.) ; Other ' \
            u'permanents you control can\'t be the targets of spells or' \
            u' abilities your opponents control.'
        replaced_text = u' ; Other permanents you control can\'t be the' \
            u' targets of spells or abilities your opponents control.'
        self.assertEqual(remove_reminders(text), replaced_text)

    def should_preserve_hybrid_activation_costs(self):
        text = u'{(g/u)}: ~this~ gains shroud until end of turn. ;'
        self.assertEqual(remove_reminders(text), text)

    def should_remove_level_up_reminder(self):
        text = (u'Level up {W} ({W}: Put a level counter on this. Level up'
                u' only as a sorcery.) ;')
        replaced_text = u'Level up {W} ;'
        self.assertEqual(remove_reminders(text), replaced_text)

    def should_preserve_multi_hybrid_activations(self):
        text = (u'{(r/w)}: ~this~ becomes a 2/2 Kithkin Spirit. ;'
                u'{(r/w){(r/w){(r/w)}: If ~this~ is a Spirit, it becomes a 4/4 '
                u'Kithkin Spirit Warrior. ; {(r/w){(r/w){(r/w){(r/w){(r/w)'
                u'{(r/w)}: If ~this~ is a Warrior, it becomes an 8/8 Kithkin'
                u' Spirit Warrior Avatar with flying and first strike.')
        self.assertEqual(remove_reminders(text), text)

    def should_preserve_hybrid_activations_with_reminders(self):
        text = u'Cycling {(w/u)} ({(w/u)}, Discard this card: Draw a card.)'
        replaced = u'Cycling {(w/u)}'
        self.assertEqual(remove_reminders(text), replaced)

    def should_handle_multiple_reminders_with_mana_costs(self):
        text = (u'Kicker {2}{B} (You may pay an additional {2}{B} as you'
                u' cast this spell.) ; Target creature gets +3/+0 until end of'
                u' turn. If ~this~ was kicked, that creature gains lifelink '
                u'until end of turn. (Damage dealt by the creature also causes '
                u'its controller to gain that much life.)')
        replaced_text = (u'Kicker {2}{B} ; Target creature gets +3/+0 until '
                         u'end of turn. If ~this~ was kicked, that creature '
                         u'gains lifelink until end of turn.')
        self.assertEqual(remove_reminders(text), replaced_text)

    def should_handle_quotation_marks(self):
        text = (u'Change the text of target permanent by replacing all '
                u'instances of one color word or basic land type with another '
                u'until end of turn. (For example, you may change "nonred '
                u'creature" to "nongreen creature" or "plainswalk" to '
                u'"swampwalk.")')
        repl = (u'Change the text of target permanent by replacing all '
                u'instances of one color word or basic land type with another '
                u'until end of turn.')
        self.assertEqual(remove_reminders(text), repl)

    def should_handle_nested_reminders(self):
        text = (u'Super haste (This may attack the turn before you play it. (You may put this card into play from your hand, tapped and attacking, during your declare attackers step. If you do, you lose the game at the end of your next turn unless you pay this card\'s mana cost during that turn.))')
        repl = u'Super haste'
        self.assertEqual(remove_reminders(text), repl)