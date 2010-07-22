class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html

    def extract(self):
        if not self.html:
            return False
