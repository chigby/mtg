from mtglib.card import Card

class DescribeCard(object):

    def setUp(self):
        self.card = Card()

    def should_have_name(self):
        assert hasattr(self.card, 'name')

    def should_have_cost(self):
        assert hasattr(self.card, 'cost')

    def should_have_type(self):
        assert hasattr(self.card, 'type')

    def should_have_rules_text(self):
        assert hasattr(self.card, 'rules_text')
        
    def should_have_set_rarity(self):
        assert hasattr(self.card, 'set_rarity')


class WhenCreatingFromBlock(object):

    def setUp(self):
        self.block = (
            (u'\r\n              Name:\r\n          ', u'\nSengir Vampire\n'), 
            (u'\r\n              Cost:\r\n          ', u'\r\n     3BB\r\n   '), 
            (u'\r\n              Type:\r\n          ', u'\r\n    Creature  \u2014 Vampire\r\n                    '), 
            (u'\r\n                        Pow/Tgh:\r\n                    ', u'\r\n                        (4/4)\r\n                    '), 
            (u'\r\n                        Rules Text:\r\n                    ', u"\r\n                        Flying (This creature can't be blocked except by creatures with flying or reach.)||\nWhenever a creature dealt damage by Sengir Vampire this turn is put into a graveyard, put a +1/+1 counter on Sengir Vampire.\r\n                    "), 
            (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Tenth Edition Rare, Ninth Edition Rare, Torment Rare, Beatdown Box Set Uncommon, Battle Royale Box Set Uncommon, Fourth Edition Uncommon, Revised Edition Uncommon, Unlimited Edition Uncommon, Limited Edition Beta Uncommon, Limited Edition Alpha Uncommon\r\n                    ')
            )
        self.card = Card.from_block(self.block)

    def should_return_card(self):
        assert isinstance(self.card, Card)
        
    def should_extract_name(self):
        assert self.card.name == 'Sengir Vampire'

    def should_extract_cost(self):
        assert self.card.cost == '3BB'

    def should_extract_type(self):
        assert self.card.type == u'Creature  \u2014 Vampire'
        
    def should_extract_rules_text(self):
        rules_text = ('Flying (This creature can\'t be blocked except by '
                      'creatures with flying or reach.) ; Whenever a creature '
                      'dealt damage by Sengir Vampire this turn is put into a '
                      'graveyard, put a +1/+1 counter on Sengir Vampire.')
        print self.card.rules_text
        assert self.card.rules_text == rules_text

    def should_extract_set_rarity(self):
        set_rarity = ('Tenth Edition Rare, Ninth Edition Rare, Torment Rare, '
                      'Beatdown Box Set Uncommon, Battle Royale Box Set '
                      'Uncommon, Fourth Edition Uncommon, Revised Edition '
                      'Uncommon, Unlimited Edition Uncommon, Limited Edition '
                      'Beta Uncommon, Limited Edition Alpha Uncommon')
        assert self.card.set_rarity == set_rarity

    def should_extract_loyalty(self):
        assert self.card.loyalty == ''

    def should_extract_pow_tough(self):
        assert self.card.pow_tgh == '(4/4)'

class WhenCreatingPlaneswalkerFromBlock(object):
    
    def setUp(self):
        self.block = (
            (u'\r\n                        Name:\r\n                    ', u'\nLiliana Vess\n'), 
            (u'\r\n                        Cost:\r\n                    ', u'\r\n                        3BB\r\n                    '), 
            (u'\r\n                        Type:\r\n                    ', u'\r\n                        Planeswalker  \u2014 Liliana\r\n                    '), 
            (u'\r\n                        Loyalty:\r\n                    ', u'\r\n                        (5)\r\n                    '), 
            (u'\r\n                        Rules Text:\r\n                    ', u'\r\n                        +1: Target player discards a card.||\n-2: Search your library for a card, then shuffle your library and put that card on top of it.||\n-8: Put all creature cards in all graveyards onto the battlefield under your control.\r\n                    '), 
            (u'\r\n                        Set/Rarity:\r\n                    ', u'\r\n                        Magic 2011 Mythic Rare, Duel Decks: Garruk vs. Liliana Mythic Rare, Magic 2010 Mythic Rare, Lorwyn Rare\r\n                    ')
            )
        self.card = Card.from_block(self.block)

    def should_extract_name(self):
        assert self.card.name == 'Liliana Vess'

    def should_extract_cost(self):
        assert self.card.cost == '3BB'

    def should_extract_rules_text(self):
        rules_text = ('+1: Target player discards a card. ; -2: Search your'
                      ' library for a card, then shuffle your library and put'
                      ' that card on top of it. ; -8: Put all creature cards '
                      'in all graveyards onto the battlefield under your '
                      'control.')
        assert self.card.rules_text == rules_text

    def should_extract_loyalty(self):
        assert self.card.loyalty == '(5)'
