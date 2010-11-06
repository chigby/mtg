Console-based access to the Gatherer Magic Card Database.

Usage: %prog [options] [cardname]

Examples:

    Look up a card by name:
    $ mtg.py sengir vampire

    Limit by color:
    $ mtg.py thrull --color=w

    Limit by card text, including reminder text.  A string of comma
    separated terms searches cards containing all terms, not the exact
    phrase: 
    $ mtg.py --text='flying,islandwalk'
    
    To search by exact phrase, specify the phrase:
    $ mtg.py --text='destroy all creatures'

    Limiting by type is done with the --type option.  This option will
    accept anything: card types, creature types, supertypes, etc.  For
    example:

    Limit by card type:
    $ mtg.py --text='destroy all creatures' --type=instant

    Limit by creature type and rarity:
    $ mtg.py --type=goblin --rarity=m

    Limit by supertype and two possible subtypes:
    $ mtg.py --type='snow,|construct,|goblin'

    Limit by subtype and card type:
    $ mtg.py --type='elf,!creature'

    To limit by power, toughness, or converted mana cost, you can use
    the inequality operators > and < as follows.  Some shells require
    these characters to be escaped or enclosed in quotation marks.
    
    Creatures with power greater than 11:
    $ mtg.py --power='>11'

    Creatures power/toughness = 7/3:
    $ mtg.py --power=7 --tough=3

    Enchantments costing less than 2 mana that give something -1/-1:
    $ mtg.py --cmc='<2' --text='-1/-1' --type=enchantment  

    It is possible to combine or negate characteristics using the OR
    (|) and NOT (!) operators.  Commas are used to delimit options.
    Examples:

    $ mtg.py zendikon --color='!b'
    $ mtg.py --type='legendary,artifact,!equipment'
    $ mtg.py --text='win the game' --set='!unhinged,!unglued' 
    $ mtg.py guildmage --color='|r,|g' 
    $ mtg.py --text='gain life' --set='|zendikar,|worldwake' --color='!g,!w'
    $ mtg.py --text='counter target' --color='!u,!b,!r'
