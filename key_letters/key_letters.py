import datetime

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Define the keystream to target.
segment = "RDUMRIYWOYNKY"
#segment = "ELYOIECBAQK"
targetKeystreamLetters = set()
for letter in segment:
	targetKeystreamLetters.add(letter)

# Construct lookup for letters.
lookup = dict()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		pair = letter1 + letter2
		keystreamLetter = QuagmireIII(alphabet, "KRYPTOS", letter1, "K").encrypt(letter2)
		lookup[pair] = keystreamLetter

# Function to return all length-n strings of distinct letters.
# Can be optimized with a bit-mapping...
def distinctStrings(n, alphabet):
	if n > len(alphabet.characters):
		return set()
	length = 1
	strings = set()
	for letter in alphabet.characters:
		strings.add(letter)
	while length < n:
		newStrings = set()
		for string in strings:
			for letter in alphabet.characters:
				if letter not in string:
					newString = "".join(sorted(string + letter))
					newStrings.add(newString)
		strings = newStrings
		length += 1
	return sorted(strings)

# Set logging.
attemptsPerMessage = 100000
attempts = 0

# Search.
for i in range(1,len(alphabet.characters)):
	filename = "key_letters_" + str(i) + ".output"
	results = open(filename, 'w', 1)
	results.write("Key Letters\tKeystream Letters\n")
	strings = distinctStrings(i, alphabet)
	for string in strings:
		keystreamLetters = set()
		for letter1 in string:
			for letter2 in string:
				keystreamLetters.add(lookup[letter1 + letter2])
		attempts += 1
		if targetKeystreamLetters.issubset(keystreamLetters):
			keystream = ""
			for letter in sorted(keystreamLetters):
				keystream += letter
			results.write(string + "\t" + keystream + "\n")
		if attempts % attemptsPerMessage == 0:
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + string)
	results.close()
