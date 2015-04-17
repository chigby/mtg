# -*- coding: utf-8 -*-

class ColoredManaCost(object):
	YELLOW = '\033[33m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	BLACK = '\033[30m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

	def draw(self, string):
		manaCost = ''
		for letter in string:
			if letter == 'U':
				manaCost += self.blue(letter)
			elif letter == 'R':
				manaCost += self.red(letter)
			elif letter == 'W':
				manaCost += self.yellow(letter)
			elif letter == 'B':
				manaCost += self.black(letter)
			elif letter == 'G':
				manaCost += self.green(letter)
			else:
				manaCost += letter

		return manaCost

	def yellow(self, string):
		return '{0}{1}{2}'.format(ColoredManaCost.YELLOW, string, ColoredManaCost.ENDC)

	def blue(self, string):
		return '{0}{1}{2}'.format(ColoredManaCost.BLUE, string, ColoredManaCost.ENDC)

	def green(self, string):
		return '{0}{1}{2}'.format(ColoredManaCost.GREEN, string, ColoredManaCost.ENDC)

	def red(self, string):
		return '{0}{1}{2}'.format(ColoredManaCost.RED, string, ColoredManaCost.ENDC)

	def black(self, string):
		return '{0}{1}{2}'.format(ColoredManaCost.BLACK, string, ColoredManaCost.ENDC)
