import datetime
import math

# Li'l kludge to work around out-of-date math lib.
def lcm(x, y):
	return (x * y) // (math.gcd(x, y))

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

# Define the two segments of keystream.
segment1 = "RDUMRIYWOYNKY"
segment2 = "ELYOIECBAQK"

# Define the minimum LCM length of the combined keystream.
minPeriod = 24

# 1kwords	1,000
# 10kwords	10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:
# 1kwords

# In progress:
# english3_pruned

# Define dictionary functions / classes.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return sorted(dictionary)

# Load dictionary for the first key.
dictionaryName = "english3_pruned"
dictionaryFilename = "../resources/dictionaries/" + dictionaryName + ".txt"

dictionary = loadDictionaryFile(dictionaryFilename)

# Open output file.
filename = "three_key"
results = open(filename + ".output", 'w', 1)
results.write("Key1\tKey2\tKey3\tStream\n")

# Set logging rate.
attemptsPerMessage = 10000
attempts = 0

# Loop over the possible combinations of keys.
for word1 in dictionary:
	for word2 in dictionary:
		# Avoid repetition.
		if word2 < word1:
			continue
		for word3 in dictionary:
			if word3 < word2 or word3 < word1:
				continue
			# If the keys' lengths' LCM is above the threshold, test them.
			keyLength1 = len(word1)
			keyLength2 = len(word2)
			keyLength3 = len(word3)
			leastCommonMultiple = lcm(lcm(keyLength1, keyLength2), keyLength3)
			if leastCommonMultiple > minPeriod:
				keystream1 = word1 * (leastCommonMultiple // keyLength1)
				keystream2 = word2 * (leastCommonMultiple // keyLength2)
				keystream3 = word3 * (leastCommonMultiple // keyLength3)
				keystream = encrypt(lookup, keystream1, encrypt(lookup, keystream2, keystream3))
				# Test for presence of known keystream segments.
				if (segment1 in keystream) and (segment2 in keystream):
					results.write(word1 + "\t" + word2 + "\t" + word3 + "\t" + keystream + "\n")
			attempts += 1
			if attempts % attemptsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + word1 + ", " + word2 + ", " + word3)

# Close output file.
results.close()
