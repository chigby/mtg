import unittest2

import mtg

class MtgTestCase(unittest2.TestCase):
    """Test case for mtg"""

    def setUp(self):
        pass

    def test_replace_reminders(self):
        text = 'Flying (Can only be blocked by creatures with flying.)'
        self.assertEqual(mtg.replace_reminders(text), 'Flying ')

    def test_reminders_hybrid(self):
        text = '({(g/w)} can be paid with either {G} or {W}.) ; Other ' \
            'permanents you control can\'t be the targets of spells or' \
            ' abilities your opponents control.'
        replaced_text =  '; Other permanents you control can\'t be the' \
            ' targets of spells or abilities your opponents control.'
        self.assertEqual(mtg.replace_reminders(text), replaced_text)
    
    def test_reminders_hybrid_cost(self):
        text = '{(g/u)}: ~this~ gains shroud until end of turn. ;'
        self.assertEqual(mtg.replace_reminders(text), text)

    def test_reminders_figure_of_destiny(self):
        text = ('{(r/w)}: ~this~ becomes a 2/2 Kithkin Spirit. ;'
                '{(r/w){(r/w){(r/w)}: If ~this~ is a Spirit, it becomes a 4/4 '
                'Kithkin Spirit Warrior. ; {(r/w){(r/w){(r/w){(r/w){(r/w)'
                '{(r/w)}: If ~this~ is a Warrior, it becomes an 8/8 Kithkin'
                ' Spirit Warrior Avatar with flying and first strike.')
        self.assertEqual(mtg.replace_reminders(text), text)
