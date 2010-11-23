import sys

from dingus import DingusTestCase
#from bin.mtg import main
#import bin.mtg as mod

from types import ModuleType
mtg = ModuleType('mtg')
exec open('bin/mtg') in mtg.__dict__
sys.modules['mtg'] = mtg
mod = mtg

class DescribeOptionParsing(DingusTestCase(mtg.main)):
    
    def setup(self):
        super(DescribeOptionParsing, self).setup()

    def should_print_help_if_no_args(self):
        mtg.main(['./mtg.py'])
        assert mod.OptionParser().calls('print_help')


class DescribeMainProgram(DingusTestCase(mtg.main, exclude=['OptionParser', 
                                                            'card_flags'])):
    
    def setup(self):
        super(DescribeMainProgram, self).setup()

    def should_make_card_request(self):
        mtg.main(['./mtg.py', 'sengir', 'vampire'])
        assert mod.SearchRequest.calls('()', {'name': 'sengir,vampire'})

    def should_make_card_request_with_text(self):
        mtg.main(['./mtg.py', '--text=trample'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_make_card_request_with_block(self):
        mtg.main(['./mtg.py', '--block=zendikar'])
        assert mod.SearchRequest.calls('()', {'block': 'zendikar'})

    def should_make_card_request_with_special(self):
        mtg.main(['./mtg.py', '--type=scheme', '--special'])
        assert mod.SearchRequest.calls('()', {'type': 'scheme'}, special=True,
                                       exclude_other_colors=None)

    def should_make_card_request_with_exclude(self):
        mtg.main(['./mtg.py', '--color=u', '-x'])
        print mod.SearchRequest.calls()
        assert mod.SearchRequest.calls('()', {'color': 'u'}, special=None,
                                       exclude_other_colors=True)

    def should_not_request_reminder(self):
        mtg.main(['./mtg.py', '--text=trample', '--reminder'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_not_request_hidesets(self):
        mtg.main(['./mtg.py', '--text=trample', '--hidesets'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_not_pass_rulings_to_gatherer_request(self):
        mtg.main(['./mtg.py', '--text=trample', '--rulings'])
        assert mod.SearchRequest.calls('()', {'text': 'trample'})

    def should_show_cards(self):
        mtg.main(['./mtg.py', 'sengir', 'vampire'])
        for card in mod.CardExtractor().extract():
            print card.calls()
            assert card.calls('show')
        
    def should_show_cards_and_rulings(self):
        mtg.main(['./mtg.py', 'sengir', 'vampire', '--rulings'])
        assert mod.CardExtractor().calls('extract')[0].kwargs == \
            {'get_card_urls': True}
        for card in mod.CardExtractor().extract():
            assert card.calls('show')[0].kwargs == {'rulings': True}

    def should_show_cards_and_flavor(self):
        mtg.main(['./mtg.py', 'natural', 'selection', '--flavor'])
        assert mod.CardExtractor().calls('extract')[0].kwargs == \
            {'get_card_urls': True}
        for card in mod.CardExtractor().extract():
            assert card.calls('show')[0].kwargs['flavor'] == True

    def should_show_cards_and_rulings(self):
        mtg.main(['./mtg.py', 'tarmogoyf', '--reminder'])
        assert mod.CardExtractor().calls('extract')[0].kwargs == \
            {'get_card_urls': None}
        for card in mod.CardExtractor().extract():
            assert card.calls('show')[0].kwargs == {'reminders': True, 
                                                    'rulings': None, 
                                                    'flavor':None}
