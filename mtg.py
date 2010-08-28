#!/opt/local/bin/python
"""
Console-based access to the Gatherer Magic Card Database.

Usage: %prog [options] [cardname]
"""

import httplib2
import re
import textwrap
import urllib, urllib2
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser

from mtglib.card import replace_reminders, formatted_wrap, prettify_text

def group(lst, n):
    newlist = []
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            newlist.append(tuple(val))
    return newlist

settings_url = 'http://gatherer.wizards.com/Pages/Settings.aspx'
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

def get_rulings(url):
    url = url.replace('..', 'http://gatherer.wizards.com/Pages')
    try:
        sock = urllib2.urlopen(url)
    except Exception as err:
        return err.message
    soup = BeautifulSoup(sock.read())
    for tag in soup.findAll('autocard'):
        tag.replaceWith(tag.string)
    rulings_text = soup.findAll(attrs={'id' : re.compile('rulingText$')})
    rulings_date = soup.findAll(attrs={'id' : re.compile('rulingDate$')})
    rulings_text = [''.join(tag.contents) for tag in rulings_text]
    rulings_date = [''.join(tag.contents) for tag in rulings_date]
    return zip(rulings_date, rulings_text)

def get_modifiers(lst):
    modifiers = re.compile('^([!=|<>]+)')
    results = []
    for item in lst:
        matches = modifiers.match(item)
        if matches:
            modifier_char = '+' + matches.group(0)
            if modifier_char == '+|':
                modifier_char = '|'
            item = modifiers.sub('', item)
        else:
            modifier_char = '+'
        results.extend([modifier_char, item])
    return results

def main(options, args):
    name = '+'.join(['[{0}]'.format(arg) for arg in args])

    url = ('http://gatherer.wizards.com/Pages/Search/Default.aspx'
           '?output=spoiler&method=text&name={0}'.format(name))

    possible_options = ['text', 'color', 'subtype', 'type', 'set', 'cmc',
                        'power', 'tough', 'rarity']
    for opt in possible_options:
        value = getattr(options, opt)
        if value:
            sep = re.compile('[,]+')
            value = sep.split(value)
            url += '&%s=' % opt
            url += ('%s[%s]' * (len(value))) % tuple(get_modifiers(value))
    
    if options.special:
        url += '&special=true'
    
    print url
    url = url.replace('"', '%22').replace(' ', '%20')
    http = httplib2.Http()
    headers = {'Content-type': 'application/x-www-form-urlencoded'} 
    try:
        response, content = http.request(settings_url, 'POST', headers=headers,
                                         body=urllib.urlencode(params))
    except httplib2.ServerNotFoundError:
        print 'Could not connect.'
        return 0
    headers = {'Cookie': response['set-cookie']}
    
    try:
        response, content = http.request(url, 'GET', headers=headers) 
    except httplib2.ServerNotFoundError:
        print 'Could not connect.'
        return 0

    soup = BeautifulSoup(content)
    if not soup.table:
        return 0
    for tag in soup.findAll('br'):
        tag.replaceWith('||')

    td_tags = soup.table.findAll('td')

    if options.rulings:
        a_tags = soup.table.findAll('a')
        hrefs = [tag['href'] for tag in a_tags]
        print hrefs
    
    content_lists = [tag.contents for tag in td_tags]
    
    unified_content = []
    for lst in content_lists:
        unified_content.append(''.join([item.string or u'' for item in lst]))
    unified_content = [item for item in unified_content if item != u'\n||\n']
    unified_content = group(unified_content, 2)
    unified_content = group(unified_content, 6)
    card_template = (u"{0[Name]} {0[Cost]}\n"
                   u"{0[Type]}\nText: {0[Number]} {0[Rules Text]}\n"
                   u"{0[Set/Rarity]}")
    for i, card in enumerate(unified_content):
        cards = {}
        print '\n------------------------------'
        #print card
        for line in card:
            cards[line[0].strip(':\r\n ')] = prettify_text(line[1])
        #print cards
        # removes the name from the card text.  make optional?
        cards['Rules Text'] = (cards['Rules Text'].
                               replace(cards['Name'], '~this~'))
        if 'Loyalty' in cards:
            cards['Number'] = cards['Loyalty']
        else:
            cards['Number'] = cards['Pow/Tgh']
        if not options.reminder:
            cards['Rules Text'] = replace_reminders(cards['Rules Text'])
        if options.hidesets:
            cards['Set/Rarity'] = ''
        else:
            cards['Set/Rarity'] = textwrap.fill(cards['Set/Rarity'])
        cards['Rules Text'] = formatted_wrap(cards['Rules Text'])        
        print card_template.format(cards)
        if options.rulings and i < 5:
            rulings = get_rulings(hrefs[i])
            for date, text in rulings:
                print textwrap.fill('{0}: {1}'.format(date, text))
    return i+1

if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options] [cardname]')
    parser.add_option("-t", "--text", dest="text",
                      help="containing rules text TEXT", metavar="TEXT")
    parser.add_option('--color', dest='color', help='cards matching COLOR (w, u, b, r, g, c)')
    parser.add_option('--type', dest='type', help='cards matching TYPE (e.g. artifact, creature, legendary, snow)')
    parser.add_option('--subtype', dest='subtype', 
                      help='cards matching SUBTYPE (e.g. goblin, equipment, aura)')
    parser.add_option('--power', dest='power', 
                      help='cards with power POWER (uses <, >, =)')
    parser.add_option('--tough', dest='tough', 
                      help='cards with toughness TOUGHNESS (uses <, >, =)')
    parser.add_option('--set', dest='set', 
                      help='cards matching expansion set SET (e.g. unlimited)')
    parser.add_option('--rarity', dest='rarity', 
                      help='cards matching rarity RARITY (c, u, r, m)')
    parser.add_option('--cmc', dest='cmc', help='cards with converted mana '
                      'cost CMC (uses <, >, =)')
    parser.add_option('-r', '--reminder', dest='reminder', action='store_true',
                      help='include reminder text')
    parser.add_option('--hidesets', dest='hidesets', action='store_true',
                      help='hide which sets the card was in')
    parser.add_option('--rulings', dest='rulings', action='store_true',
                      help='show rulings for the card')
    parser.add_option('--special', dest='special', action='store_true',
                      help='include special cards (e.g. planes)')
    (options, args) = parser.parse_args()
    num_results = main(options, args)
    if num_results != 1:
        print("\n{0} results found.".format(num_results))

