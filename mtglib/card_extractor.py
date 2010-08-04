import BeautifulSoup

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html

    def _group(self, lst, n):
        newlist = []
        for i in range(0, len(lst), n):
            val = lst[i:i+n]
            if len(val) == n:
                newlist.append(tuple(val))
        return newlist

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
        print td_tags
        unified_content = []
        for lst in content_lists:
            unified_content.append(''.join([item.string or u'' for item in lst]))
        # TODO: filter '\n||\n here
        unified_content = self._group(unified_content, 2)
        unified_content = self._group(unified_content, 6)        
        return unified_content
