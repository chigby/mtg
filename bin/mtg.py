#!/opt/local/bin/python
"""
Console-based access to the Gatherer Magic Card Database.

Usage: %prog [options] [cardname]
"""

import logging
import sys
from logging import handlers, Formatter
from optparse import OptionParser
from mtglib.gatherer_request import CardRequest
from mtglib.card_extractor import CardExtractor
from mtglib.card import Card

def main(args):

    # create logger
    logger = logging.getLogger('mtg')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.debug('Starting main program')

    parser = OptionParser(usage='Usage: %prog [options] [cardname]')
    parser.add_option("-t", "--text", dest="text",
                      help="containing rules text TEXT", metavar="TEXT")
    parser.add_option('--color', dest='color', help='cards matching COLOR (w, u, b, r, g, c)')
    parser.add_option('--type', dest='type', help='cards matching TYPE (e.g. artifact, creature, legendary, snow)')
    parser.add_option('--subtype', dest='subtype', 
                      help='cards matching SUBTYPE (e.g. goblin, equipment, aura)')
    parser.add_option('--power', dest='power', 
                      help='cards with power POWER (uses <, >, =)')
    parser.add_option('--tough', dest='tough', 
                      help='cards with toughness TOUGHNESS (uses <, >, =)')
    parser.add_option('--set', dest='set', 
                      help='cards matching expansion set SET (e.g. unlimited)')
    parser.add_option('--rarity', dest='rarity', 
                      help='cards matching rarity RARITY (c, u, r, m)')
    parser.add_option('--cmc', dest='cmc', help='cards with converted mana '
                      'cost CMC (uses <, >, =)')
    parser.add_option('-r', '--reminder', dest='reminder', action='store_true',
                      help='include reminder text')
    parser.add_option('--hidesets', dest='hidesets', action='store_true',
                      help='hide which sets the card was in')
    parser.add_option('--rulings', dest='rulings', action='store_true',
                      help='show rulings for the card')
    parser.add_option('--special', dest='special', action='store_true',
                      help='include special cards (e.g. planes)')
    logger.debug(args)
    
    (options, args) = parser.parse_args(args[1:])
    options.name =  ','.join(args)

    card_flags = ['text', 'color', 'subtype', 'type', 'set', 'cmc',
                  'power', 'tough', 'rarity', 'name']
    card_options = {}
    for a, b in zip(card_flags, map(vars(options).get, card_flags)):
        if b:
            card_options[a] = b
    logger.debug(card_options)
    request = CardRequest(card_options, special=options.special)
    extractor = CardExtractor(request.send())
    parsed = extractor.extract()
    cards = []
    for block in parsed:
        print Card.from_block(block).show()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    
