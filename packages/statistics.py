import math

class Error(Exception):
	# Base class for exceptions in this module.
	pass

class AlphabetError(Error):
	# Error resulting from trying to use two distinct character sets
	# Attributes
	#	characters1 -- The first set of characters
	#	characters2 -- The second set of characters
	def __init__(self, characters1, characters2):
		self.characters1 = characters1
		self.characters2 = characters2

class SmallSampleError(Error):
	# Error resulting from a too-short string.
	# Attributes
	#	string -- The string that doesn't have enough characters
	def __init__(self, string):
		self.string = string

# alphabet is assumed to be of type alphabet.py::Alphabet
def indexOfCoincidence( text, alphabet ):
	c = len(alphabet.characters)
	N = len(text)
	if N < 2:
		raise SmallSampleError(text)
	ic = 0.;
	for character in alphabet.characters:
		n = text.count(character)
		ic += n*(n-1)
	return ic * c / (N*(N-1))

# Both arguments are assumed to be of type alphabet.py::Distribution
def distributionDeviation( distribution, referenceDistribution ):
	if not distribution.alphabet == referenceDistribution.alphabet:
		raise AlphabetError(distribution.alphabet.characters, referenceDistribution.alphabet.characters)
	deviation = 0.
	for i in range(0, len(referenceDistribution.frequencies)):
		deviation += (distribution.frequencies[i] - referenceDistribution.frequencies[i]) ** 2
	return math.sqrt(deviation)
