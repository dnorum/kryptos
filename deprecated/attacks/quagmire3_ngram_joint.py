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
results = open("quagmire3_3gram_joint2.output", 'w', 1)
results.write("Offset,Key1,Rank1,Key2,Rank2,RankMult\n")

# Loop over the Ngrams.
ngrams = LoadNgrams("resources/ngrams/3grams.txt")
n = 3
for key in ngrams:
	for x in range(len(ciphertext)-n+1):
		plain = QuagmireIII(alphabet, "KRYPTOS", key, "K").decrypt(ciphertext[x:x+n])
		rank = ngrams[key]
		if plain in ngrams:
			results.write(str(x) + "," + key + "," + str(rank) + "," + plain + "," + str(ngrams[plain]) + "," + str(ngrams[plain]+rank) + "\n")

# Close the files.
results.close()
