from dingus import DingusTestCase

from bin.mtg import main
import bin.mtg as mod

class DescribeMainProgram(DingusTestCase(main, exclude=['OptionParser'])):
    
    def setup(self):
        super(DescribeMainProgram, self).setup()

    def should_make_card_request(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.CardRequest.calls('()', {'name': 'sengir,vampire'})

    def should_make_card_request_with_text(self):
        main(['./mtg.py', '--text=trample'])
        assert mod.CardRequest.calls('()', {'text': 'trample'})

    def should_make_card_request_with_special(self):
        main(['./mtg.py', '--type=scheme', '--special'])
        assert mod.CardRequest.calls('()', {'type': 'scheme'}, special=True)

    def should_not_request_reminder(self):
        main(['./mtg.py', '--text=trample', '--reminder'])
        assert mod.CardRequest.calls('()', {'text': 'trample'})

    def should_not_request_hidesets(self):
        main(['./mtg.py', '--text=trample', '--hidesets'])
        assert mod.CardRequest.calls('()', {'text': 'trample'})

    def should_not_pass_rulings_to_gatherer_request(self):
        main(['./mtg.py', '--text=trample', '--rulings'])
        assert mod.CardRequest.calls('()', {'text': 'trample'})

    def should_parse_response(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.CardExtractor.calls('()', mod.CardRequest().send())
        assert mod.CardExtractor().calls('extract').once()
        for block in mod.CardExtractor().extract():
            assert mod.Card.calls('from_block', block)

    def should_show_cards(self):
        main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.Card.from_block().calls('show')
            # print mod.Card.from_block.calls()
            # assert card.calls('show')
