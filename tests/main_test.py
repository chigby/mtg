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
        
