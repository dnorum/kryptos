# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/formatting.py")
execfile("packages/quagmire.py")

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plainAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Load the crib.
cribFile = open("resources/cribs/kryptos4.txt", 'r')
ciphertext = cribFile.readline()
ciphertext = alphabet.scrub(ciphertext)
plaintext = cribFile.readline()
plaintext = alphabet.scrub(plaintext)
assert len(ciphertext) == len(plaintext)
cribFile.close()

# Set up the output file.
indicatorFile = open("cribbed_quagmire1-4_indicators.output", 'w', 1)

# Loop over the dictionary.
with open("resources/dictionaries/dictionary_english_russian.txt", 'r') as dictionary:
	words = set(word.rstrip() for word in dictionary)
words = sorted(words)

nWords = 1
for word in words:

	#ciphertext(cipher) = plaintext(plaintext) - plaintext(indicatorLetter) + ciphertext(indicatorOffset)

	# Quagmire I
	plainAlphabet.key(word)
	cipherAlphabet.sort()
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QI\t" + word + "\t" + str(indicatorSeries) + "\t" + str(periodicities(indicatorSeries)) + "\n"
	indicatorFile.write(output)

	# Quagmire II
	plainAlphabet.sort()
	cipherAlphabet.key(word)
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QII\t" + word + "\t" + str(indicatorSeries) + "\t" + str(periodicities(indicatorSeries)) + "\n"
	indicatorFile.write(output)
	
	# Quagmire III
	plainAlphabet.key(word)
	cipherAlphabet.key(word)
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QIII\t" + word + "\t" + str(indicatorSeries) + "\t" + str(periodicities(indicatorSeries)) + "\n"
	indicatorFile.write(output)

	# Quagmire IV
	for key in ["KRYPTOS", "KOMITET"]:
		plainAlphabet.key(key)
		cipherAlphabet.key(word)
		indicatorSeries = []
		for i in range(0,len(plaintext)):
			indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
			- plainAlphabet.encodeCharacter(plaintext[i])
			indicatorSeries.append(indicator % modAlphabet)
		output = "QIV\t" + key + "\t" + word + "\t" + str(indicatorSeries) + "\t" + str(periodicities(indicatorSeries)) + "\n"
		indicatorFile.write(output)

		plainAlphabet.key(word)
		cipherAlphabet.key(key)
		indicatorSeries = []
		for i in range(0,len(plaintext)):
			indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
			- plainAlphabet.encodeCharacter(plaintext[i])
			indicatorSeries.append(indicator % modAlphabet)
		output = "QIV\t" + word + "\t" + key + "\t" + str(indicatorSeries) + "\t" + str(periodicities(indicatorSeries)) + "\n"
		indicatorFile.write(output)

	if nWords % 10000 == 0:
		print str(nWords) + ", " + word
	nWords += 1

# Close the file.
indicatorFile.close()
