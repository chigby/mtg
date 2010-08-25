from dingus import DingusTestCase

from bin.mtg import main
import bin.mtg as mod

class DescribeMainProgram(DingusTestCase(main, exclude=['OptionParser', 
                                                        'card_flags'])):
    
    def setup(self):
        super(DescribeMainProgram, self).setup()

    def should_make_card_request(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.SearchRequest.calls('()', {'name': 'sengir,vampire'})

    def should_make_card_request_with_text(self):
        main(['./mtg.py', '--text=trample'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_make_card_request_with_special(self):
        main(['./mtg.py', '--type=scheme', '--special'])
        assert mod.SearchRequest.calls('()', {'type': 'scheme'}, special=True)

    def should_not_request_reminder(self):
        main(['./mtg.py', '--text=trample', '--reminder'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_not_request_hidesets(self):
        main(['./mtg.py', '--text=trample', '--hidesets'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_not_pass_rulings_to_gatherer_request(self):
        main(['./mtg.py', '--text=trample', '--rulings'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_parse_response(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.CardExtractor.calls('()', mod.SearchRequest().send())
        assert mod.CardExtractor().calls('extract').once()
        for block in mod.CardExtractor().extract():
            assert mod.Card.calls('from_block', block)

    def should_show_cards(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.Card.from_block().calls('show')
        
    def should_show_cards_and_rulings(self):
        main(['./mtg.py', 'sengir', 'vampire', '--rulings'])
        assert mod.CardExtractor().calls('extract')[0].kwargs == \
            {'get_card_urls': True}
        assert mod.Card.from_block().calls('show')[0].kwargs == \
            {'rulings': True}

