import datetime
import numpy

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define substring function.
def substring(string, substringLength):
	result = []
	stringLength = len(string)
	if stringLength < substringLength or substringLength == 0:
		return result
	for i in range(0, stringLength - substringLength + 1):
		result.append(string[i:i+substringLength])
	return result

def substringsByLength(string):
	result = [[]]
	length = len(string)
	if length == 0:
		return result
	for i in range(1, length + 1):
		result.append(substring(string, i))
	return result

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
cipherAlphabet.key("KRYPTOS")
plainAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plainAlphabet.key("KRYPTOS")

# Define the two segments of keystream.
segment1 = "RDUMRIYWOYNKY"
segment2 = "ELYOIECBAQK"

# Create substrings for keystream.
keystreamSubstrings = substringsByLength(segment1)
substrings2 = substringsByLength(segment2)
for i in range(0, len(substrings2)):
	keystreamSubstrings[i] = numpy.concatenate((keystreamSubstrings[i], substrings2[i]))

# 1kwords	1,000
# 10kwords	10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:
# 1kwords
# 10kwords

# In progress:
# english3_pruned

def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return dictionary

# Load dictionary for the first key.
dictionaryName = "english3_pruned"
dictionaryFilename = "../resources/dictionaries/" + dictionaryName + ".txt"
keyDictionary1 = sorted(loadDictionaryFile(dictionaryFilename))
keyDictionary2 = sorted(loadDictionaryFile(dictionaryFilename))

# Open output file.
filename = "key_autokey_" + dictionaryName
results = open(filename + ".output", 'w', 1)
results.write("Length\tKey\tKey Segment\tWord\tKeystream\n")

# Set logging rate and minimum word length.
attemptsPerMessage = 10000
minWordLength = 3

# Loop over the possible combinations of keys and stream fragment.
attempts = 0
for word1 in keyDictionary1:
	# Clean up and double-up the key to account for offsets.
	key = word1 * 2
	# Create key substrings.
	keySubstrings = substringsByLength(key)
	for word2 in keyDictionary2:
		word = word2.strip().upper()
		length = len(word)
		if length < len(key) and length < min(len(segment1), len(segment2)) and length >= minWordLength:
			for keySegment in keySubstrings[length]:
				keystreamFragment = QuagmireIII(alphabet, "KRYPTOS", keySegment, "K").encrypt(word)
				if keystreamFragment in keystreamSubstrings[length]:
					results.write(str(length) + "\t" + word1.strip().upper() + "\t" + keySegment + "\t" + word + "\t" + keystreamFragment + "\n")
			attempts += 1
			if attempts % attemptsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + word1.strip().upper() + ", " + word)

# Close files.
results.close()
