import datetime
import numpy

# Load all necessary packages.
exec(open("packages/alphabet.py").read())
exec(open("packages/quagmire.py").read())

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

# In progress:
# 10kwords

# Load dictionary for the first key.
dictionaryName = "10kwords"
dictionaryFilename = "resources/dictionaries/" + dictionaryName + ".txt"
keyDictionary1 = open(dictionaryFilename, 'r')

# Open output file.
filename = "key_autokey_beginnings_" + dictionaryName
results = open(filename + ".output", 'w', 1)
results.write("Length\tKey\tKey Segment\tWord\tKeystream\n")

# Set logging rate and minimum word length.
attemptsPerMessage = 10000

# Loop over the possible combinations of keys and stream fragment.
attempts = 0
hits = set()
for word1 in keyDictionary1:

	# Resuming...
	if word1.strip().upper() < "DISEASE":
		continue

	# Clean up and double-up the key to account for offsets.
	key = word1.strip().upper() * 2
	# Create key substrings.
	keySubstrings = substringsByLength(key)
	# Load the dictionary for the stream fragment.
	keyDictionary2 = open(dictionaryFilename, 'r')
	for word2 in keyDictionary2:
		word = word2.strip().upper()
		for i in range(0, len(word)):
			beginning = word[-(i+1):]
			length = len(beginning)
			if length < len(key) and length < min(len(segment1), len(segment2)):
				for keySegment in keySubstrings[length]:
					keystreamFragment = QuagmireIII(alphabet, "KRYPTOS", keySegment, "K").encrypt(beginning)
					if (keystreamFragment == segment1[:length]) or (keystreamFragment == segment2[:length]):
						hit = str(length) + "\t" + word1.strip().upper() + "\t" + keySegment + "\t" + beginning + "\t" + keystreamFragment + "\n"
						if hit not in hits:
							results.write(hit)
							hits.add(hit)
				attempts += 1
				if attempts % attemptsPerMessage == 0:
					print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + word1.strip().upper() + ", " + beginning)
	keyDictionary2.close()

# Close files.
keyDictionary1.close()
results.close()
