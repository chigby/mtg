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
        assert self.conditions[0].name == 'text'

    def should_assume_boolean_and(self):
        assert self.conditions[0].keywords[0].boolean == 'and'

    def should_assume_no_comparison(self):
        assert self.conditions[0].keywords[0].comparison is None


class WhenParsingCommaSeparatedKeywords(unittest.TestCase):

    def setUp(self):
        parser = ConditionParser({'text': 'exile,graveyard'})
        self.conditions = parser.get_conditions()

    def should_consider_as_separate_keywords(self):
        exile = SearchKeyword('exile', 'and')
        graveyard = SearchKeyword('graveyard', 'and')
        assert self.conditions[0].keywords == [exile, graveyard]

    def should_understand_pipe_as_logical_or(self):
        conditions = ConditionParser({'text': 'destroy|exile'}).get_conditions()
        assert conditions[0].keywords == [SearchKeyword('destroy', 'or'),
                                          SearchKeyword('exile', 'or')]

    def should_understand_bang_as_logical_not(self):
        conditions = ConditionParser({'text': 'return,!hand'}).get_conditions()
        assert conditions[0].keywords == [SearchKeyword('return', 'and'),
                                          SearchKeyword('hand', 'not')]


class WhenParsingNumbers(unittest.TestCase):

    def should_assume_equality_conditional(self):
        parser = ConditionParser({'cmc': '5'})
        cond = parser.get_conditions()
        assert cond[0].name == 'cmc'
        assert cond[0].keywords == [SearchKeyword(5, 'and', '=')]

    def should_understand_less_than_conditional(self):
        parser = ConditionParser({'power': '<5'})
        cond = parser.get_conditions()
        assert cond[0].name == 'power'
        self.assertEqual(cond[0].keywords, [SearchKeyword(5, 'and', '<')])

    def should_understand_multiple_conditionals(self):
        parser = ConditionParser({'power': '<5,>0'})
        cond = parser.get_conditions()
        assert cond[0].name == 'power'
        self.assertEqual(cond[0].keywords, [SearchKeyword(5, 'and', '<'),
                                            SearchKeyword(0, 'and', '>')])

    def should_understand_greater_than_conditional(self):
        parser = ConditionParser({'tough': '>3'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword(3, 'and', '>')])

    def should_understand_equality_conditional(self):
        parser = ConditionParser({'tough': '=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword(3, 'and', '=')])

    def should_understand_greater_than_or_equal_to(self):
        parser = ConditionParser({'tough': '>=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword(3, 'and', '>=')])

    def should_understand_less_than_or_equal_to(self):
        parser = ConditionParser({'tough': '<=3'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword(3, 'and', '<=')])

    def should_raise_error_for_non_numeric_input(self):
        parser = ConditionParser({'tough': 'f'})
        assert_raises(SyntaxError, parser.get_conditions)


class WhenParsingColors(unittest.TestCase):

    def should_assume_and_when_comma_separated(self):
        parser = ConditionParser({'color': 'w,u,g'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword('W', 'and'),
                                            SearchKeyword('U', 'and'),
                                            SearchKeyword('G', 'and')])

    def should_assume_and_when_adjacent(self):
        parser = ConditionParser({'color': 'wbg'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword('W', 'and'),
                                            SearchKeyword('B', 'and'),
                                            SearchKeyword('G', 'and')])

    def should_correctly_combine_not_and_and(self):
        parser = ConditionParser({'color': '!b,r'})
        cond = parser.get_conditions()
        self.assertEqual(cond[0].keywords, [SearchKeyword('B', 'not'),
                                            SearchKeyword('R', 'and')])

    def should_raise_error_for_non_color_input(self):
        parser = ConditionParser({'color': 'd'})
        assert_raises(SyntaxError, parser.get_conditions)


class WhenParsingPhrases(unittest.TestCase):

    def setUp(self):
        parser = ConditionParser({'text': 'first strike'})
        self.keywords = parser.get_conditions()[0].keywords

    def should_treat_space_separated_terms_as_single_phrase(self):
        assert self.keywords.pop() == SearchKeyword('first strike', 'and')


class WhenGettingUrl(unittest.TestCase):

    def should_group_text_in_brackets(self):
        word = SearchKeyword('trample', 'and')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+["trample"]')

    def should_assume_exact_quote_if_spaces(self):
        word = SearchKeyword('first strike', 'and')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+["first strike"]')

    def should_parse_logical_or(self):
        first = SearchKeyword('first', 'or')
        strike = SearchKeyword('strike', 'or')
        fl = SearchFilter('text', keywords=[first, strike])
        self.assertEqual(fl.url_fragment(), 'text=|["first"]|["strike"]')

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
        self.assertEqual(fl.url_fragment(), 'name=+["sengir"]+["vampire"]')

    def should_group_url_keywords_if_excluding_others(self):
        word = SearchKeyword('w', 'and')
        fl = SearchFilter('color', keywords=[word])
        fl.exclude_others = True
        self.assertEqual(fl.url_fragment(), 'color=+@(+["w"])')

    def should_render_not_operator(self):
        word = SearchKeyword('graveyard', 'not')
        fl = SearchFilter('text', keywords=[word])
        self.assertEqual(fl.url_fragment(), 'text=+!["graveyard"]')


class WhenMakingSearchRequest(unittest.TestCase):

    def should_recognize_creature_type_as_subtype(self):
        options = dict(type='dryad')
        request = SearchRequest(options)
        fl = SearchFilter('subtype', keywords=[SearchKeyword('dryad', 'and')])
        self.assertEqual(request.get_filters(), [fl])

    def should_separate_type_and_subtypes(self):
        options = dict(type='land,dryad')
        request = SearchRequest(options)
        subt = SearchFilter('subtype', keywords=[SearchKeyword('dryad', 'and')])
        type_ = SearchFilter('type', keywords=[SearchKeyword('land', 'and')])
        self.assertEqual(request.get_filters(), [type_, subt])

    def should_separate_many_types_with_not_modifier(self):
        options = dict(type='legendary,artifact,!equipment,!creature')
        request = SearchRequest(options)
        type_keywords = [SearchKeyword('legendary', 'and'),
                         SearchKeyword('artifact', 'and'),
                         SearchKeyword('creature', 'not')]
        subtype_keywords = [SearchKeyword('equipment', 'not')]
        subt = SearchFilter('subtype', keywords=subtype_keywords)
        type_ = SearchFilter('type', keywords=type_keywords)
        self.assertEqual(request.get_filters(), [type_, subt])

    def should_allow_color_exclusion(self):
        request = SearchRequest({'color': 'wu'}, exclude_other_colors=True)
        self.assertTrue(request.get_filters()[0].exclude_others)


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