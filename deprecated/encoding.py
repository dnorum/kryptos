class CharacterEncoding:
	def __init__(self, character, value):
		self.character = character
		self.value = value
		if not value >= 0:
			raise ValueError("Value must be non-negative")
		if value != round(value):
			raise ValueError("Value must be integer")
		if not len(character) == 1:
			raise ValueError("String must be single character")
	# Purely for debugging
	def Print(self):
		print self.character, "//", self.value

class CharacterMapping:
	def __init__(self):
		self.map = []
	def addCharacterEncoding(self, encoding):
		self.map.append(encoding)
	def encode(self, character):
		for encoding in self.map:
			if encoding.character == character:
				return encoding.value
		return -1
	def decode(self, value):
		for encoding in self.map:
			if encoding.value == value:
				return encoding.character
		return -1
	# Purely for debugging
	def Print(self):
		for encoding in self.map:
			encoding.Print()

def encode(string, mapping):
	encoded = []
	for character in string:
		encoded.append(mapping.encode(character))
	return encoded

def decode(array, mapping):
	decoded = []
	for value in array:
		decoded.append(mapping.decode(value))
	return decoded

def loadMappingZeroIndexed(filename):
	mapping = CharacterMapping()
	index = 0
	mappingFile = open(filename, 'r')
	characters = mappingFile.read().rstrip('\n')
	for character in characters:
		mapping.addCharacterEncoding(CharacterEncoding(character, index))
		index += 1
	return mapping

#mapping = loadMappingZeroIndexed("mapping1.txt")
#string = "ALPHABETICALENCODING"
#print encode(string, mapping)
