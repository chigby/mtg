import mtglib.card_extractor as mod
from mtglib.card_extractor import CardExtractor

class WhenInstantiatingCardExtractor(object):

    def setUp(self):
        self.extractor = CardExtractor('html')

    def should_be_instance_of_card_extractor(self):
        assert isinstance(self.extractor, CardExtractor)

    def should_accept_html(self):
        assert hasattr(self.extractor, 'html')
