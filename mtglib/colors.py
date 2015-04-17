# -*- coding: utf-8 -*-

class ColoredManaSymbol(object):
	YELLOW = '\033[33m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	BLACK = '\033[30m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

	def color(self, string):
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
		return '{0}{1}{2}'.format(ColoredManaSymbol.YELLOW, string, ColoredManaSymbol.ENDC)

	def blue(self, string):
		return '{0}{1}{2}'.format(ColoredManaSymbol.BLUE, string, ColoredManaSymbol.ENDC)

	def green(self, string):
		return '{0}{1}{2}'.format(ColoredManaSymbol.GREEN, string, ColoredManaSymbol.ENDC)

	def red(self, string):
		return '{0}{1}{2}'.format(ColoredManaSymbol.RED, string, ColoredManaSymbol.ENDC)

	def black(self, string):
		return '{0}{1}{2}'.format(ColoredManaSymbol.BLACK, string, ColoredManaSymbol.ENDC)
