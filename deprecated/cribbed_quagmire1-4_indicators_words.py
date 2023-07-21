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
with open("resources/dictionaries/words_english_russian.txt", 'r') as dictionary:
	words = set(word.rstrip() for word in dictionary)

def is_word(word):
	return word in words

# Scan over the indicators.
indicatorsTested = 0
for line in indicatorFile:

	indicator = map(int, line[line.find("[")+1:line.find("]")].split(","))
	period = int(line[line.rfind(",")+1:-1])

	# Break apart by cipher.
	cipher = line[:line.find(",")-1]
	if cipher == "QI":
		plainAlphabet.sort()
		plainAlphabet.key(line.split(",")[1])
		cipherAlphabet.sort()
	if cipher == "QII":
		plainAlphabet.sort()
		cipherAlphabet.sort()
		cipherAlphabet.key(line.split(",")[1])
	if cipher == "QIII":
		plainAlphabet.sort()
		plainAlphabet.key(line.split(",")[1])
		cipherAlphabet.sort()
		cipherAlphabet.key(line.split(",")[1])
	if cipher == "QIV":
		plainAlphabet.sort()
		plainAlphabet.key(line.split(",")[1])
		cipherAlphabet.sort()
		cipherAlphabet.key(line.split(",")[2])

	for i in range(0,alphabet.modulus()):
		indicatorKey = "".join(cipherAlphabet.decodeString([(character + i) % alphabet.modulus() for character in indicator])[0:period])
		for j in range(0,len(indicatorKey)):
			if is_word(indicatorKey[j:] + indicatorKey[:j]):
				print(line.rstrip() + " // " + indicatorKey + ", " + plainAlphabet.decodeCharacter(i) + "\n")
				outputFile.write(line.rstrip() + " // " + indicatorKey + ", " + plainAlphabet.decodeCharacter(i) + "\n")

	if indicatorsTested % 10000 == 0:
		print str(indicatorsTested)
	indicatorsTested += 1

# Close the files.
indicatorFile.close()
outputFile.close()
