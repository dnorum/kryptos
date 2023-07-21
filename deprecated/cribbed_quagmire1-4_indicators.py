# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/statistics.py")
execfile("packages/vigenere.py")
execfile("packages/quagmire/quagmire1.py")
execfile("packages/quagmire/quagmire2.py")
execfile("packages/quagmire/quagmire3.py")
execfile("packages/quagmire/quagmire4.py")

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

# Calculate the period of an indicator series.
def findPeriod(array):
	maxPeriod = len(array)
	for period in range(1, maxPeriod):
		if array[period:maxPeriod] == array[0:maxPeriod-period]:
			return period
	return maxPeriod

# Loop over the dictionary.
i = 1
with open("resources/dictionaries/words_english_russian.txt", 'r') as dictionary:
	words = set(word.rstrip() for word in dictionary)

for word in words:
	word = word.rstrip()

	#ciphertext(cipher) = plaintext(plaintext) - plaintext(indicatorLetter) + ciphertext(indicatorOffset)

	# Quagmire I
	plainAlphabet.key(word)
	cipherAlphabet.sort()
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QI," + word + "," + str(indicatorSeries) + "," + str(findPeriod(indicatorSeries)) + "\n"
	indicatorFile.write(output)
	plainAlphabet.sort()

	# Quagmire II
	plainAlphabet.sort()
	cipherAlphabet.key(word)
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QII," + word + "," + str(indicatorSeries) + "," + str(findPeriod(indicatorSeries)) + "\n"
	indicatorFile.write(output)
	cipherAlphabet.sort()

	# Quagmire III
	plainAlphabet.key(word)
	cipherAlphabet.key(word)
	indicatorSeries = []
	for i in range(0,len(plaintext)):
		indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
		- plainAlphabet.encodeCharacter(plaintext[i])
		indicatorSeries.append(indicator % modAlphabet)
	output = "QIII," + word + "," + str(indicatorSeries) + "," + str(findPeriod(indicatorSeries)) + "\n"
	indicatorFile.write(output)
	plainAlphabet.sort()
	cipherAlphabet.sort()

	# Quagmire IV
	for key in ["KRYPTOS", "KOMITET"]:
		plainAlphabet.key(key)
		cipherAlphabet.key(word)
		indicatorSeries = []
		for i in range(0,len(plaintext)):
			indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
			- plainAlphabet.encodeCharacter(plaintext[i])
			indicatorSeries.append(indicator % modAlphabet)
		output = "QIV," + key + "," + word + "," + str(indicatorSeries) + "," + str(findPeriod(indicatorSeries)) + "\n"
		indicatorFile.write(output)
		plainAlphabet.sort()
		cipherAlphabet.sort()

		plainAlphabet.key(word)
		cipherAlphabet.key(key)
		indicatorSeries = []
		for i in range(0,len(plaintext)):
			indicator = cipherAlphabet.encodeCharacter(ciphertext[i]) \
			- plainAlphabet.encodeCharacter(plaintext[i])
			indicatorSeries.append(indicator % modAlphabet)
		output = "QIV," + word + "," + key + "," + str(indicatorSeries) + "," + str(findPeriod(indicatorSeries)) + "\n"
		indicatorFile.write(output)
		plainAlphabet.sort()
		cipherAlphabet.sort()

	if i % 10000 == 0:
		print str(i)
	i += 1

# Close the file.
indicatorFile.close()
