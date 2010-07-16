"""Request to the gatherer site"""
import re

def get_modifiers(lst):
    modifiers = re.compile('^([!=|<>]+)')
    results = []
    for item in lst:
        matches = modifiers.match(item)
        if matches:
            modifier_char = '+' + matches.group(0)
            if modifier_char == '+|':
                modifier_char = '|'
            item = modifiers.sub('', item)
        else:
            modifier_char = '+'
        results.extend([modifier_char, item])
    return results

def get_url_fragments(options):
    fragments = []
    for opt, value in options.items():
        if value:
            sep = re.compile('[,]+')
            value = sep.split(value)
            frag = '%s=' % opt
            frag += ('%s[%s]' * (len(value))) % tuple(get_modifiers(value))
            fragments.append(frag)
    return fragments
                
class CardRequest(object):

    base_url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
                '?output=spoiler&method=text&')

    def __init__(self, options, special=False):
        self.options = options
        self.special = special
        
    @property
    def url_fragments(self):
        return get_url_fragments(self.options)

    @property
    def special_fragment(self):
        return self.special and '&special=true' or ''

    @property
    def url(self):
        return self.base_url + '&'.join(self.url_fragments) + \
            self.special_fragment
