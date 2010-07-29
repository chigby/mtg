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

        td_tags = soup.table.findAll('td')
        
        # Get rulings hrefs here.

        content_lists = [tag.contents for tag in td_tags]
        print content_lists
        for p in content_lists:
            print p.string
        unified_content = []
        for lst in content_lists:
            unified_content.append(''.join([item.string or u'' for item in lst]))
        return unified_content
