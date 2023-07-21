import datetime

execfile("packages/alphabet.py")
execfile("packages/language.py")
execfile("packages/quagmire.py")

# Define filenames and settings.
filename = "quote_genetic_attack"
alphabetFile = "resources/reference_distribution.txt"
dictionaryFilename = "resources/dictionaries/3esl.txt"
languageFilename = dictionaryFilename
countsFilename = "resources/frequency_lists/written.num"
countsFileSeparator = " "
countsFileBaseline = 89740556.0

# Load resources.
alphabet = loadDistribution(alphabetFile).alphabet
language = loadLanguage(languageFilename)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Loading word-frequency distribution from " + countsFilename + ".")
frequencies = loadFrequenciesFromCounts(countsFilename, countsFileSeparator, alphabet, countsFileBaseline)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Loading word-rank distribution from " + countsFilename + ".")
ranks = loadRanksFromCounts(countsFilename, countsFileSeparator, alphabet)

ciphertext = "RDUMRIYWOYNKY"
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Targeting ciphertext: " + ciphertext)

# Open the dictionary.
dictionaryFile = open(dictionaryFilename, 'r')

# Open the initial output file for the base codons.
results = open(filename + ".output", 'w', 1)
results.write("Length\tKey\tPosition\tPlaintext\tStatus\n")

# Set output frequencies.
wordsPerMessage = 1000
triesPerMessage = 1000000
resultsPerMessage = 10000

# Open final evaluation file.
finalResults = open(filename + "_evaluation.output", 'w', 1)
finalResults.write("Length\tKey\tPosition\tPlaintext\tStatus\tFrequencies\tRanks\n")

# Define evaluation function.
def printEvaluation(codon, frequencies, outputFile):
	result_frequency = (evaluateFrequency(codon.sequence, frequencies) + evaluateFrequency(codon.expression, frequencies)) / 2.0
	result_rank = (evaluateRank(codon.sequence, ranks) + evaluateRank(codon.expression, ranks)) / 2.0
	frequencyFormatted = "{:.2e}".format(result_frequency)
	rankFormatted = "{:.2e}".format(result_rank)
	outputFile.write(codon.toString("\t") + "\t" + frequencyFormatted + "\t" + rankFormatted + "\n")
	return "Success"

# Brute-force codons.
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for base-level codons.")
codons = []
nwords = 0
length_ciphertext = len(ciphertext)
completedGenes = []
for word in dictionaryFile:
	word = word.rstrip().upper()
	n = len(word)
	if n <= length_ciphertext:
		for x in range(len(ciphertext)-n+1):
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
			status = language.verify(plain)
			if status != set("unverified"):
				new_codon = Codon(x, word, plain, status)
				if new_codon.length == length_ciphertext:
					printEvaluation(new_codon, frequencies, finalResults)
				else:
					results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
					codons.append(new_codon)
		nwords += 1
		if nwords % wordsPerMessage == 0:
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)
dictionaryFile.close()

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for initial codons.")
initial_codons = []
nwords = 0
for word in language.endings:
	if word not in language.words:
		n = len(word)
		if n <= length_ciphertext:
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[:n])
			status = language.verify(plain)
			if status != set("unverified"):
				results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
				new_codon = Codon(0, word, plain, status)
				if new_codon.length == length_ciphertext:
					printEvaluation(new_codon, frequencies, finalResults)
				else:
					initial_codons.append(new_codon)
			nwords += 1
			if nwords % wordsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for final codons.")
final_codons = []
nwords = 0
for word in language.beginnings:
	if word not in language.words:
		n = len(word)
		if n <= length_ciphertext:
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[-n:])
			status = language.verify(plain)
			if status != set("unverified"):
				results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
				new_codon = Codon(length_ciphertext - n, word, plain, status)
				if new_codon.length == length_ciphertext:
					printEvaluation(new_codon, frequencies, finalResults)
				else:
					final_codons.append(new_codon)
			nwords += 1
			if nwords % wordsPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)
results.close()

# Jam puzzle pieces together.
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Growing codons.")
next_codons = codons
codons = initial_codons
for codon in next_codons:
	if codon.start == 0:
		codons.append(codon)
next_codons.extend(final_codons)
geneLength = 3
for i in range(1, geneLength+1):
	print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Pass " + str(i) + ":")
	ntries = 0
	nextended = 0
	ncompleted = 0
	results = open(filename + "_round" + str(i) + ".output", 'w', 1)
	results.write("Length\tKey\tPosition\tPlaintext\tStatus\n")
	new_codons = []
	for codon in codons:
		extended = 0
		for next_codon in next_codons:
			newCodon = codon.add(next_codon, language)
			if newCodon != codon:
				extended = 1
				if (newCodon.start + newCodon.length) == length_ciphertext:
					printEvaluation(newCodon, frequencies, finalResults)
					ncompleted += 1
				else:
					new_codons.append(newCodon)
					results.write(newCodon.toString("\t") + "\n")
					nextended += 1
			ntries += 1
			if ntries % triesPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(ntries) + " attempts, " + str(nextended) + " genes extended, " + str(ncompleted) + " genes completed.")
		if extended == 0:
			printEvaluation(codon, frequencies, finalResults)
			ncompleted += 1
	results.close()
	codons = new_codons

# Group the results together to evaluate.
results.close()
