# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/ngram.py")
execfile("packages/statistics.py")
execfile("packages/vigenere.py")
execfile("packages/quagmire.py")

# Define the alphabet and reference distribution.
referenceDistribution = loadDistribution("resources/reference_distribution.txt")
alphabet = referenceDistribution.alphabet

# Load the ciphertext.
ciphertext = "RDUMRIYWOYNKY"

# Set up the output file.
results = open("quagmire3_dict_joint.output", 'w', 1)
dictionaryFile = open("resources/dictionaries/words_alpha.txt", 'r')

ngrams = LoadNgrams("resources/ngrams/1grams.txt")
threegrams = LoadNgrams("resources/ngrams/3grams.txt")

for word in dictionaryFile:
	word = word.rstrip()
	n = len(word)
	if n > 3:
		for x in range(len(ciphertext)-n+1):
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
			rank = 0
			for character in plain:
				rank += ngrams[character]
			rank = float(rank) / float(n)
			threerank = 0
			mapped = 1
			for y in range(len(plain)-2):
				found = 0
				if plain[y:y+3] in threegrams:
					threerank += threegrams[plain[y:y+3]]
					found = 1
				mapped *= found
			threerank = float(threerank) / float(len(plain)-2)
			if mapped == 1 and rank < 10:
				results.write(str(x) + "," + word + "," + plain + "," + str(rank) + "," + str(threerank) + "\n")

# Close the files.
results.close()
