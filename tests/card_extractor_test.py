# -*- coding: utf-8 -*-
import re
import textwrap

from dingus import DingusTestCase, Dingus, returner
from nose.tools import assert_raises, eq_

import mtglib.card_extractor as mod
from mtglib.gatherer_request import CardRequest
from mtglib.card_extractor import CardExtractor, SingleCardExtractor, Card

class WhenInstantiatingCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_html(self):
        assert hasattr(self.extractor, 'html')


class WhenExtractingSingleCard(object):

    def setup(self):
        self.html = open('tests/_data/acorn_harvest.html')
        self.extractor = CardExtractor(self.html)
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


class WhenExtractingSingleDualFacedPlaneswalker(object):

    def setup(self):
        self.html = open('tests/_data/garruk_relentless.html')
        self.cards = CardExtractor(self.html).extract()

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
        eq_(self.cards[0].name, 'Elvish Hexhunter')

    def should_extract_mana_cost(self):
        eq_(self.cards[0].mana_cost, '(G/W)')

    def should_extract_types(self):
        eq_(self.cards[0].types, unicode('Creature  — Elf Shaman', 'utf-8'))

    def should_extract_power_toughness_block(self):
        eq_(self.cards[0].pow_tgh, '(1/1)')

    def should_extract_card_text(self):
        eq_(self.cards[0].card_text, '{(g/w)}, {T}, Sacrifice Elvish Hexhunter'
            ': Destroy target enchantment.')

    def should_extract_card_expansion(self):
        eq_(self.cards[0].set_rarity, 'Shadowmoor (Common)')

# class WhenExtractingCardsWithBlankLines(DingusTestCase(CardExtractor)):

#     def setup(self):
#         super(WhenExtractingCardsWithBlankLines, self).setup()
#         self.extractor = CardExtractor('<html></html>')
#         self.table = mod.BeautifulSoup.BeautifulSoup().table
#         self.table.findAll.return_value = [Dingus()] * 13
#         all_tags = []
#         for i in range(26):
#             tag = Dingus()
#             tag.contents = [Dingus()] * 3
#             tag['href'] = 'http://www.com'
#             if i % 2 != 0:
#                 for contents in tag.contents:
#                     contents.string = u'\r\n string\r\n'
#             else:
#                 all_contents = []
#                 for i in range(3):
#                     contents = Dingus()
#                     if i == 1:
#                         contents.string = u'||'
#                     else:
#                         contents.string = u'\n'
#                     all_contents.append(contents)
#                 tag.contents = all_contents
#             all_tags.append(tag)
#         self.table.findAll.return_value = all_tags
#         self.extracted = self.extractor.extract()


# class WhenExtractingCards(DingusTestCase(CardExtractor)):

#     def setup(self):
#         super(WhenExtractingCards, self).setup()
#         self.extractor = CardExtractor('<html></html>')
#         self.table = mod.BeautifulSoup.BeautifulSoup().table
#         self.table.findAll.return_value = [Dingus()] * 13
#         for tag in self.table.findAll():
#             tag.contents = [Dingus()] * 3
#             tag['href'] = 'http://www.com'
#             for contents in tag.contents:
#                 contents.string = u'\r\n string\r\n'
#         self.extracted = self.extractor.extract()

#     def should_be_false_if_empty(self):
#         assert not CardExtractor('').extract()

#     def should_get_card_urls_if_asked(self):
#         self.extractor.extract(get_card_urls=True)
#         assert mod.BeautifulSoup.BeautifulSoup().table.calls('findAll', 'a')

#     def should_parse_html(self):
#         assert mod.BeautifulSoup.calls('BeautifulSoup', '<html></html>').once()

#     def should_raise_exception_if_bad_format(self):
#         mod.BeautifulSoup.BeautifulSoup().table = False
#         assert CardExtractor('<html></html>').extract() == []

#     def should_replace_br_tags_with_pipes(self):
#         soup = mod.BeautifulSoup.BeautifulSoup()
#         for tag in soup.findAll():
#             assert tag.calls('replaceWith', '||')
#         assert soup.calls('findAll', 'br').once()

#     def should_find_all_td_tags(self):
#         assert self.table.calls('findAll', 'td').once()


# class WhenExtractingManyCards(DingusTestCase(CardExtractor,
#                                              exclude=['BeautifulSoup', 're', 'Card'])):

#     def setup(self):
#         super(WhenExtractingManyCards, self).setup()
#         self.extractor = CardExtractor(fork_html)

#     def should_return_list_of_cards(self):
#         for card in self.extractor.extract():
#             assert isinstance(card, Card)

#     def should_get_card_urls(self):
#         for card in self.extractor.extract(get_card_urls=True):
#             assert card.url

#     def should_return_correct_cards(self):
#         cards = self.extractor.extract()
#         assert cards[0].name == 'Fork'
#         assert cards[0].type == 'Instant'
#         assert cards[1].name == 'Forked Bolt'
#         assert cards[1].type == 'Sorcery'
#         assert cards[2].name == 'Forked Lightning'
#         assert cards[2].type == 'Sorcery'
#         assert cards[3].name == 'Forked-Branch Garami'

#     def should_return_correct_cards(self):
#         cards = self.extractor.extract(get_card_urls=True)
#         assert cards[0].name == 'Fork'
#         assert cards[0].type == 'Instant'
#         assert cards[1].name == 'Forked Bolt'
#         assert cards[1].type == 'Sorcery'
#         assert cards[2].name == 'Forked Lightning'
#         assert cards[2].type == 'Sorcery'
#         assert cards[3].name == 'Forked-Branch Garami'


# class WhenExtractingCardsWithoutManaCosts(
#     DingusTestCase(CardExtractor, exclude=['re', 'Card', 'BeautifulSoup'])):

#     def setup(self):
#         super(WhenExtractingCardsWithoutManaCosts, self).setup()
#         self.extractor = CardExtractor(costless_html)
#         self.card = self.extractor.extract()[1]

#     def should_extract_blank_mana_cost(self):
#         eq_(self.card.cost, '')

#     def should_extract_rules_text(self):
#         eq_(self.card.rules_text, u'Suspend 4—{U} (Rather than cast this card '
#             'from your hand, pay {U} and exile it with four time counters on '
#             'it. At the beginning of your upkeep, remove a time counter. When'
#             ' the last is removed, cast it without paying its mana cost.) '
#             '; Target player draws three cards.')

#     def should_extract_sets_and_rarity(self):
#         eq_(self.card.set_rarity, 'Duel Decks: Jace vs. Chandra Rare, '
#             'Time Spiral Rare')



# class DescribeSingleCardExtractor(object):

#     def should_accept_html(self):
#         self.extractor = SingleCardExtractor('<html></html>')
#         assert self.extractor.html == '<html></html>'

#     def should_replace_autocard_tags_with_its_content(self):
#         self.extractor = SingleCardExtractor('<html></html>')
#         self.extractor.extract()
#         for tag in mod.BeautifulSoup.BeautifulSoup().findAll():
#             assert tag.calls('replaceWith', tag.string)


# class WhenExtractingRulings(DingusTestCase(SingleCardExtractor)):

#     def setup(self):
#         super(WhenExtractingRulings, self).setup()
#         self.extractor = SingleCardExtractor('<html></html>')
#         self.soup = mod.BeautifulSoup.BeautifulSoup()

#         def compile_(string):
#             return string
#         mod.re.compile = compile_

#         def findAll(attrs):
#             all_tags = [Dingus()] *3
#             for tag in all_tags:
#                 if attrs == 'autocard':
#                     tag.string = 'autocard'
#                 elif 'rulingText$' in attrs.values():
#                     tag.contents = 'This is a ruling'
#                 elif 'rulingDate$' in attrs.values():
#                     tag.contents = '2010-08-23'
#             return all_tags
#         self.soup.findAll = findAll
#         self.extracted = self.extractor.extract()

#     def should_return_false_if_no_html(self):
#         self.extractor = SingleCardExtractor('')
#         assert self.extractor.extract() == False

#     def should_parse_html(self):
#         assert mod.BeautifulSoup.calls('BeautifulSoup', '<html></html>').once()

#     def should_combine_ruling_contents(self):
#         print self.extracted
#         assert self.extracted == [('2010-08-23', 'This is a ruling'),
#                                   ('2010-08-23', 'This is a ruling'),
#                                   ('2010-08-23', 'This is a ruling')]


# fork_html = """
# <div class="textspoiler">
#     <table>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl00_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=1294">Fork</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl00_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>
#                         RR
#                     </td>
# </tr>

#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Instant
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>

#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Copy target instant or sorcery spell, except that the copy is red. You may choose new targets for the copy.
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Revised Edition Rare, Unlimited Edition Rare, Limited Edition Beta Rare, Limited Edition Alpha Rare
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl01_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=193512">Forked Bolt</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl01_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>
#                         R
#                     </td>
# </tr>

#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Sorcery
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>

#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Forked Bolt deals 2 damage divided as you choose among one or two target creatures and/or players.
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Rise of the Eldrazi Uncommon
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl02_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=201292">Forked Lightning</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl02_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>
#                         3R
#                     </td>
# </tr>

#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Sorcery
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>

#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Forked Lightning deals 4 damage divided as you choose among one, two, or three target creatures.
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Masters Edition III Uncommon, Portal Rare
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl03_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=74410">Forked-Branch Garami</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl03_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>
#                         3GG
#                     </td>
# </tr>

#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Creature  — Spirit
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>
#                         (4/4)
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Soulshift 4, soulshift 4 (When this is put into a graveyard from the battlefield, you may return up to two target Spirit cards with converted mana cost 4 or less from your graveyard to your hand.)
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Betrayers of Kamigawa Uncommon
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>

#     </table>
# </div>
# """

# costless_html = """
# <div class="textspoiler">
#     <table>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl00_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=122449">Aeon Chronicler</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl00_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>
#                         3UU
#                     </td>
# </tr>


#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Creature  — Avatar
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>
#                         (*/*)
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Aeon Chronicler's power and toughness are each equal to the number of cards in your hand.<br />
# Suspend X—{X}{3}{U}. X can't be 0.  (Rather than cast this card from your hand, you may pay {X}{3}{U} and exile it with X time counters on it. At the beginning of your upkeep, remove a time counter. When the last is removed, cast it without paying its mana cost. It has haste.)<br />
# Whenever a time counter is removed from Aeon Chronicler while it's exiled, draw a card.
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Planar Chaos Rare
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>

#                 <tr>
#                     <td>
#                         Name:
#                     </td>
#                     <td>
#                         <a id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl01_cardLink" class="nameLink" onclick="return CardLinkAction(event, this, 'SameWindow');" href="../Card/Details.aspx?multiverseid=189244">Ancestral Vision</a>
#                     </td>
#                 </tr>
#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl01_costRow">
#         <td>
#                         Cost:
#                     </td>
#         <td>

#                     </td>
# </tr>

#                 <tr id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_cardEntries_ctl01_colorIndicatorRow">
#         <td>
#                         Color:
#                     </td>
#         <td>
#                         Blue
#                     </td>
# </tr>

#                 <tr>
#                     <td>
#                         Type:
#                     </td>
#                     <td>
#                         Sorcery
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Pow/Tgh:
#                     </td>
#                     <td>

#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Rules Text:
#                     </td>
#                     <td>
#                         Suspend 4—{U} (Rather than cast this card from your hand, pay {U} and exile it with four time counters on it. At the beginning of your upkeep, remove a time counter. When the last is removed, cast it without paying its mana cost.)<br />
# Target player draws three cards.
#                     </td>
#                 </tr>
#                 <tr>
#                     <td>
#                         Set/Rarity:
#                     </td>
#                     <td>
#                         Duel Decks: Jace vs. Chandra Rare, Time Spiral Rare
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="2">
#                         <br />
#                     </td>
#                 </tr>
#     </table>
# </div>"""
