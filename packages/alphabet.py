class Error(Exception):
	# Base class for exceptions in this module.
	pass

class AllowableCharacterError(Error):
	# Error resulting from the presence of a disallowed character.
	# Attributes:
	#	character -- The character which caused the error
	#	allowableCharacters -- Allowable characters, for reference
	def __init__(self, character, allowableCharacters):
		self.character = character
		self.allowableCharacters = allowableCharacters

class AllowableValueError(Error):
	# Error resulting from decoding an out-of-bounds value.
	# Attributes:
	#	value -- The value which caused the error
	#	maxIndex -- The maximum allowable index value
	def __init__(self, value, maxIndex):
		self.value = value
		self.maxIndex = maxIndex

class RepeatedCharacterError(Error):
	# Error resulting from a repeated character in a by-definition unique string.
	# Attributes:
	#	character -- The character being repeated.
	def __init__(self, character):
		self.character = character

class DimensionError(Error):
	# Error resulting from mismatched dimensions.
	# Attributes:
	#	dimension1 -- The first dimension
	#	dimension2 -- The second dimension
	def __init__(self, dimension1, dimension2):
		self.dimension1 = dimension1
		self.dimension2 = dimension2

# Define the universe of characters.
def allowableCharacters():
	return "ABCDEFGHIJKLMNOPQRSTUVWXYZ.,?"

# Note that for calculation purposes, the numerical value of a character is equal to its index.
class Alphabet:

	# Kludgy as hell
	allowableCharacters = allowableCharacters()

	def __init__(self, characters):
		for character in characters:
			# Check for unsupported characters.
			if character not in allowableCharacters():
				raise AllowableCharacterError(character, allowableCharacters)
			# Make sure that the characters in the alphabet are unique.
			if characters.count(character) > 1:
				raise RepeatedCharacterError(character)
		self.characters = characters

	# Default sort.
	def sort(self):
		self.characters = sorted(self.characters)

	# Pull out the number of characters for modular arithmetic.
	def modulus(self):
		return len(self.characters)

	# Sort the alphabet using a key.
	# E.g., "ABCDE" + "BED" = "BEDAC"
	def key(self, key):
		sortedCharacters = ""
		# Start from a sorted state.
		self.sort()
		# Put the key first, taking only the first instance of duplicated characters.
		for character in key:
			if character not in self.characters:
				raise AllowableCharacterError(character, self.characters)
			if character not in sortedCharacters:
				sortedCharacters += character
		# Add in the rest of the alphabet in order.
		for character in self.characters:
			if character not in sortedCharacters:
				sortedCharacters += character
		self.characters = sortedCharacters

	# Check to make sure that a string only contains characters from the alphabet.
	def check(self, string):
		for character in string:
			if character not in self.characters:
				raise AllowableCharacterError(character, self.characters)

	# Remove non-alphabet characters from a string.
	def scrub(self, string):
		scrubbed = ""
		for character in string:
			if character in self.characters:
				scrubbed += character
		return scrubbed

	def encodeCharacter(self, character):
		if character not in self.characters:
			raise AllowableCharacterError(character, self.characters)
		return self.characters.index(character)

	def encodeString(self, string):
		encodedString = []
		for character in string:
			encodedString.append(self.encodeCharacter(character))
		return encodedString

	def decodeCharacter(self, value):
		if value not in range(0,len(self.characters)):
			raise AllowableValueError(value, len(self.characters))
		return self.characters[value]

	def decodeString(self, values):
		decodedString = []
		for value in values:
			decodedString.append(self.decodeCharacter(value))
		return decodedString

	def encodeCharacterWildcard(self, character, wildcard):
		if character == wildcard:
			return wildcard
		if character not in self.characters:
			raise AllowableCharacterError(character, self.characters)
		return self.characters.index(character)

	def encodeStringWildcard(self, string, wildcard):
		encodedString = []
		for character in string:
			encodedString.append(self.encodeCharacterWildcard(character, wildcard))
		return encodedString

	def decodeCharacterWildcard(self, value, wildcard):
		if value == wildcard:
			return wildcard
		if value not in range(0,len(self.characters)):
			raise AllowableValueError(value, len(self.characters))
		return self.characters[value]

	def decodeStringWildcard(self, values, wildcard):
		decodedString = []
		for value in values:
			decodedString.append(self.decodeCharacterWildcard(value, wildcard))
		return decodedString

class Distribution:

	def __init__(self, alphabet, frequencies):
		self.alphabet = alphabet
		self.frequencies = frequencies
		if not len(self.alphabet.characters) == len(frequencies):
			raise DimensionError(len(self.alphabet.characters), len(frequencies))

	def printDistribution(self):
		for i in range(0,len(self.alphabet.characters)-1):
			print(self.alphabet.characters[i], self.frequencies[i])

def loadDistribution(fileName):
	# Initialize
	characters = ""
	frequencies = []

	definition = open(fileName, 'r')
	for line in definition:
		# Ignore comment lines w/ leading space and any empty lines
		if not line[0] == ' ' and not len(line) == 0:
			characters += line[0]
			# Remove any trailing whitespace (esp. newlines)
			frequencies.append(float(line.rstrip()[2:]))
	definition.close()
	alphabet = Alphabet(characters)
	return Distribution(alphabet, frequencies)

# alphabet is assumed to be of type alphabet.py::Alphabet
def createDistribution(string, alphabet):
	# Only consider characters in the alphabet
	string = alphabet.scrub(string)
	nCharacters = float(len(string))
	frequencies = []
	for character in alphabet.characters:
		frequencies.append(float(string.count(character))/nCharacters)
	return Distribution(alphabet, frequencies)
