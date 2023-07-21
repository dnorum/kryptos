execfile("packages/alphabet.py")

# Open the raw log file.
indicatorFile = open("cribbed_quagmire1-4_indicators.output", 'r')

# Open the output file.
outputFile = open("cribbed_quagmire1-4_indicators_words.output", 'w', 1)

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plainAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Turn the dictionary into a set for checking words.
with open("resources/dictionaries/dictionary_english_russian.txt", 'r') as dictionary:
	words = set(word.rstrip() for word in dictionary)

def is_word(word):
	return word in words

# Scan over the indicators.
indicatorsTested = 1
for line in indicatorFile:

	chunkedLine = line.split("\t")

	cipher = chunkedLine[0]
	indicator = map(int, chunkedLine[-2][1:-1].split(","))
	periods = map(int, chunkedLine[-1][1:-2].split(","))

	# Break apart by cipher.
	if cipher == "QI":
		plainAlphabet.key(chunkedLine[1])
		cipherAlphabet.sort()
	if cipher == "QII":
		plainAlphabet.sort()
		cipherAlphabet.key(chunkedLine[1])
	if cipher == "QIII":
		plainAlphabet.key(chunkedLine[1])
		cipherAlphabet.key(chunkedLine[1])
	if cipher == "QIV":
		plainAlphabet.key(chunkedLine[1])
		cipherAlphabet.key(chunkedLine[2])

	for period in periods:
		for i in range(0,alphabet.modulus()):
			indicatorKey = "".join(cipherAlphabet.decodeString([(character + i) % alphabet.modulus() for character in indicator])[0:period])
			for j in range(0,len(indicatorKey)):
				if is_word(indicatorKey[j:] + indicatorKey[:j]):
					print("HIT: " + line.rstrip() + " // " + indicatorKey + ", " + plainAlphabet.decodeCharacter(i) + "\n")
					outputFile.write(line.rstrip() + " // " + indicatorKey + ", " + plainAlphabet.decodeCharacter(i) + "\n")

	if indicatorsTested % 10000 == 0:
		print str(indicatorsTested) + "," + line.rstrip()
	indicatorsTested += 1

# Close the files.
indicatorFile.close()
outputFile.close()
