# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/statistics.py")
execfile("packages/vigenere.py")
execfile("packages/quagmire/quagmire4.py")

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
ciphertextBackwards = ciphertext[::-1]

# Set up the output file.
possibleHits = open("quagmire4_KOMITET_KRYPTOS_forw|back.output", 'w', 1)
possibleHits.write(" Frequency Deviation Threshold:" + str(threshold) + "\n")

# Loop over the dictionary.
i = 1
dictionaryFile = open("resources/dictionaries/words_alpha.txt", 'r')
for word in dictionaryFile:
	word = word.rstrip()
	for letter in alphabet.characters:
		# Create the ciphers.
		q1 = QuagmireIV(alphabet, "KRYPTOS", "KOMITET", word, letter)
		q2 = QuagmireIV(alphabet, "KOMITET", "KRYPTOS", word, letter)
		# Try the ciphertext forwards.
		plaintext1 = q1.decrypt(ciphertext)
		plaintext2 = q2.decrypt(ciphertext)
		# Calculate statistics and output.
		rating1 = distributionDeviation(createDistribution(plaintext1, alphabet), referenceDistribution)
		rating2 = distributionDeviation(createDistribution(plaintext2, alphabet), referenceDistribution)
		if rating1 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + "KRYPTOS" + "," + "KOMITET" + "," + word + "," + letter + "," + str(rating1) + "\n"
			possibleHits.write(attempt)
		if rating2 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + "KOMITET" + "," + "KRYPTOS" + "," + word + "," + letter + "," + str(rating2) + "\n"
			possibleHits.write(attempt)
		# Try the ciphertext backwards.
		plaintext1 = q1.decrypt(ciphertextBackwards)
		plaintext2 = q2.decrypt(ciphertextBackwards)
		# Calculate statistics and output.
		rating1 = distributionDeviation(createDistribution(plaintext1, alphabet), referenceDistribution)
		rating2 = distributionDeviation(createDistribution(plaintext2, alphabet), referenceDistribution)
		if rating1 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + "KRYPTOS" + "," + "KOMITET" + "," + word + "," + letter + "," + str(rating1) + "\n"
			possibleHits.write(attempt)
		if rating2 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + "KOMITET" + "," + "KRYPTOS" + "," + word + "," + letter + "," + str(rating2) + "\n"
			possibleHits.write(attempt)
		if i % 10000 == 0:
			print str(i)
		i += 1

# Close the files.
dictionaryFile.close()
possibleHits.close()
