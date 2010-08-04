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
