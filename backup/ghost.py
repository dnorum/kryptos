import datetime

# Load all necessary packages.
exec(open("packages/alphabet.py").read())
exec(open("packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Define the two segments of keystream.
keystreams = ["ELYOIECBAQK", "RDUMRIYWOYNKY"]

# Define invalidating strings.
invalidStrings = {"AAA"}

# Define dictionary functions / classes.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			word = line.strip().upper()
			if len(word) != 1 or word in {"A", "I", "Q", "X"}:
				dictionary.add(word)
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

# Load dictionary for the first key.
dictionaryName = "10kwords_pruned"
dictionaryFilename = "resources/dictionaries/" + dictionaryName + ".txt"
words = loadDictionaryFile(dictionaryFilename)
beginnings = extractBeginnings(words)
middles = extractMiddles(words)
endings = extractEndings(words)

# 1kwords	1,000
# 10kwords	10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:
# 1kwords
# 10kwords
# 3esl

# In progress:
# english3

# Bundle it up.
dictionary = Dictionary(words, beginnings, middles, endings)

# Open output file.
filename = "ghost"
results = open(filename + "_" + dictionaryName + ".output", 'w', 1)
results.write("Text 1\tText2\n")
attemptsPerMessage = 10000

# Define search function.
def ghostSearch(dictionary, invalidStrings, alphabet, text1, text2, keystream, attempts, attemptsPerMessage, results):
	for letter1 in alphabet.characters:
		for letter2 in alphabet.characters:
			attempts += 1
			if attempts % attemptsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + text1 + ", " + text2)
			if QuagmireIII(alphabet, "KRYPTOS", letter1, "K").encrypt(letter2) == keystream[0]:
				newText1 = text1 + letter1
				newText2 = text2 + letter2
				if len(validityText(dictionary, invalidStrings, newText1)) * len(validityText(dictionary, invalidStrings, newText2)) != 0:
					# Valid extension found.
					if len(keystream) == 1:
						results.write(newText1 + "\t" + newText2 + "\n")
					else:
						attempts = ghostSearch(dictionary, invalidStrings, alphabet, newText1, newText2, keystream[1:], attempts, attemptsPerMessage, results)
	return attempts

# Search.
for keystream in keystreams:
	ghostSearch(dictionary, invalidStrings, alphabet, "", "", keystream, 0, attemptsPerMessage, results)

# Close files.
results.close()
