# -*- coding: utf-8 -*-
import re
import textwrap

from dingus import DingusTestCase, Dingus, returner
from nose.tools import assert_raises, eq_

import mtglib.card_extractor as mod
from mtglib.gatherer_request import CardRequest
from mtglib.card_extractor import CardExtractor, Card, Symbol

class DescribeCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_card_source(self):
        assert hasattr(self.extractor, 'card_source')

    def should_have_cards(self):
        self.extractor = CardExtractor(open('tests/_data/acorn_harvest.html'))
        assert self.extractor.cards


class WhenExtractingSingleCard(object):

    def setup(self):
        self.extractor = CardExtractor(open('tests/_data/acorn_harvest.html'))
        self.extracted = self.extractor.extract()
        self.card = self.extracted[0]

    def should_get_one_result(self):
        eq_(len(self.extracted), 1)

    def should_extract_name(self):
        assert self.card.card_name == 'Acorn Harvest'

    def should_extract_mana_cost(self):
        eq_(self.card.mana_cost, '3G')

    def should_extract_types(self):
        assert self.card.types == 'Sorcery'

    def should_extract_text(self):
        eq_(self.card.card_text, unicode('Put two 1/1 green Squirrel creature '
            'tokens onto the battlefield. ; Flashback\xe2\x80\x94{1}{G}, Pay 3 life.'
            ' (You may cast this card from your graveyard for its flashback '
            'cost. Then exile it.)', 'utf-8'))

    def should_extract_rarity(self):
        eq_(self.card.rarity, 'Common')

    def should_extract_expansion(self):
        eq_(self.card.expansion, 'Torment')

    def should_extract_artist(self):
        eq_(self.card.artist, 'Edward P. Beard, Jr.')

    def should_extract_converted_mana_cost(self):
        eq_(self.card.converted_mana_cost, '4')

    def should_extract_card_number(self):
        eq_(self.card.card_number, '118')


class WhenExtractingSingleCreature(object):

    def setup(self):
        self.ex = CardExtractor(open('tests/_data/personal_incarnation.html'))
        self.extracted = self.ex.extract()
        self.card = self.extracted[0]

    def should_extract_power_and_toughness(self):
        '6/6' in self.card.show()


class WhenExtractingSingleCardWithManySets(object):

    def setup(self):
        self.extractor = CardExtractor(open('tests/_data/blazing_torch.html'))
        self.extracted = self.extractor.extract()
        self.card = self.extracted[0]

    def should_extract_all_sets(self):
        eq_(self.card.all_sets, 'Zendikar (Uncommon), Innistrad (Common)')


class WhenExtractingSingleDualFacedPlaneswalker(object):

    def setup(self):
        extractor = CardExtractor(open('tests/_data/garruk_relentless.html'))
        self.cards = extractor.extract()

    def should_get_two_results(self):
        eq_(len(self.cards), 2)

    def should_extract_names(self):
        eq_(self.cards[0].card_name, 'Garruk Relentless')
        eq_(self.cards[1].card_name, 'Garruk, the Veil-Cursed')

    def should_extact_loyalty(self):
        eq_(self.cards[0].loyalty, '3')

    def should_extract_color_indicator(self):
        eq_(self.cards[1].color_indicator, 'Black, Green')


class WhenExtractingMultipleCards(object):

    def setup(self):
        self.html = open('tests/_data/hex.html')
        self.cards = CardExtractor(self.html).extract_many()

    def should_get_nine_results(self):
        eq_(len(self.cards), 9)

    def should_extract_name(self):
        eq_(self.cards[0].card_name, 'Elvish Hexhunter')

    def should_extract_mana_cost(self):
        eq_(self.cards[0].mana_cost, '(G/W)')

    def should_extract_multipart_mana_cost(self):
        eq_(self.cards[1].mana_cost, '4BB')

    def should_extract_types(self):
        eq_(self.cards[0].types, unicode('Creature  — Elf Shaman', 'utf-8'))

    def should_extract_power_toughness_block(self):
        eq_(self.cards[0].pow_tgh, '(1/1)')

    def should_extract_card_text(self):
        eq_(self.cards[0].card_text, '{(g/w)}, {T}, Sacrifice Elvish Hexhunter'
            ': Destroy target enchantment.')

    def should_extract_multipart_card_text(self):
        eq_(self.cards[7].card_text, 'First strike ; Sacrifice Vampire Hexmage'
            ': Remove all counters from target permanent.')

    def should_extract_card_expansion(self):
        eq_(self.cards[0].set_rarity, 'Shadowmoor (Common)')

    def should_extract_multiple_card_expansions(self):
        eq_(self.cards[1].set_rarity, 'Magic: The Gathering-Commander (Rare), '
            'Ravnica: City of Guilds (Rare)')


class WhenExtractingFlavorText(object):

    def setup(self):
        self.html = open('tests/_data/mirari.html')
        self.cards = CardExtractor(self.html).extract()

    def should_format_flavor_text(self):
        assert 'Braids' in self.cards[0].show(flavor=True)
        assert u' \u2014' in self.cards[0].show(flavor=True)

    def should_exclude_flavor_text_by_default(self):
        assert 'Braids' not in self.cards[0].show()


class WhenExtractingRulings(object):

    def setup(self):
        self.html = open('tests/_data/mirari.html')
        self.cards = CardExtractor(self.html).extract()

    def should_extract_all_rulings(self):
        eq_(len(self.cards[0].ruling_data), 7)

    def should_extract_ruling_date(self):
        eq_(self.cards[0].ruling_data[0][0], '2004/10/4')

    def should_extract_ruling_text(self):
        eq_(self.cards[0].ruling_data[0][1], 'Everything about the original '
            'spell is copied, including any decisions made on announcement, '
            'such as whether it was kicked or its Buyback cost was paid. '
            'Effects on the spell, such as Sleight of Mind or Flashback, are'
            ' not copied. ')


class DescribeSymbols(object):

    def should_abbreviate_color_names(self):
        eq_(Symbol('Green').short, 'G')

    def should_abbreviate_color_names(self):
        eq_(Symbol('Blue').short, 'U')

    def should_abbreviate_tap(self):
        eq_(Symbol('Tap').short, 'T')

    def should_abbreviate_untap(self):
        eq_(Symbol('Untap').short, 'Q')

    def should_abbreviate_hybrid_mana(self):
        eq_(Symbol('Blue or Black').short, '(U/B)')

    def should_format_for_textboxes(self):
        eq_(Symbol('Green').textbox, '{G}')

    def should_downcase_hybrid_mana_in_textbox(self):
        eq_(Symbol('Blue or Black').textbox, '{(u/b)}')

    def should_abbreviate_phyrexian_mana(self):
        eq_(Symbol('Phyrexian Black').short, '(B/P)')

    def should_downcase_phyrexian_mana_in_textbox(self):
        eq_(Symbol('Phyrexian Blue').textbox, '{(u/p)}')

    def should_preserve_all_numerals(self):
        eq_(Symbol('12').short, '12')

    def should_format_show_mana(self):
        eq_(Symbol('Snow').textbox, '{S}i}')

    def should_format_x(self):
        eq_(Symbol('Variable Colorless').short, 'X')

    def should_format_hybrid_colorless_mana(self):
        eq_(Symbol('Two or White').short, '(2/W)')
