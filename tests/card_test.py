import unittest2

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


# class WhenCreatingFromBlock(object):

#     def setUp(self):
#         self.block = (
#             (u'\r\n              Name:\r\n          ', u'\nSengir Vampire\n'),
#             (u'\r\n              Cost:\r\n          ', u'\r\n     3BB\r\n   '),
#             (u'\r\n              Type:\r\n          ', u'\r\n    Creature  \u2014 Vampire\r\n                    '),
#             (u'\r\n                        Pow/Tgh:\r\n                    ', u'\r\n                        (4/4)\r\n                    '),
#             (u'\r\n                        Rules Text:\r\n                    ', u"\r\n                        Flying (This creature can't be blocked except by creatures with flying or reach.)||\nWhenever a creature dealt damage by Sengir Vampire this turn is put into a graveyard, put a +1/+1 counter on Sengir Vampire.\r\n                    "),
#             (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Tenth Edition Rare, Ninth Edition Rare, Torment Rare, Beatdown Box Set Uncommon, Battle Royale Box Set Uncommon, Fourth Edition Uncommon, Revised Edition Uncommon, Unlimited Edition Uncommon, Limited Edition Beta Uncommon, Limited Edition Alpha Uncommon\r\n                    ')
#             )
#         self.card = Card.from_block(self.block)

#     def should_return_card(self):
#         assert isinstance(self.card, Card)

#     def should_extract_name(self):
#         assert self.card.name == 'Sengir Vampire'

#     def should_extract_cost(self):
#         assert self.card.cost == '3BB'

#     def should_extract_type(self):
#         assert self.card.type == u'Creature  \u2014 Vampire'

#     def should_extract_rules_text(self):
#         rules_text = ('Flying (This creature can\'t be blocked except by '
#                       'creatures with flying or reach.) ; Whenever a creature '
#                       'dealt damage by Sengir Vampire this turn is put into a '
#                       'graveyard, put a +1/+1 counter on Sengir Vampire.')
#         assert self.card.rules_text == rules_text

#     def should_extract_set_rarity(self):
#         set_rarity = ('Tenth Edition Rare, Ninth Edition Rare, Torment Rare, '
#                       'Beatdown Box Set Uncommon, Battle Royale Box Set '
#                       'Uncommon, Fourth Edition Uncommon, Revised Edition '
#                       'Uncommon, Unlimited Edition Uncommon, Limited Edition '
#                       'Beta Uncommon, Limited Edition Alpha Uncommon')
#         assert self.card.set_rarity == set_rarity

#     def should_extract_loyalty(self):
#         assert self.card.loyalty == ''

#     def should_extract_pow_tough(self):
#         assert self.card.pow_tgh == '(4/4)'

# class WhenCreatingPlaneswalkerFromBlock(object):

#     def setUp(self):
#         self.block = (
#             ('url', 'http://www.com'),
#             (u'\r\n                        Name:\r\n                    ', u'\nLiliana Vess\n'),
#             (u'\r\n                        Cost:\r\n                    ', u'\r\n                        3BB\r\n                    '),
#             (u'\r\n                        Type:\r\n                    ', u'\r\n                        Planeswalker  \u2014 Liliana\r\n                    '),
#             (u'\r\n                        Loyalty:\r\n                    ', u'\r\n                        (5)\r\n                    '),
#             (u'\r\n                        Rules Text:\r\n                    ', u'\r\n                        +1: Target player discards a card.||\n-2: Search your library for a card, then shuffle your library and put that card on top of it.||\n-8: Put all creature cards in all graveyards onto the battlefield under your control.\r\n                    '),
#             (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Magic 2011 Mythic Rare, Duel Decks: Garruk vs. Liliana Mythic Rare, Magic 2010 Mythic Rare, Lorwyn Rare\r\n                    ')
#             )
#         self.card = Card.from_block(self.block)

#     def should_extract_name(self):
#         assert self.card.name == 'Liliana Vess'

#     def should_extract_cost(self):
#         assert self.card.cost == '3BB'

#     def should_extract_rules_text(self):
#         rules_text = ('+1: Target player discards a card. ; -2: Search your'
#                       ' library for a card, then shuffle your library and put'
#                       ' that card on top of it. ; -8: Put all creature cards '
#                       'in all graveyards onto the battlefield under your '
#                       'control.')
#         assert self.card.rules_text == rules_text

#     def should_extract_loyalty(self):
#         assert self.card.loyalty == '(5)'

#     def should_extract_url(self):
#         assert self.card.url == 'http://www.com'

# class WhenPrintingCreatureCard(unittest2.TestCase):

#     def setUp(self):
#         self.block = (
#             (u'\r\n                        Name:\r\n                    ', u'\nCloud Crusader\n'),
#             (u'\r\n                        Cost:\r\n                    ', u'\r\n                        2WW\r\n                    '),
#             (u'\r\n                        Type:\r\n                    ', u'\r\n                        Creature  \u2014 Human Knight\r\n                    '),
#             (u'\r\n                        Pow/Tgh:\r\n                    ', u'\r\n                        (2/3)\r\n                    '),
#             (u'\r\n                        Rules Text:\r\n                    ', u'\r\n                        Flying||\nFirst strike (This creature deals combat damage before creatures without first strike.)\r\n                    '),
#             (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Magic 2011 Common\r\n                    ')
#             )

#         self.card = Card.from_block(self.block)

#     def should_use_unicode(self):
#         assert isinstance(self.card.show(), unicode)

#     def should_print_okay(self):
#         assert self.card.show() == (u'Cloud Crusader 2WW\nCreature \u2014 '
#                                     u'Human Knight\nText: (2/3) Flying ; First'
#                                     ' strike\nMagic 2011 Common')

# class WhenPrintingSingleCardInfo(DingusTestCase(Card, exclude=['textwrap'])):

#     def setup(self):
#         super(WhenPrintingSingleCardInfo, self).setup()
#         self.card = Card()
#         self.card.pow_tgh = '(1/1)'
#         self.card.url = 'http://www.com'
#         extractor = mod.SingleCardExtractor().extract
#         extractor.return_value = [('2010-08-23', 'This is a ruling'),
#                                   ('2010-08-23', 'This is a very long ruling that '
#                                    'just keeps going on and on and does not stop '
#                                    'for anything.'),
#                                   ('2010-08-23', 'This is a ruling')]
#         mod.SingleCardExtractor().extract_flavor.return_value = \
#             ('As it spins, dead voices shriek in an ever-increasing cacophony, '
#              'rending the mind asunder.')


#     def should_allow_rulings_requests(self):
#         self.card.show(rulings=True)
#         assert mod.CardRequest.calls('()', 'http://www.com')

#     def should_extract_rulings(self):
#         self.card.show(rulings=True)
#         assert mod.SingleCardExtractor.calls('()', mod.CardRequest().send())
#         assert mod.SingleCardExtractor().calls('extract').once()

#     def should_format_rulings(self):
#         self.card.show(rulings=True)
#         assert self.card.rulings == ('\n2010-08-23: This is a ruling\n'
#                                      '2010-08-23: This is a very long ruling '
#                                      'that just keeps going on and on\nand '
#                                      'does not stop for anything.\n2010-08-23:'
#                                      ' This is a ruling')

#     def should_show_rulings(self):
#         assert self.card.rulings in self.card.show(rulings=True)

#     def should_allow_flavor_text_request(self):
#         self.card.show(flavor=True)
#         assert mod.CardRequest.calls('()', 'http://www.com')

#     def should_extract_flavor_text(self):
#         self.card.show(flavor=True)
#         assert mod.SingleCardExtractor.calls('()', mod.CardRequest().send())
#         assert mod.SingleCardExtractor().calls('extract_flavor').once()

#     def should_show_flavor_text(self):
#         assert self.card.flavor_text in self.card.show(flavor=True)

#     def should_format_flavor_text(self):
#         self.card.show(flavor=True)
#         print self.card.flavor
#         assert self.card.flavor == ('As it spins, dead voices shriek in an '
#                                     'ever-increasing cacophony,\nrending the'
#                                     ' mind asunder.\n')

# class WhenPrintingCardWithManySets(object):

#     def setup(self):
#         self.block = (
#             ('url', 'http://www.com'),
#             (u'\r\n                        Name:\r\n                    ', u'\nGiant Growth\n'),
#             (u'\r\n                        Cost:\r\n                    ', u'\r\n                        G\r\n                    '),
#             (u'\r\n                        Type:\r\n                    ', u'\r\n                        Instant\r\n                    '),
#             (u'\r\n                        Pow/Tgh:\r\n                    ', u'\n'),
#             (u'\r\n                        Rules Text:\r\n                    ', u'\r\n                        Target creature gets +3/+3 until end of turn.\r\n                    '),
#             (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Magic 2011 Common, Duel Decks: Garruk vs. Liliana Common, Masters Edition III Common, Magic 2010 Common, Masters Edition II Common, Duel Decks: Elves vs. Goblins Common, Tenth Edition Common, Ninth Edition Common, Eighth Edition Common, Seventh Edition Common, Beatdown Box Set Common, Starter 2000 Common, Battle Royale Box Set Common, Classic Sixth Edition Common, Fifth Edition Common, Ice Age Common, Fourth Edition Common, Revised Edition Common, Unlimited Edition Common, Limited Edition Beta Common, Limited Edition Alpha Common\r\n                    ')
#             )
#         self.card = Card.from_block(self.block)

#     def should_wrap_set_list(self):
#         assert self.card.show().count('\n') == 10

# class WhenPrintingSorceryCard(object):

#     def setup(self):
#         self.block = (
#             (u'\r\n                        Name:\r\n                    ', u"\nWinter's Chill\n"),
#             (u'\r\n                        Cost:\r\n                    ', u'\r\n                        XU\r\n                    '),
#             (u'\r\n                        Type:\r\n                    ', u'\r\n                        Instant\r\n                    '),
#             (u'\r\n                        Pow/Tgh:\r\n                    ', u'\n'),
#             (u'\r\n                        Rules Text:\r\n                    ', u"\r\n                        Cast Winter's Chill only during combat before blockers are declared.||\nX can't be greater than the number of snow lands you control.||\nDestroy X target attacking creatures at end of combat. For each attacking creature, its controller may pay {1} or {2} to prevent this effect. If that player pays only {1} for that creature, prevent all combat damage that would be dealt to and dealt by that creature this turn.\r\n                    "),
#             (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Ice Age Rare\r\n                    ')
#             )
#         self.card = Card.from_block(self.block)

#     def should_wrap_text(self):
#         assert self.card.show().count('\n') == 9

#     def should_replace_card_name(self):
#         rules_text = u' '.join(self.card.show().split('\n')[2:])
#         assert '~this~' in rules_text
#         assert 'Winter\'s Chill' not in rules_text

class WhenRemovingReminderText(unittest2.TestCase):
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
