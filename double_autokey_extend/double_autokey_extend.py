import datetime

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Define the ciphertext and minimum key length.
ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
minKeyLength = 6

# Define dictionary functions / classes.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return dictionary

def extractBeginnings(dictionary):
	beginnings = set()
	for word in dictionary:
		for i in range(0, len(word)):
			beginnings.add(word[0:(i+1)])
	return beginnings

def extractMiddles(dictionary):
	middles = set()
	for word in dictionary:
		for i in range(0, len(word)):
			ending = word[-(i+1):]
			for j in range(0, len(ending)):
				middles.add(ending[0:(j+1)])
	return middles

def extractEndings(dictionary):
	endings = set()
	for word in dictionary:
		for i in range(0, len(word)):
			endings.add(word[-(i+1):])
	return endings

class Dictionary:
	def __init__(self, words, beginnings, middles, endings):
		self.words = words
		self.beginnings = beginnings
		self.middles = middles
		self.endings = endings

# Construct lookup for letters.
lookup = dict()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		pair = letter1 + letter2
		keystreamLetter = QuagmireIII(alphabet, "KRYPTOS", letter1, "K").encrypt(letter2)
		lookup[pair] = keystreamLetter

def encrypt(lookup, string1, string2):
	if len(string1) != len(string2):
		raise Error
	result = ""
	for i in range(0, len(string1)):
		result += lookup[string1[i] + string2[i]]
	return result

# Define text validity / word-search function.
def validityText(dictionary, invalidStrings, text):
	validities = set()
	for string in invalidStrings:
		if string in text:
			return validities
	# Base cases.
	if (text in dictionary.words):
		validities.add("words")
	if (text in dictionary.beginnings):
		validities.add("beginnings")
	if (text in dictionary.middles):
		validities.add("middles")
	if (text in dictionary.endings):
		validities.add("endings")
	# Break apart and scan.
	for i in range(1, len(text)):
		first = text[:i]
		second = text[i:]
		firstValidity = validityText(dictionary, invalidStrings, first)
		secondValidity = validityText(dictionary, invalidStrings, second)
		if not firstValidity.isdisjoint({"endings"}):
			if not secondValidity.isdisjoint({"beginnings"}):
				validities.add("endings_beginnings")
			if not secondValidity.isdisjoint({"words_beginnings"}):
				validities.add("endings_words_beginnings")
			if not secondValidity.isdisjoint({"words"}):
				validities.add("endings_words")
		if not firstValidity.isdisjoint({"endings_words"}):
			if not secondValidity.isdisjoint({"beginnings", "words_beginnings"}):
				validities.add("endings_words_beginnings")
			if not secondValidity.isdisjoint({"words_beginnings"}):
				validities.add("endings_words_beginnings")
			if not secondValidity.isdisjoint({"words"}):
				validities.add("endings_words")
		if not firstValidity.isdisjoint({"words"}):
			if not secondValidity.isdisjoint({"beginnings", "words_beginnings"}):
				validities.add("words_beginnings")
			if not secondValidity.isdisjoint({"words"}):
				validities.add("words")
	return validities

# Load dictionary for the keys.
dictionaryName = "10kwords_pruned"
dictionaryFilename = "../resources/dictionaries/" + dictionaryName + ".txt"
words = loadDictionaryFile(dictionaryFilename)
beginnings = extractBeginnings(words)
middles = extractMiddles(words)
endings = extractEndings(words)

# Bundle it up.
dictionary = Dictionary(words, beginnings, middles, endings)

# 1kwords	1,000
# 10kwords	10,000
# 10kwords_pruned	~10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:

# In progress:
# 10kwords_pruned

# Open output file.
filename = "double_autokey_extend"
results = open(filename + "_" + dictionaryName + ".output", 'w', 1)
results.write("Key 1\tKey 2\tPlaintext\n")

# Set logging.
attemptsPerMessage = 100
attempts = 0

# Search.
for key1 in sorted(words):

	if key1 < "ENHANCE":
		continue

	if len(key1) > minKeyLength:
		for key2 in sorted(words):
			if len(key2) > minKeyLength and not key1 > key2:
				length = min(len(key1), len(key2))
				keystream = QuagmireIII(alphabet, "KRYPTOS", key1[:length], "K").encrypt(key2[:length])
				plaintext = QuagmireIII(alphabet, "KRYPTOS", keystream, "K").decrypt(ciphertext[:length])
				if not validityText(dictionary, {}, plaintext).isdisjoint({"beginnings", "words", "words_beginnings"}):
					newLength = length + len(plaintext)
					keystream = encrypt(lookup, (key1 + plaintext)[length:newLength], (key2 + plaintext)[length:newLength])
					newPlaintext = QuagmireIII(alphabet, "KRYPTOS", keystream, "K").decrypt(ciphertext[length:newLength])
					if len(validityText(dictionary, {}, newPlaintext)) != 0:
						results.write(key1 + "\t" + key2 + "\t" + plaintext + " " + newPlaintext + "\n")
				attempts += 1
				if attempts % attemptsPerMessage == 0:
					print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + key1 + ", " + key2)

# Close files.
results.close()
