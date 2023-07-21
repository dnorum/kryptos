# Load all necessary packages.
execfile("../../packages/alphabet.py")
execfile("../../packages/formatting.py")
execfile("../../packages/statistics.py")
execfile("../../packages/vigenere.py")
execfile("../../packages/quagmire/quagmire1.py")
execfile("../../packages/quagmire/quagmire2.py")
execfile("../../packages/quagmire/quagmire3.py")
execfile("../../packages/quagmire/quagmire4.py")

# Define the alphabet and reference distribution.
referenceDistribution = loadDistribution("../../resources/reference_distribution.txt")
alphabet = referenceDistribution.alphabet

# Load the ciphertext.
ciphertextFile = open("../../resources/ciphertexts/kryptos4.txt", 'r')
ciphertext = ciphertextFile.read()
ciphertextFile.close()
ciphertext = alphabet.scrub(ciphertext)
ciphertextBackwards = ciphertext[::-1]

# Set up the output files.
forwardsAttempts = open("KRYPTOS_forwards.output", 'w')
backwardsAttempts = open("KRYPTOS_backwards.output", 'w')

# Loop over the dictionary.
dictionaryFile = open("../../resources/dictionaries/7letter.txt", 'r')
for word in dictionaryFile:
	word = word.rstrip()
	for letter in alphabet.characters:
		# Try the ciphertext forwards.
		plaintext = QuagmireII(alphabet, "KRYPTOS", word, letter).decrypt(ciphertext)
		# Calculate statistics and output.
		distribution = createDistribution(plaintext, alphabet)
		attempt = "KRYPTOS" + "," + word + "," + letter + "," + str(distributionDeviation(distribution, referenceDistribution)) + "\n"
		forwardsAttempts.write(attempt)

		# Try the ciphertext backwards.
		plaintext = QuagmireII(alphabet, "KRYPTOS", word, letter).decrypt(ciphertextBackwards)
		# Calculate statistics and output.
		distribution = createDistribution(plaintext, alphabet)
		attempt = "KRYPTOS" + "," + word + "," + letter + "," + str(distributionDeviation(distribution, referenceDistribution)) + "\n"
		backwardsAttempts.write(attempt)

# Close the files.
dictionaryFile.close()
forwardsAttempts.close()
backwardsAttempts.close()
