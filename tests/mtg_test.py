import unittest2

import mtg

class WhenRemovingReminderText(unittest2.TestCase):
    """When Removing Reminder Text"""

    def should_delete_reminder_text(self):
        text = 'Flying (Can only be blocked by creatures with flying.)'
        assert mtg.replace_reminders(text) == 'Flying '

    def should_remove_hybrid_mana_reminders(self):
        text = '({(g/w)} can be paid with either {G} or {W}.) ; Other ' \
            'permanents you control can\'t be the targets of spells or' \
            ' abilities your opponents control.'
        replaced_text =  '; Other permanents you control can\'t be the' \
            ' targets of spells or abilities your opponents control.'
        assert mtg.replace_reminders(text) == replaced_text
    
    def should_preserve_hybrid_activation_costs(self):
        text = '{(g/u)}: ~this~ gains shroud until end of turn. ;'
        assert mtg.replace_reminders(text) == text

    def should_remove_level_up_reminder(self):
        text = ('Level up {W} ({W}: Put a level counter on this. Level up'
                ' only as a sorcery.) ;')
        replaced_text = 'Level up {W} ;'
        assert mtg.replace_reminders(text) == replaced_text

    def should_preserve_multi_hybrid_activations(self):
        text = ('{(r/w)}: ~this~ becomes a 2/2 Kithkin Spirit. ;'
                '{(r/w){(r/w){(r/w)}: If ~this~ is a Spirit, it becomes a 4/4 '
                'Kithkin Spirit Warrior. ; {(r/w){(r/w){(r/w){(r/w){(r/w)'
                '{(r/w)}: If ~this~ is a Warrior, it becomes an 8/8 Kithkin'
                ' Spirit Warrior Avatar with flying and first strike.')
        assert mtg.replace_reminders(text) == text
