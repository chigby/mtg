import re
import textwrap

def formatted_wrap(text):
    return textwrap.fill(u'            {0}'.format(text)).strip()

def replace_reminders(text):
    """Remove reminder text from cards (complete sentences enclosed in
    parentheses)."""
    return re.sub(r'\(.*?\.\)\ *', '', text)    

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
        self.url = ''
        self.card_template = (u"{0.name} {0.cost}\n"
                              u"{0.type}\nText: {0.number} {0.rules_text}\n"
                              u"{0.set_rarity}")

    @classmethod
    def from_block(cls, block):
        card = cls()
        for line in block:
            setattr(card, prettify_attr(line[0]), prettify_text(line[1]))        
        return card

    def show(self, reminders=False):
        if not reminders:
            self.rules_text = replace_reminders(self.rules_text)
        self.rules_text = self.rules_text.replace(self.name, '~this~')
        self.rules_text = formatted_wrap(self.rules_text)
        return self.card_template.format(self)
    
    @property
    def number(self):
        return self.pow_tgh or self.loyalty
