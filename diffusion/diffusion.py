import datetime

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Construct lookup for letters.
lookupEncrypt = dict()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		pair = letter1 + letter2
		keystreamLetter = QuagmireIII(alphabet, "KRYPTOS", letter1, "K").encrypt(letter2)
		lookupEncrypt[pair] = keystreamLetter

lookupDecrypt = dict()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		pair = letter1 + letter2
		keystreamLetter = QuagmireIII(alphabet, "KRYPTOS", letter1, "K").decrypt(letter2)
		lookupDecrypt[pair] = keystreamLetter

def crypt(lookup, string1, string2):
	if len(string1) != len(string2):
		raise Error
	result = ""
	for i in range(0, len(string1)):
		result += lookup[string1[i] + string2[i]]
	return result

# Load distribution.
frequency = dict()
with open("../resources/distribution.txt") as source:
	for line in source:
		frequency[line[0]] = float(line[2:])

# Open output file.

for letter in alphabet.characters:
	filename = "diffusion.output"
	results = open(filename, 'w', 1)
	

# Close output file.
results.close()
