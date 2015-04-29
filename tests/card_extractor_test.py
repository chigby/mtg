# -*- coding: utf-8 -*-
import re
import textwrap

from nose.tools import assert_raises, eq_

from mtglib.card_extractor import CardExtractor, Card, Symbol


def card_html(name):
    return open('tests/_data/{name}.html'.format(name=name))


class DescribeCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_card_source(self):
        assert hasattr(self.extractor, 'card_source')

    def should_have_cards(self):
        self.extractor = CardExtractor(card_html('acorn_harvest'))
        assert self.extractor.cards


class WhenExtractingSingleCard(object):

    def setup(self):
        self.extractor = CardExtractor(card_html('acorn_harvest'))
        self.extracted = self.extractor.extract()
        self.card = self.extracted[0]

    def should_get_one_result(self):
        eq_(len(self.extracted), 1)

    def should_extract_name(self):
        assert self.card.name == 'Acorn Harvest'

    def should_extract_mana_cost(self):
        eq_(self.card.mana_cost, '3G')

    def should_extract_types(self):
        eq_(self.card.types, ['Sorcery'])

    def should_extract_text(self):
        eq_(self.card.rules_text, u'Put two 1/1 green Squirrel creature '
            u'tokens onto the battlefield. ; Flashback—{1}{G}, Pay 3 life.'
            u' (You may cast this card from your graveyard for its flashback '
            u'cost. Then exile it.)')

    def should_not_extract_rarity(self):
        assert not hasattr(self.card, 'rarity')

    def should_extract_expansion(self):
        assert not hasattr(self.card, 'expansion')

    def should_extract_artist(self):
        eq_(self.card.artist, 'Edward P. Beard, Jr.')

    def should_extract_converted_mana_cost(self):
        eq_(self.card.converted_mana_cost, '4')

    def should_extract_collector_number(self):
        eq_(self.card.collector_number, '118')

    def should_extract_expansion(self):
        eq_(self.card.printings, [('Torment', 'Common')])

    def should_extract_community_rating(self):
        eq_(self.card.community_rating, '3.330')

    def should_extract_community_votes(self):
        eq_(self.card.community_votes, '44')

class WhenExtractingSingleCreature(object):

    def setup(self):
        self.ex = CardExtractor(card_html('personal_incarnation'))
        self.extracted = self.ex.extract()
        self.card = self.extracted[0]

    def should_extract_power(self):
        eq_(self.card.power, '6')

    def should_extract_toughness(self):
        eq_(self.card.toughness, '6')


class WhenExtractingSingleCardWithManySets(object):

    def setup(self):
        self.extractor = CardExtractor(card_html('blazing_torch'))
        self.extracted = self.extractor.extract()
        self.card = self.extracted[0]

    def should_extract_all_sets(self):
        eq_(self.card.printings,
            [('Zendikar', 'Uncommon'), ('Innistrad', 'Common')])


class WhenExtractingSingleDualFacedPlaneswalker(object):

    def setup(self):
        extractor = CardExtractor(card_html('garruk_relentless'))
        self.cards = extractor.extract()

    def should_get_two_results(self):
        eq_(len(self.cards), 2)

    def should_extract_names(self):
        eq_(self.cards[0].name, 'Garruk Relentless')
        eq_(self.cards[1].name, 'Garruk, the Veil-Cursed')

    def should_extact_type(self):
        eq_(self.cards[0].types, ['Planeswalker'])
        eq_(self.cards[0].subtypes, ['Garruk'])

    def should_extact_loyalty(self):
        eq_(self.cards[0].loyalty, '3')

    def should_extract_color_indicator(self):
        eq_(self.cards[1].color_indicator, 'Black, Green')


class WhenExtractingManyCardsWithPlaneswalkers(object):

    def setup(self):
        extractor = CardExtractor(card_html('sorin'))
        self.cards = extractor.extract_many()
        self.sorin_markov = self.cards[0]

    def should_get_four_results(self):
        eq_(len(self.cards), 4)

    def should_extract_loyalty(self):
        eq_(self.sorin_markov.loyalty, u'4')

    def should_extract_type(self):
        eq_(self.sorin_markov.types, ['Planeswalker'])
        eq_(self.sorin_markov.subtypes, ['Sorin'])

    def should_extract_printings(self):
        eq_(self.sorin_markov.printings,
            [('Magic 2012', 'Mythic Rare'), ('Zendikar', 'Mythic Rare')])


class WhenExtractingFractionalNumbers(object):

    def setup(self):
        extractor = CardExtractor(card_html('donkey'))
        self.cards = extractor.extract_many()
        self.assquatch = self.cards[0]
        self.bad_ass = self.cards[1]
        self.cheap_ass = self.cards[2]

    def should_get_fractional_power_and_toughness(self):
        eq_(self.assquatch.power, '3{1/2}')
        eq_(self.assquatch.toughness, '3{1/2}')

    def should_get_fractional_power(self):
        eq_(self.bad_ass.power, '3{1/2}')
        eq_(self.bad_ass.toughness, '1')

    def should_get_fractional_toughness(self):
        eq_(self.cheap_ass.power, '1')
        eq_(self.cheap_ass.toughness, '3{1/2}')


class WhenExtractingMultipleCards(object):

    def setup(self):
        self.html = card_html('hex')
        self.cards = CardExtractor(self.html).extract_many()
        self.hexhunter = self.cards[1]
        self.hex_ = self.cards[2]
        self.hexmage = self.cards[8]

    def should_get_nine_results(self):
        eq_(len(self.cards), 10)

    def should_extract_name(self):
        eq_(self.hexhunter.name, 'Elvish Hexhunter')

    def should_extract_mana_cost(self):
        eq_(self.hexhunter.mana_cost, '(G/W)')

    def should_extract_multipart_mana_cost(self):
        eq_(self.hex_.mana_cost, '4BB')

    def should_extract_types(self):
        eq_(self.hexhunter.types, ['Creature'])
        eq_(self.hexhunter.subtypes, ['Elf', 'Shaman'])

    def should_extract_power(self):
        eq_(self.hexhunter.power, '1')

    def should_extract_toughness(self):
        eq_(self.hexhunter.toughness, '1')

    def should_extract_rules_text(self):
        eq_(self.hexhunter.rules_text, '{(g/w)}, {T}, Sacrifice Elvish Hexhunter'
            ': Destroy target enchantment.')

    def should_extract_multipart_card_text(self):
        eq_(self.hexmage.rules_text, "First strike\nSacrifice Vampire Hexmage"
            ": Remove all counters from target permanent.")

    def should_extract_printings(self):
        eq_(self.hexhunter.printings, [('Shadowmoor', 'Common')])

    def should_extract_multiple_card_expansions(self):
        eq_(self.hex_.printings,
            [('Magic: The Gathering-Commander', 'Rare'),
             ('Ravnica: City of Guilds', 'Rare')])


class WhenExtractingFlavorText(object):

    def setup(self):
        self.html = card_html('mirari')
        self.cards = CardExtractor(self.html).extract()

    def should_format_flavor_text(self):
        eq_(self.cards[0].flavor_text,
            u'"It offers you what you want, not what you need."\n—Braids, dementia summoner')


class WhenExtractingRulings(object):

    def setup(self):
        self.html = card_html('mirari')
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
        eq_(Symbol('Snow').textbox, '{S}')

    def should_format_x(self):
        eq_(Symbol('Variable Colorless').short, 'X')

    def should_format_hybrid_colorless_mana(self):
        eq_(Symbol('Two or White').short, '(2/W)')

    def should_format_half_mana(self):
        eq_(Symbol('Half a Red').textbox, '{Half R}')

    def should_format_infinite(self):
        eq_(Symbol('Infinite').textbox, u'{∞}')

    def should_format_little_girl_mana_cost(self):
        # As far as I can tell, this is a bug in Gatherer affecting
        # one card: Little Girl.
        eq_(Symbol('500').short, '(Half W)')
