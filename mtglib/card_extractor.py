import BeautifulSoup

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html

    def extract(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        if not soup.table:
            raise Exception('Bad format for cards.')
        for tag in soup.findAll('br'):
            tag.replaceWith('||')
