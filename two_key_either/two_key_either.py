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
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
cipherAlphabet.key("KRYPTOS")
plainAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plainAlphabet.key("KRYPTOS")

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
keystreamSegments = ["RDUMRIYWOYNKY", "ELYOIECBAQK"]

# Define the minimum LCM length of the keystream.
minPeriod = 0
for segment in keystreamSegments:
	minPeriod = max(minPeriod, len(segment))

# 1kwords	1,000
# 10kwords	10,000
# 3esl		~22,000
# english3	~190,000
# words_alpha	~370,000
# dictionary_english_russian	~1,892,000

# Scanned to no avail:

# In progress:
# english3

# Define dictionary functions / classes.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return sorted(dictionary)

# Load dictionary.
dictionaryName = "english3"
dictionaryFilename = "../resources/dictionaries/" + dictionaryName + ".txt"
dictionary = loadDictionaryFile(dictionaryFilename)

# Open output file.
filename = "two_key"
results = open(filename + "_" + dictionaryName + ".output", 'w', 1)
results.write("Key1\tKey2\tStream\n")

# Set logging rate.
attemptsPerMessage = 10000

# Loop over the possible combinations of keys.
attempts = 0
for key1 in dictionary:
	for key2 in dictionary:
		# Avoid repetition.
		if key1 < key2:
			# If the keys' lengths' LCM is above the threshold, test them.
			keyLength1 = len(key1)
			keyLength2 = len(key2)
			leastCommonMultiple = lcm(keyLength1, keyLength2)
			if leastCommonMultiple > minPeriod:
				# Generate repeating portion of combined keystream.
				keystream1 = key1 * (leastCommonMultiple // keyLength1)
				keystream2 = key2 * (leastCommonMultiple // keyLength2)
				keystream = encrypt(lookup, keystream1, keystream2)
				# Test for presence of known keystream segments.
				for segment in keystreamSegments:
					if segment in keystream:
						results.write(key1 + "\t" + key2 + "\t" + segment + "\n")
			attempts += 1
			if attempts % attemptsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + key1 + ", " + key2)

# Close output file.
results.close()
