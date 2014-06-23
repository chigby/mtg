import unittest
from nose.tools import assert_raises

from mtglib.gatherer_request import SearchRequest, ConditionParser, \
    SearchKeyword, SearchFilter


class WhenInstantiatingSearchRequest(unittest.TestCase):

    def setUp(self):
        self.request = SearchRequest({'text': 'first strike'})

    def should_be_instance_of_card_request(self):
        assert isinstance(self.request, SearchRequest)

    def should_store_options(self):
        assert self.request.options == {'text': 'first strike'}


class WhenParsingSimpleTextInput(unittest.TestCase):

    def setUp(self):
        parser = ConditionParser({'text': 'trample'})
        self.conditions = parser.get_conditions()

    def should_assign_filter_name(self):
        assert self.conditions['text'].name == 'text'

    def should_assume_boolean_and(self):
        assert self.conditions['text'].keywords[0].boolean == 'and'

    def should_assume_no_comparison(self):
        assert self.conditions['text'].keywords[0].comparison is None


class WhenParsingCommaSeparatedKeywords(unittest.TestCase):

    def setUp(self):
        parser = ConditionParser({'text': 'exile,graveyard'})
        self.conditions = parser.get_conditions()

    def should_consider_as_separate_keywords(self):
        exile = SearchKeyword('exile', 'and')
        graveyard = SearchKeyword('graveyard', 'and')
        assert self.conditions['text'].keywords == [exile, graveyard]

    def should_understand_pipe_as_logical_or(self):
        conditions = ConditionParser({'text': 'destroy|exile'}).get_conditions()
        assert conditions['text'].keywords == [SearchKeyword('destroy', 'or'),
                                               SearchKeyword('exile', 'or')]

    def should_understand_bang_as_logical_not(self):
        conditions = ConditionParser({'text': 'return,!hand'}).get_conditions()
        assert conditions['text'].keywords == [SearchKeyword('return', 'and'),
                                               SearchKeyword('hand', 'not')]


class WhenParsingNumbers(unittest.TestCase):

    def should_assume_equality_conditional(self):
        parser = ConditionParser({'cmc': '5'})
        cond = parser.get_conditions()
        assert cond['cmc'].name == 'cmc'
        self.assertEqual(cond['cmc'].keywords, [SearchKeyword(5, 'and', '=')])

    def should_understand_less_than_conditional(self):
        parser = ConditionParser({'power': '<5'})
        cond = parser.get_conditions()
        assert cond['power'].name == 'power'
        self.assertEqual(cond['power'].keywords, [SearchKeyword(5, 'and', '<')])

    def should_understand_multiple_conditionals(self):
        parser = ConditionParser({'power': '<5,>0'})
        cond = parser.get_conditions()
        assert cond['power'].name == 'power'
        self.assertEqual(cond['power'].keywords, [SearchKeyword(5, 'and', '<'),
                                                  SearchKeyword(0, 'and', '>')])

    def should_understand_greater_than_conditional(self):
        parser = ConditionParser({'tough': '>3'})
        cond = parser.get_conditions()
        self.assertEqual(cond['tough'].keywords, [SearchKeyword(3, 'and', '>')])

    def should_understand_equality_conditional(self):
        parser = ConditionParser({'tough': '=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond['tough'].keywords, [SearchKeyword(3, 'and', '=')])

    def should_understand_greater_than_or_equal_to(self):
        parser = ConditionParser({'tough': '>=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond['tough'].keywords, [SearchKeyword(3, 'and', '>=')])

    def should_understand_less_than_or_equal_to(self):
        parser = ConditionParser({'tough': '<=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond['tough'].keywords, [SearchKeyword(3, 'and', '<=')])

    def should_raise_error_for_non_numeric_input(self):
        parser = ConditionParser({'tough': 'f'})
        assert_raises(ValueError, parser.get_conditions)


class WhenParsingColors(unittest.TestCase):

    def should_assume_and_when_comma_separated(self):
        parser = ConditionParser({'color': 'w,u,g'})
        cond = parser.get_conditions()
        self.assertEqual(cond['color'].keywords, [SearchKeyword('W', 'and'),
                                                  SearchKeyword('U', 'and'),
                                                  SearchKeyword('G', 'and')])

    def should_assume_and_when_adjacent(self):
        parser = ConditionParser({'color': 'wbg'})
        cond = parser.get_conditions()
        self.assertEqual(cond['color'].keywords, [SearchKeyword('W', 'and'),
                                                  SearchKeyword('B', 'and'),
                                                  SearchKeyword('G', 'and')])

    def should_correctly_combine_not_and_and(self):
        parser = ConditionParser({'color': '!b,r'})
        cond = parser.get_conditions()
        self.assertEqual(cond['color'].keywords, [SearchKeyword('B', 'not'),
                                                  SearchKeyword('R', 'and')])

    def should_convert_guild_to_colors(self):
        parser = ConditionParser({'color': 'dimir'})
        cond = parser.get_conditions()
        self.assertEqual(cond['color'].keywords, [SearchKeyword('U', 'and'),
                                                  SearchKeyword('B', 'and')])

    def should_convert_shard_to_colors(self):
        parser = ConditionParser({'color': 'grixis'})
        cond = parser.get_conditions()
        self.assertEqual(cond['color'].keywords, [SearchKeyword('B', 'and'),
                                                  SearchKeyword('R', 'and'),
                                                  SearchKeyword('U', 'and')])

    def should_raise_error_for_non_color_input(self):
        parser = ConditionParser({'color': 'd'})
        assert_raises(ValueError, parser.get_conditions)

class WhenParsingRarities(unittest.TestCase):

    def should_upcase_keyword(self):
        parser = ConditionParser({'rarity': 's'})
        cond = parser.get_conditions()
        self.assertEqual(cond['rarity'].keywords, [SearchKeyword('S', 'and')])

    def should_raise_error_if_invalid_rarity(self):
        parser = ConditionParser({'rarity': 'd'})
        assert_raises(ValueError, parser.get_conditions)

    def should_accept_complete_words(self):
        parser = ConditionParser({'rarity': 'special'})
        cond = parser.get_conditions()
        self.assertEqual(cond['rarity'].keywords, [SearchKeyword('S', 'and')])

class WhenParsingPhrases(unittest.TestCase):

    def setUp(self):
        parser = ConditionParser({'text': 'first strike'})
        self.keywords = parser.get_conditions()['text'].keywords

    def should_treat_space_separated_terms_as_single_phrase(self):
        assert self.keywords[0] == SearchKeyword('first strike', 'and')


class WhenGettingUrl(unittest.TestCase):

    def should_group_text_in_brackets(self):
        word = SearchKeyword('trample', 'and')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+[trample]')

    def should_assume_exact_quote_if_spaces(self):
        word = SearchKeyword('first strike', 'and')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+["first strike"]')

    def should_parse_logical_or(self):
        first = SearchKeyword('first', 'or')
        strike = SearchKeyword('strike', 'or')
        fl = SearchFilter('text', keywords=[first, strike])
        self.assertEqual(fl.url_fragment(), 'text=|[first]|[strike]')

    def should_render_greater_than_comparison(self):
        word = SearchKeyword(5, 'and', '>')
        fl = SearchFilter('power', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'power=+>[5]')

    def should_render_less_then_comparison(self):
        word = SearchKeyword(5, 'and', '<')
        fl = SearchFilter('power', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'power=+<[5]')

    def should_render_greater_than_or_equal_to_comparison(self):
        word = SearchKeyword(5, 'and', '>=')
        fl = SearchFilter('power', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'power=+>=[5]')

    def should_render_less_than_or_equal_to_comparison(self):
        word = SearchKeyword(5, 'and', '<=')
        fl = SearchFilter('power', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'power=+<=[5]')

    def should_render_equality_comparison(self):
        word = SearchKeyword(5, 'and', '=')
        fl = SearchFilter('power', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'power=+=[5]')

    def should_separate_and_words(self):
        sengir = SearchKeyword('sengir', 'and')
        vampire = SearchKeyword('vampire', 'and')
        fl = SearchFilter('name', keywords=[sengir, vampire])
        self.assertEqual(fl.url_fragment(), 'name=+[sengir]+[vampire]')

    def should_group_url_keywords_if_excluding_others(self):
        word = SearchKeyword('w', 'and')
        fl = SearchFilter('color', keywords=[word])
        fl.exclude_others = True
        self.assertEqual(fl.url_fragment(), 'color=+@(+[w])')

    def should_group_url_keywords_if_excluding_other_types(self):
        word = SearchKeyword('goblin', 'and')
        fl = SearchFilter('type', keywords=[word])
        fl.exclude_others = True
        self.assertEqual(fl.url_fragment(), 'type=+@(+[goblin])')

    def should_not_quote_rarities(self):
        word = SearchKeyword('M', 'and')
        fl = SearchFilter('rarity', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'rarity=+[M]')

    def should_render_not_operator(self):
        word = SearchKeyword('graveyard', 'not')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+![graveyard]')


class WhenMakingSearchRequest(unittest.TestCase):

    def should_recognize_creature_type_as_subtype(self):
        options = dict(type='dryad')
        request = SearchRequest(options)
        fl = SearchFilter('subtype', keywords=[SearchKeyword('dryad', 'and')])
        self.assertEqual(request.get_filters(), {'subtype': fl})

    def should_separate_type_and_subtypes(self):
        options = dict(type='land,dryad')
        request = SearchRequest(options)
        subt = SearchFilter('subtype', keywords=[SearchKeyword('dryad', 'and')])
        type_ = SearchFilter('type', keywords=[SearchKeyword('land', 'and')])
        self.assertEqual(request.get_filters(), {'type':type_,
                                                 'subtype': subt})

    def should_separate_many_types_with_not_modifier(self):
        options = dict(type='legendary,artifact,!equipment,!creature')
        request = SearchRequest(options)
        type_keywords = [SearchKeyword('legendary', 'and'),
                         SearchKeyword('artifact', 'and'),
                         SearchKeyword('creature', 'not')]
        subtype_keywords = [SearchKeyword('equipment', 'not')]
        subt = SearchFilter('subtype', keywords=subtype_keywords)
        type_ = SearchFilter('type', keywords=type_keywords)
        self.assertEqual(request.get_filters(), {'type': type_,
                                                 'subtype': subt})

    def should_allow_color_exclusion(self):
        request = SearchRequest({'color': 'wu'}, exclude_others=['color'])
        self.assertTrue(request.get_filters()['color'].exclude_others)

    def should_allow_type_exclusion(self):
        request = SearchRequest({'type': 'elemental'}, exclude_others=['type'])
        self.assertTrue(request.get_filters()['subtype'].exclude_others)

    def should_allow_type_and_subtype_exclusion(self):
        request = SearchRequest({'type': 'dryad,creature'}, exclude_others=['type'])
        self.assertTrue(request.get_filters()['type'].exclude_others)
        self.assertTrue(request.get_filters()['subtype'].exclude_others)


class WhenMakingSpecialRequest(unittest.TestCase):

    def setUp(self):
        self.request = SearchRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)

    def should_have_special(self):
        assert self.request.special == True

    def should_have_special_fragment(self):
        assert self.request.special_fragment == '&special=true'

    def should_include_special_option_in_url(self):
        request = SearchRequest({'name': 'only,blood,ends,your,nightmares'},
                              special=True)
        assert request.special_fragment in request.url

    def should_assume_special_if_looking_for_a_special_type(self):
        request = SearchRequest({'type': 'plane'})
        self.assertIn('&special=true', request.url)
