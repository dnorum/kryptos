import datetime

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

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

# Define the ciphertext.
ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

# 1kwords	1,000
# 10kwords	10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:
# 1kwords
# 10kwords_pruned

# In progress:
# english3_pruned

# Define dictionary function.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return sorted(dictionary)

# Define ghost class.
def addHook(string, character):
	if character in string:
		return string
	else:
		newString = "".join(sorted(string + character))
		return newString
def ghostLookup(dictionary):
	lookup = dict()
	for word in dictionary:
		length = len(word)
		if not word in lookup:
			lookup[word] = " "
		else:
			lookup[word] = addHook(lookup[word], " ")
		if length > 1:
			for i in range(1, length):
				beginning = word[:i]
				if not beginning in lookup:
					lookup[beginning] = word[i]
				else:
					lookup[word] = addHook(lookup[word], word[i])
	return lookup

def findGhost(ghostLookup, string, extension):
	found = False
	if string == "" and extension == "":
		return found
	if string in ghostLookup and extension == "":
		return True
	if string == "":
		found = found or findGhost(ghostLookup, extension[0], extension[1:])
	if string not in ghostLookup:
		return found
	found = found or findGhost(ghostLookup, string + extension[0], extension[1:])
	if " " in ghostLookup[string]:
		found = found or findGhost(ghostLookup, "", extension)
	return found

# Load dictionary.
dictionaryName = "english3_pruned"
dictionaryFilename = "../resources/dictionaries/" + dictionaryName + ".txt"
dictionary = loadDictionaryFile(dictionaryFilename)

# Create ghostLookup.
ghostLookup = ghostLookup(dictionary)

# Open output file.
filename = "ghost_beginning"
results = open(filename + "_" + dictionaryName + ".output", 'w', 1)
results.write("Stream1\tStream2\tCipher\tLength\n")

# Set logging rate.
attemptsPerMessage = 10000

# Initialize streams.
streams = set()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		stream = letter1 + " " + letter2 + " " + lookup[letter1 + letter2]
		streams.add(stream)
# Loop over the possible combinations of streams.
attempts = 0
minLength = 9
extended = True
while extended:
	newStreams = set()
	extended = False
	for stream in streams:
		streamComponents = stream.split()
		stream1 = streamComponents[0]
		stream2 = streamComponents[1]
		cipher = streamComponents[2]
		if attempts % attemptsPerMessage == 0:
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + stream1 + ", " + stream2)
		for letter1 in alphabet.characters:
			newStream1 = stream1 + letter1
			if not findGhost(ghostLookup, "", newStream1):
				continue
			for letter2 in alphabet.characters:
				newStream2 = stream2 + letter2
				if not findGhost(ghostLookup, "", newStream2):
					continue
				newCipher = cipher + lookup[letter1 + letter2]
				if newCipher != ciphertext[:len(newCipher)]:
					continue
				if len(newCipher) > minLength:				
					results.write(newStream1 + "\t" + newStream2 + "\t" + newCipher + "\t" + str(len(newCipher)) + "\n")
				newStreams.add(newStream1 + " " + newStream2 + " " + newCipher)
				extended = True
	streams = newStreams

# Close output file.
results.close()
