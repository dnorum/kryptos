import datetime

execfile("packages/alphabet.py")
execfile("packages/language.py")
execfile("packages/quagmire.py")

# Define filenames and settings.
filename = "no_kill_overkill_but_organized"
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
wordsPerMessage = 100
triesPerMessage = 100000
resultsPerMessage = 10000

# Brute-force codons.
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for base-level codons.")
codons = []
nwords = 0
for word in dictionaryFile:
	word = word.rstrip().upper()
	n = len(word)
	for x in range(len(ciphertext)-n+1):
		plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
		status = language.verify(plain)
		if status != set("unverified"):
			results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
			codons.append(Codon(x, word, plain, status))
	nwords += 1
	if nwords % wordsPerMessage == 0:
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)
dictionaryFile.close()

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for initial codons.")
initial_codons = []
nwords = 0
for word in endings:
	if word not in words:
		n = len(word)
		for x in range(len(ciphertext)-n+1):
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
			status = language.verify(plain)
			if status != set("unverified"):
				results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
				initial_codons.append(Codon(x, word, plain, status))
		nwords += 1
		if nwords % wordsPerMessage == 0:
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Brute-force searching " + dictionaryFilename + " for final codons.")
final_codons = []
nwords = 0
for word in beginnings:
	if word not in words:
		n = len(word)
		for x in range(len(ciphertext)-n+1):
			plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
			status = language.verify(plain)
			if status != set("unverified"):
				results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\n")
				final_codons.append(Codon(x, word, plain, status))
		nwords += 1
		if nwords % wordsPerMessage == 0:
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(nwords) + ": " + word)
results.close()

# Jam puzzle pieces together.
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Growing codons.")
next_codons = codons
next_codons.extend(final_codons)
codons.extend(initial_codons)
completedGenes = []
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
				new_codons.append(newCodon)
				results.write(newCodon.toString("\t") + "\n")
				nextended += 1
			ntries += 1
			if ntries % triesPerMessage == 0:
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(ntries) + " attempts, " + str(nextended) + " genes extended, " + str(ncompleted) + " genes completed.")
		if extended == 0:
			completedGenes.append(codon)
			ncompleted += 1
	results.close()
	next_codons = new_codons

# Group the results together to evaluate.
codons.extend(new_codons)
codons.extend(completedGenes)

# Open final evaluation file.
results = open(filename + "_evaluation.output", 'w', 1)
results.write("Length\tKey\tPosition\tPlaintext\tStatus\tFrequencies\tRanks\n")

# Final summary.
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Final output summary with rank and frequency evaluations.")
nresults = 0
for codon in codon:
	results.write(codon.toString("\t") + "\t" + str(round(evaluateFrequency(codon.expression, frequencies), 2)) + "\t" + str(round(evaluateRank(codon.expression, frequencies), 2)) + "\n")
	nresults += 1
	if nresults % resultsPerMessage == 0:
		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + codon.toString("\t") + "\t" + str(round(evaluateFrequency(codon.expression, frequencies), 2)) + "\t" + str(round(evaluateRank(codon.expression, frequencies), 2)))
results.close()
