base_url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
            '?action=advanced&')

random_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random'

TYPES = set([
    'artifact',
    'basic',
    'conspiracy',
    'creature',
    'enchantment',
    'instant',
    'land',
    'legendary',
    'ongoing',
    'phenomenon',
    'plane',
    'planeswalker',
    'scheme',
    'snow',
    'sorcery',
    'tribal',
    'vanguard',
    'world',
])

# Types that require "special = True" to show any cards
SPECIAL_TYPES = set([
    'conspiracy',
    'phenomenon',
    'plane',
    'ongoing',
    'scheme',
])

COLORS = {'w': 'W', 'u': 'U', 'b': 'B', 'r': 'R', 'g': 'G', 'c': 'C'}

COLOR_PROPER_NAMES = {
    'white': 'w',
    'blue': 'u',
    'black': 'b',
    'red': 'r',
    'green': 'g',
    'colorless': 'c',
    'boros': 'rw',
    'golgari': 'bg',
    'selesnya': 'wg',
    'dimir': 'ub',
    'orzhov': 'wb',
    'izzet': 'ur',
    'gruul': 'rg',
    'azorius': 'uw',
    'rakdos': 'br',
    'simic': 'ug',
    'bant': 'wug',
    'esper': 'ubw',
    'grixis': 'bru',
    'jund': 'rbg',
    'naya': 'wrg',
    'abzan': 'wbg',
    'jeskai': 'urw',
    'sultai': 'bgu',
    'mardu': 'rwb',
    'temur': 'gur',
}

RARITY_PATTERN = r'(.*?) ((Unc|C)ommon|(Mythic )?Rare|Special|Promo|Land)$'

RARITIES = {
    'c': 'C',
    'common': 'C',
    'u': 'U',
    'uncommon': 'U',
    'r': 'R',
    'rare': 'R',
    'mythic': 'M',
    'm': 'M',
    'l': 'L',
    'land': 'L',
    's': 'S',
    'special': 'S',
    'p': 'P',
    'promo': 'P',
}

VALID_WORDS = {'rarity': RARITIES, 'color': COLORS}

separator = '\n------------------------------'

readme = """Usage: %prog [options] [cardname]

Examples:

    Look up a card by name:
    $ mtg sengir vampire

    Limit by color.  Use the one-letter abbreviations: w, u, b, r, g, or c.
    $ mtg thrull --color=w

    To match multiple colors, combine letters.  How you separate them
    determines the type of search.

    Search for angels that are white OR black:
    $ mtg angel --color=w|b

    Search for angels that are white AND black (no comma separation
    forces multicolored matches).
    $ mtg angel --color=wb

    Exclude unselected colors with -x.  Search for angels that are black only.
    $ mtg angel --color=b -x

    Limit by card text, including reminder text.  A string of comma
    separated terms searches cards containing all terms, not the exact
    phrase:
    $ mtg --text=flying,islandwalk

    To search by exact phrase, specify the phrase:
    $ mtg --text='destroy all creatures'

    Limiting by type is done with the --type option.  This option will
    accept anything: card types, creature types, supertypes, etc.  For
    example:

    Limit by card type:
    $ mtg --text='destroy all creatures' --type=instant

    Limit by creature type and rarity:
    $ mtg --type=goblin --rarity=m

    Limit by supertype and two possible subtypes:
    $ mtg --type='snow,construct|goblin'

    Limit by subtype and card type:
    $ mtg --type='elf,!creature'

    To limit by power, toughness, or converted mana cost, you can use
    the inequality operators > and < as follows.  Some shells require
    these characters to be escaped or enclosed in quotation marks.

    Creatures with power greater than 11:
    $ mtg --power='>11'

    Creatures power/toughness = 7/3:
    $ mtg --power=7 --tough=3

    Enchantments costing less than 2 mana that give something -1/-1:
    $ mtg --cmc='<2' --text='-1/-1' --type=enchantment

    It is possible to combine or negate characteristics using the OR
    (|) and NOT (!) operators.  Commas are used to delimit options.
    Examples:

    $ mtg zendikon --color='!b'
    $ mtg --type='legendary,artifact,!equipment'
    $ mtg --text='win the game' --set='!unhinged,!unglued'
    $ mtg guildmage --color=r|g
    $ mtg --text='gain life' --set=zendikar --color="u|b|r" -x
    $ mtg --text='counter target' --color="w|g" -x
"""
