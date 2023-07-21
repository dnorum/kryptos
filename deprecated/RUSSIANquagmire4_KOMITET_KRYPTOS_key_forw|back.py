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
possibleHits = open("RUSSIANquagmire4_KOMITET_KRYPTOS_key_forw|back.output", 'w', 1)
possibleHits.write(" Frequency Deviation Threshold:" + str(threshold) + "\n")

# Loop over the dictionary.
i = 1
dictionaryFile = open("resources/dictionaries/words_russian.txt", 'r')
for word in dictionaryFile:
	word = word.rstrip()
	for letter in alphabet.characters:
		# Create the ciphers.
		q1 = QuagmireIV(alphabet, word, "KRYPTOS", "KOMITET", letter)
		q2 = QuagmireIV(alphabet, word, "KOMITET", "KRYPTOS", letter)
		q3 = QuagmireIV(alphabet, "KRYPTOS", word, "KOMITET", letter)
		q4 = QuagmireIV(alphabet, "KOMITET", word, "KRYPTOS", letter)
		# Try the ciphertext forwards.
		plaintext1 = q1.decrypt(ciphertext)
		plaintext2 = q2.decrypt(ciphertext)
		plaintext3 = q3.decrypt(ciphertext)
		plaintext4 = q4.decrypt(ciphertext)
		# Calculate statistics and output.
		rating1 = distributionDeviation(createDistribution(plaintext1, alphabet), referenceDistribution)
		rating2 = distributionDeviation(createDistribution(plaintext2, alphabet), referenceDistribution)
		rating3 = distributionDeviation(createDistribution(plaintext3, alphabet), referenceDistribution)
		rating4 = distributionDeviation(createDistribution(plaintext4, alphabet), referenceDistribution)
		if rating1 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + word + "," + "KRYPTOS" + "," + "KOMITET" + "," + letter + "," + str(rating1) + "\n"
			possibleHits.write(attempt)
		if rating2 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + word + "," + "KOMITET" + "," + "KRYPTOS" + "," + letter + "," + str(rating2) + "\n"
			possibleHits.write(attempt)
		if rating3 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + "KRYPTOS" + "," + word + "," + "KOMITET" + "," + letter + "," + str(rating3) + "\n"
			possibleHits.write(attempt)
		if rating4 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "forwards" + "," + "KOMITET" + "," + word + "," + "KRYPTOS" + "," + letter + "," + str(rating4) + "\n"
			possibleHits.write(attempt)
		# Try the ciphertext backwards.
		plaintext1 = q1.decrypt(ciphertextBackwards)
		plaintext2 = q2.decrypt(ciphertextBackwards)
		plaintext3 = q3.decrypt(ciphertextBackwards)
		plaintext4 = q4.decrypt(ciphertextBackwards)
		# Calculate statistics and output.
		rating1 = distributionDeviation(createDistribution(plaintext1, alphabet), referenceDistribution)
		rating2 = distributionDeviation(createDistribution(plaintext2, alphabet), referenceDistribution)
		rating3 = distributionDeviation(createDistribution(plaintext3, alphabet), referenceDistribution)
		rating4 = distributionDeviation(createDistribution(plaintext4, alphabet), referenceDistribution)
		if rating1 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + word + "," + "KRYPTOS" + "," + "KOMITET" + "," + letter + "," + str(rating1) + "\n"
			possibleHits.write(attempt)
		if rating2 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + word + "," + "KOMITET" + "," + "KRYPTOS" + "," + letter + "," + str(rating2) + "\n"
			possibleHits.write(attempt)
		if rating3 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + "KRYPTOS" + "," + word + "," + "KOMITET" + "," + letter + "," + str(rating3) + "\n"
			possibleHits.write(attempt)
		if rating4 <= threshold:
			attempt = "QUAGMIRE IV" + "," + "backwards" + "," + "KOMITET" + "," + word + "," + "KRYPTOS" + "," + letter + "," + str(rating4) + "\n"
			possibleHits.write(attempt)
		if i % 10000 == 0:
			print str(i)
		i += 1

# Close the files.
dictionaryFile.close()
possibleHits.close()
