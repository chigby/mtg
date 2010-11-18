base_url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
            '?output=spoiler&method=text&')
settings_url = 'http://gatherer.wizards.com/Pages/Settings.aspx'
settings_header =  {'Content-type': 'application/x-www-form-urlencoded'}
params = {'ctl00$ctl00$MainContent$SearchControls$CardSearchBoxParent'
          '$CardSearchBox':'Search Terms...',
          'ctl00$ctl00$MainContent$SearchControls$SearchCardName':'on', 
          'ctl00$ctl00$MainContent$SubContent$AutoComplete':
              'EnableAutoComplete',
          'ctl00$ctl00$MainContent$SubContent$CardLinkAction':'SameWindow',
          'ctl00$ctl00$MainContent$SubContent$GroupBy':'None',
          'ctl00$ctl00$MainContent$SubContent$HintText':'EnableHintText',
          'ctl00$ctl00$MainContent$SubContent$ResultsPerPage':'100',
          'ctl00$ctl00$MainContent$SubContent$ResultsView':'SpoilerView',
          'ctl00$ctl00$MainContent$SubContent$Save':'Save',
          'ctl00$ctl00$MainContent$SubContent$SelectingCard':'NavigatesToCard',
          'ctl00$ctl00$MainContent$SubContent$cardRulings':'on',
          'ctl00$ctl00$MainContent$SubContent$languagePreferenceSelector'
          '$LanguageGroup':'en-US',
          '__EVENTVALIDATION': '/wEWKwK75+DFAQLevrmxAQL998wLAszrof8GAqS1kKUNAs'
          'eQ9aYKArHA+agHAtuiyI8KAuW4lukEAtL65/MEAt2f/Z4CAvDTh/UIAriI5sIBAtvjr'
          'rcEAvq+4Y0KApT4iwMC5OKZxggCq/jh3QUC76eDBALT5/SDBQKV+emYAwKGm+HlBALq'
          'yuj+BALZvOTwDwKMgbNSAuDnzLIOAp70x7sEAvLXn6QKArCK6dYHAuPs49oPApCO0FQ'
          'CwdvMhgsCj/XJ2QYC5P/93QQCnf7J5AkC5fat2woCl/rZiQgCgviplAIC7/a91ggC8P'
          'mhkQEC/PSBnQEC2f/drAMC+JCPwAlYnqtQQxfeLziePLQKzhRQ535I5Q==',
          '__VIEWSTATE': '/wEPDwUKMTA0MjI1NTI4M2QYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFiMFNWN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmROYW1lBTZjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTZWFyY2hDb250cm9scyRTZWFyY2hDYXJkVHlwZXMFNWN0bDAwJGN0bDAwJE1haW5Db250ZW50JFNlYXJjaENvbnRyb2xzJFNlYXJjaENhcmRUZXh0BS9jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFN0YW5kYXJkVmlldwUuY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDb21wYWN0VmlldwUwY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDaGVja2xpc3RWaWV3BS5jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFNwb2lsZXJWaWV3BS9jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JEltYWdlT25Ib3ZlcgU1Y3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRFbmFibGVBdXRvQ29tcGxldGUFNmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkRGlzYWJsZUF1dG9Db21wbGV0ZQVIY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRFbmFibGVBdXRvQ29tcGxldGVFdmVuSWZOYW1lVW5jaGVja2VkBTFjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JEVuYWJsZUhpbnRUZXh0BTJjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JERpc2FibGVIaW50VGV4dAU/Y3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRDbG9zZURldGFpbHNPbkNhcmRJbWFnZUNsaWNrBUVjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JFJlZGlyZWN0VG9EZXRhaWxzUGFnZVdpdGhPbmVSZXN1bHQFMmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkZmVlZGJhY2tNZXNzYWdlBTljdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGZyb250UGFnZVNlYXJjaE9wdGlvbnMFOmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkb3RoZXJQYWdlc1NlYXJjaE9wdGlvbnMFN2N0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkc2VhcmNoUmVzdWx0c09wdGlvbnMFLmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkY2FyZFJ1bGluZ3MFMmN0bDAwJGN0bDAwJE1haW5Db250ZW50JFN1YkNvbnRlbnQkcG9wdWxhckNvbW1lbnRzBTFjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JHJlY2VudENvbW1lbnRzBT1jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGRpc2N1c3Npb25QcmludGluZ3NXYXJuaW5nBS5jdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGNvbW1lbnRGb3JtBTVjdGwwMCRjdGwwMCRNYWluQ29udGVudCRTdWJDb250ZW50JGZvcm1hdE5vdGlmaWNhdGlvbgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzMwVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAyOAVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMjA1MgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzNgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0MQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0OQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMzA4MgVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTA0MAVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMTAzMQVGY3RsMDAkY3RsMDAkTWFpbkNvbnRlbnQkU3ViQ29udGVudCRsYW5ndWFnZVByZWZlcmVuY2VTZWxlY3RvciRMQ0lEMjA3MKbhIzf0+FFOPMtewwL7KqW90P6P'
          }

card_flags = ['text', 'color', 'subtype', 'type', 'set', 'cmc', 'power', 
              'tough', 'rarity', 'name', 'block']

default_modifiers = dict(text='+', color='+', type='+', subtype='+', set='|', 
                         cmc='+', power='+', tough='+', rarity='+', name='+',
                         block='+')

types = ['artifact', 'basic', 'creature', 'enchantment', 'instant', 'land', 
         'legendary', 'ongoing', 'plane', 'planeswalker', 'scheme', 'snow', 
         'sorcery', 'tribal', 'vanguard', 'world']

separator = '\n------------------------------'
