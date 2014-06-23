"""Request to the Gatherer site"""
import re
from collections import Iterable

from mtglib.constants import base_url, TYPES, SPECIAL_TYPES, VALID_WORDS, COLOR_PROPER_NAMES
from mtglib.functions import is_string

__all__ = ['SearchRequest', 'CardRequest']


# linearize nested lists
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not is_string(el):
            for sub in flatten(el):
                yield sub
        else:
            yield el

# flatten a nested list of SearchKeywords and mark as boolean OR.
def or_(l, r):
    lst = list(flatten([l, r]))
    for keyword in lst:
        keyword.boolean = 'or'
    return lst


class SearchKeyword(object):
    """Represents a word of phrase and its associated search operators."""

    def __init__(self, term, boolean='and', comparison=None):
        self.term = term
        self.boolean = boolean
        self.comparison = comparison

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return '<SearchKeyword {0} bool="{1}" comp="{2}">'.format(
            self.term, self.boolean, self.comparison)

    def render_term(self):
        if is_string(self.term) and ' ' in self.term:
            return '"{0}"'.format(self.term)
        else:
            return self.term

    def render_comparison(self):
        if self.comparison:
            return self.comparison
        else:
            return ''

    def render_boolean(self):
        if self.boolean == 'and':
            return '+'
        elif self.boolean == 'not':
            return '+!'
        elif self.boolean == 'or':
            return '|'
        else: return ''

    def url_fragment(self):
        return '{1}{2}[{0}]'.format(self.render_term(), self.render_boolean(),
                                    self.render_comparison())


class SearchFilter(object):
    """Atomic search structure: card attribute and search words."""

    def __init__(self, name, keywords=[], exclude_others=False):
        self.name = name
        self.keywords = keywords
        self.exclude_others = exclude_others

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def normalize_words(self, words):
        valid_words = VALID_WORDS.get(self.name)
        for word in words:
            if valid_words.get(word.term.lower(), False):
                word.term = valid_words.get(word.term.lower(), False)
            else:
                raise ValueError(
                    '"{}" is not a valid {}'.format(word.term, self.name))
        return words

    def normalize_digits(self, words):
        for word in words:
            if not word.comparison:
                word.comparison = '='
            if word.term.isdigit():
                word.term = int(word.term)
            else:
                raise ValueError('"{}" not a valid number'.format(word.term))
        return words

    def add_keywords(self, words):
        if self.name == 'color' or self.name == 'rarity':
            words = self.normalize_words(words)
        elif self.name in ('cmc', 'power', 'tough'):
            words = self.normalize_digits(words)
        self.keywords.extend(words)

    def url_fragment(self):
        if self.exclude_others:
            url_format = '{name}=+@({keywords})'
        else:
            url_format = '{name}={keywords}'
        keywords = ''
        for word in self.keywords:
            keywords += word.url_fragment()
        return url_format.format(name=self.name, keywords=keywords)


class Lexer(object):
    """Class for applying a grammar to user input."""

    def __init__(self, rules):
        self.rules = rules

        i = 1
        regex_parts = []
        self.group_type = {}
        for regex, type_ in rules:
            groupname = 'GROUP{0}'.format(i)
            self.group_type[groupname] = type_
            regex_parts.append('(?P<{0}>{1})'.format(groupname, regex))
            i += 1
        self.regex = re.compile('|'.join(regex_parts))

    def tokenize(self, text):
        mp = self.regex.scanner(text)
        while 1:
            m = mp.match()
            if not m:
                yield None, None
                break
            else:
                yield self.group_type[m.lastgroup], m.group(m.lastindex)


class ConditionParser(object):
    """Rules for parsing user input."""

    def __init__(self, data):
        self.data = data

        self.special_rules = {
            'freeform': ('[^<>=!\|,]+', 'TEXT'),
            'numeric': ('\d+', 'NUMBER'),
            'single_character': ('[^<>=!\|,]', 'COLOR')}

        self.base_rules = [
            ('[<>=]+', 'COMPARISON'),
            ('\|', 'OR'),
            ('!', 'NOT'),
            (',', 'SEPARATOR')
        ]
        self.lexers = {}

    def getlexer(self, text_type):
        if not self.lexers.get(text_type):
            rules = [self.special_rules[text_type]] + self.base_rules
            self.lexers[text_type] = Lexer(rules)
        return self.lexers.get(text_type)

    def preprocess_color(self, value):
        if COLOR_PROPER_NAMES.get(value.lower(), False):
            return COLOR_PROPER_NAMES.get(value.lower(), False)
        return value


    def get_conditions(self):
        conditions = {}
        for name, value in self.data.items():
            if not is_string(value):
                continue
            if name == 'color':
                value = self.preprocess_color(value)
                self.lexer = self.getlexer('single_character')
            else:
                self.lexer = self.getlexer('freeform')
            fl = SearchFilter(name, keywords=[])
            fl.add_keywords(self.parse(value))
            conditions[fl.name] = fl
        return conditions

    def expr(self, token_stream, token):
        """Top level parsing function.

        An expression is <keyword> <OR> <expr>
        or               <keyword> <SEP> <expr>
        or               <keyword>

        """
        lval = self.keyword(token_stream, token, {})
        token = next(token_stream)
        if token[0] == 'OR':
            op = or_
            token = next(token_stream)
        elif token[0] == 'TEXT' or token[0] == 'COLOR':
            op = lambda l, r: list(flatten([l, r]))
        elif token[0] == 'SEPARATOR':
            op = lambda l, r: list(flatten([l, r]))
            token = next(token_stream)
        else:
            return [lval]
        rval = self.expr(token_stream, token)
        return op(lval, rval)

    def keyword(self, token_stream, token, operators):
        """Lowest level parsing function.

        A keyword consists of zero or more prefix operators (NOT, or
        COMPARISON) followed by a TEXT, COLOR, or NUMBER block.

        """
        if token[0] == 'TEXT' or token[0] == 'COLOR':
            return SearchKeyword(token[1], **operators)
        elif token[0] == 'COMPARISON':
            operators['comparison'] = token[1]
        elif token[0] == 'NOT':
            operators['boolean'] = 'not'
        else:
            if token[1] == None:
                problem = 'end of input.'
            else:
                problem = 'token {0} in input'.format(token[1])
            raise SyntaxError('Unexpected {0}'.format(problem))
        token = next(token_stream)
        return self.keyword(token_stream, token, operators)

    def parse(self, text):
        """Parse the given text, return a list of Keywords."""
        token_stream = self.lexer.tokenize(text)
        return self.expr(token_stream, next(token_stream))


class SearchRequest(object):
    """A complete search request that can be sent to Gatherer.

    Takes user-supplied options, then formulates a URL from those
    options.  This url will have the results of the search.

    """

    def __init__(self, options, special=False, exclude_others=set()):
        self.options = options
        self.special = special
        self.exclude_others = exclude_others

    def get_filters(self):
        conditions = ConditionParser(self.options).get_conditions()
        if conditions.get('type', False):
            keywords = conditions['type'].keywords
            exclude = 'type' in self.exclude_others
            type_words = [w for w in keywords if w.term.lower() in TYPES]
            subtype_words = [w for w in keywords if w.term.lower() not in TYPES]

            # If one of our types is in SPECIAL_TYPES, override the special setting
            for type_word in type_words:
                if type_word.term.lower() in SPECIAL_TYPES:
                    self.special = True
                    break

            del conditions['type']
            if type_words:
                conditions['type'] = SearchFilter('type', keywords=type_words, exclude_others=exclude)
            if subtype_words:
                conditions['subtype'] = SearchFilter('subtype', keywords=subtype_words, exclude_others=exclude)
        if conditions.get('color', False) and 'color' in self.exclude_others:
            conditions['color'].exclude_others = True
        return conditions

    @property
    def special_fragment(self):
        return self.special and '&special=true' or ''

    @property
    def url(self):
        return (base_url +
                '&'.join([fl.url_fragment() for fl in self.get_filters().values()]) +
                self.special_fragment)
