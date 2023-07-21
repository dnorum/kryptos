# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/statistics.py")
execfile("packages/vigenere.py")
execfile("packages/quagmire.py")

# Define the alphabet and reference distribution.
referenceDistribution = loadDistribution("resources/reference_distribution.txt")
alphabet = referenceDistribution.alphabet

# Set the threshold for recording a "hit"
threshold = 0.1

# Load the ciphertext.
ciphertextFile = open("resources/ciphertexts/kryptos4.txt", 'r')
ciphertext = ciphertextFile.read()
ciphertextFile.close()
ciphertext = alphabet.scrub(ciphertext)

# Set up the output file.
possibleHits = open("quagmire1-4_dictionary.output", 'w', 1)
possibleHits.write(" Frequency Deviation Threshold:" + str(threshold) + "\n")

# Loop over the dictionary.
nCiphers = 1
dictionaryFile = open("resources/dictionaries/dictionary_english_russian.txt", 'r')
for word in dictionaryFile:
	word = word.rstrip()
	for letter in alphabet.characters:
		# Create the ciphers.
		ciphers = []
		for key in ["KRYPTOS", "KOMITET"]:
			ciphers.append(QuagmireI(alphabet, key, word, letter))
			ciphers.append(QuagmireI(alphabet, word, key, letter))
			ciphers.append(QuagmireII(alphabet, key, word, letter))
			ciphers.append(QuagmireII(alphabet, word, key, letter))
			ciphers.append(QuagmireIII(alphabet, key, word, letter))
			ciphers.append(QuagmireIII(alphabet, word, key, letter))				
		ciphers.append(QuagmireIV(alphabet, "KRYPTOS", "KOMITET", word, letter))
		ciphers.append(QuagmireIV(alphabet, "KOMITET", "KRYPTOS", word, letter))
		ciphers.append(QuagmireIV(alphabet, "KRYPTOS", word, "KOMITET", letter))
		ciphers.append(QuagmireIV(alphabet, "KOMITET", word, "KRYPTOS", letter))
		ciphers.append(QuagmireIV(alphabet, word, "KRYPTOS", "KOMITET", letter))
		ciphers.append(QuagmireIV(alphabet, word, "KOMITET", "KRYPTOS", letter))
		# Try the ciphers.
		for cipher in ciphers:
			plaintext = cipher.decrypt(ciphertext)
			# Calculate statistics and output.
			rating = distributionDeviation(createDistribution(plaintext, alphabet), referenceDistribution)
			if rating <= threshold:
				possibleHits.write(cipher.string() + "," + str(rating) + "\n")
			if nCiphers % 10000 == 0:
				print str(nCiphers) + ", " + word + ", " + letter
			nCiphers += 1

# Close the files.
dictionaryFile.close()
possibleHits.close()
