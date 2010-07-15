"""Request to the gatherer site"""

def get_url_fragments(options):
    pass

class CardRequest(object):

    base_url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
                '?output=spoiler&method=text')

    def __init__(self, options, name=None):
        self.options = options
        
    @property
    def url_fragments(self):
        return get_url_fragments(self.options)
