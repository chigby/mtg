"""Request to the Gatherer site"""
import re
import httplib2
import logging
import urllib, urllib2

from constants import settings_url, settings_header, params, base_url, \
    default_modifiers, types

__all__ = ['SearchRequest', 'CardRequest']

class UrlFragment(object):
    """A piece of query string text in gatherer format."""

    def __init__(self, field, value, group=None):
        """
        Arguments:
        - `field`: Name of the field
        - `value`: Value of the field
        - `group`: Character that surrounds the values
        """
        self._field = field
        self._value = value
        self._group = group

    def __str__(self):
        if not self._value:
            return ''
        sep = re.compile('[,]+')
        value = sep.split(self.clean_value)
        field = '%s=' % self._field
        frag = ('%s[%s]' * (len(value))) % \
            tuple(self._get_modifiers(self._field, value))
        if self._group:
            frag = '+{group}({frag})'.format(group=self._group, frag=frag[1:])
        return field + frag

    def _get_modifiers(self, opt, lst):
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
                modifier_char = default_modifiers[opt]
            results.extend([modifier_char, item])
        return results

    @property
    def clean_value(self):
        return self._value.replace('"', '%22').replace(' ', '%20')


class SearchRequest(object):

    def __init__(self, options, special=False, exclude_other_colors=False):
        self.options = options
        self.special = special
        self.exclude_other_colors = exclude_other_colors

    def _get_url_fragments(self):
        fragments = []
        for opt, value in self.options.items():
            if opt == 'color' and self.exclude_other_colors:
                group = '@'
            else:
                group = None
            fragments.append(str(UrlFragment(opt, value, group=group)))
        return fragments

    def _comma_join(self, list_):
        return reduce(lambda s, t: s + ',' + t, list_)

    def _extract_subtypes(self):
        type_options = []
        subtype_options = []
        for opt in self.options['type'].split(','):
            opt = opt.lower()
            if opt.strip('!|') not in types:
                subtype_options.append(opt)
            else:
                type_options.append(opt)
        if type_options:
            self.options['type'] = ','.join(type_options)
        else:
            del self.options['type']
        if subtype_options:
            self.options['subtype'] = ','.join(subtype_options)

    def _parse_comparisons(self, attr):
        if attr in self.options:
            if not self.options[attr].startswith(('=', '<', '>')):
                self.options[attr] = '={0}'.format(self.options[attr])

    @property
    def url_fragments(self):
        if 'type' in self.options:
            self._extract_subtypes()
        if 'text' in self.options:
            if ' ' in self.options['text']:
                self.options['text'] = '"{0}"'.format(self.options['text'])
        if 'color' in self.options:
            if ',' not in self.options['color']:
                self.options['color'] = self._comma_join(self.options['color'])
            else:
                self.options['color'] = '|' + \
                    ',|'.join(self.options['color'].split(','))
        for attr in ['cmc', 'power', 'tough']:
            self._parse_comparisons(attr)
        return self._get_url_fragments()

    @property
    def special_fragment(self):
        return self.special and '&special=true' or ''

    @property
    def url(self):
        return (base_url + '&'.join((self.url_fragments)) + self.special_fragment)

    def send(self):
        http = httplib2.Http()
        try:
            response, content = http.request(settings_url, 'POST',
                                             headers=settings_header,
                                             body=urllib.urlencode(params))
        except httplib2.ServerNotFoundError as ex:
            print(ex)
            return False
        card_header = headers = {'Cookie': response['set-cookie']}

        # Possibly log this url.
        response, content = http.request(self.url, 'GET', headers=headers)
        return content


class CardRequest(object):

    def __init__(self, url):
        self.url = url

    def send(self):
        base_url = 'http://gatherer.wizards.com/Pages'
        if '..' in self.url:
            self.url = self.url.replace('..', base_url)
        socket = urllib2.urlopen(self.url)
        return socket.read()
