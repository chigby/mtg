import BeautifulSoup

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html
        self.fields_per_card = 6

    def _group(self, lst, n):
        newlist = []
        for i in range(0, len(lst), n):
            val = lst[i:i+n]
            if len(val) == n:
                newlist.append(tuple(val))
        return newlist

    def extract(self, get_card_urls=False):
        data_fields = self.fields_per_card
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        if not soup.table:
            raise Exception('Bad format for cards.')
        for tag in soup.findAll('br'):
            tag.replaceWith('||')

        td_tags = soup.table.findAll('td')
        
        # Get rulings hrefs here.
        if get_card_urls:
            data_fields = data_fields + 1
            a_tags = soup.table.findAll('a')
            card_urls = [tag['href'] for tag in a_tags]

        content_lists = [tag.contents for tag in td_tags]
        unified_content = []
        for i, lst in enumerate(content_lists):
            if get_card_urls and i % (self.fields_per_card * 2) == 0:
                unified_content.append('card_url')
                unified_content.append(card_urls.pop(0))
            unified_content.append(''.join([item.string or u'' for item in lst]))
        # TODO: filter '\n||\n here
        unified_content = self._group(unified_content, 2)
        unified_content = self._group(unified_content, data_fields)
        print unified_content
        return unified_content
