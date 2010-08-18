def prettify_text(text):
    """Removes formatting and escape sequences from card text"""
    return text.strip('\r\n ').replace('||', '').replace('\n', ' ; ')

def prettify_attr(attr):
    """Removes formatting and escape sequences card attrbutes"""
    return attr.strip(':\r\n ').replace(' ', '_').replace('/', '_').lower()

class Card(object):

    def __init__(self):
        self.name = ''
        self.cost = ''
        self.type = ''
        self.rules_text = ''
        self.set_rarity = ''
        self.loyalty = ''
        self.power_toughness = ''

    @classmethod
    def from_block(cls, block):
        card = cls()
        for line in block:
            setattr(card, prettify_attr(line[0]), prettify_text(line[1]))        
        return card
