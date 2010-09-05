Console-based access to the Gatherer Magic Card Database.

Usage: %prog [options] [cardname]

Examples:

    Look up a card by name:
    $ mtg.py sengir vampire

    Limit by color:
    $ mtg.py thrull --color=w

    Limit by card text, including reminder text.  This searches cards
    containing all terms, not the exact phrase:
    $ mtg.py --text='flying,islandwalk'
    
    To search by exact phrase, double quotes are necessary:
    $ mtg.py --text='"destroy all creatures"'

    Limit by card type:
    $ mtg.py --text='"destroy all creatures"' --type=instant

    Limit by subtype and rarity:
    $ mtg.py --type=goblin --rarity=m

    To limit by power, toughness, or converted mana cost, use the >,
    <, and = operators as follows.  Some shells require these
    characters to be escaped or enclosed in quotation marks.
    
    Creatures with power greater than 11:
    $ mtg.py --power='>11'

    Creatures power/toughness = 7/3:
    $ mtg.py --power='=7' --tough='=3'

    Enchantments costing less than 2 mana that give something -1/-1:
    $ mtg.py --cmc='<2' --text='-1/-1' --type=enchantment  

    It is possible to combine or negate characteristics using the OR
    (|) and NOT (!) operators.  Commas are used to delimit options.
    Examples:

    $ mtg.py zendikon --color='!b'
    $ mtg.py --type='legendary artifact' --subtype='!equipment'
    $ mtg.py --text='"win the game"' --set='!unhinged,!unglued' 
    $ mtg.py guildmage --color='|r,|g' 
    $ mtg.py --text='gain life' --set='|zendikar,|worldwake' --color='!g,!w'
    $ mtg.py --text='"counter target"' --color='!u,!b,!r'