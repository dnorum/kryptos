execfile("packages/alphabet.py")
execfile("packages/quagmire.py")

words = dict()
beginnings = dict()
endings = dict()
middles = dict()
dictionaryFile = open("resources/dictionaries/3esl.txt", 'r')
for word in dictionaryFile:
	word = word.rstrip().upper()
	length = len(word)
	words[word] = length
	for n in range(length-1):
		beginnings[word[:n+1]] = n+1
		endings[word[length-n-1:]] = n+1
		for k in range(1,n+1):
			middles[word[k:n+1]] = n+1-k
dictionaryFile.close()

alphabet = loadDistribution("resources/reference_distribution.txt").alphabet
frequencyFile = open("resources/frequency_lists/written.num", 'r')
frequencyBaseline = 89740556.0
frequencies = dict()
for line in frequencyFile:
	line_array = line.split(' ')
	frequencies[alphabet.scrub(line_array[1].upper())] = float(line_array[0])/frequencyBaseline
frequencyFile.close()

def evaluate(string, frequencies):
	frequencyTotal = 0
	frequencyHits = 0
	if string in frequencies:
		frequencyTotal += frequencies[string]
		frequencyHits += 1
	for n in range(len(string)-1):
		if string[:n+1] in frequencies:
			frequencyTotal += frequencies[string[:n+1]]
			frequencyHits += 1
		if string[len(string)-n-1:] in frequencies:
			frequencyTotal += frequencies[string[len(string)-n-1:]]
			frequencyHits += 1
		for k in range(1,n+1):
			if string[k:n+1] in frequencies:
				frequencyTotal += frequencies[string[k:n+1]]
				frequencyHits += 1
	if frequencyHits != 0:
		frequencyTotal = float(frequencyTotal) / float(frequencyHits)
	return frequencyTotal

def verify(string, words, beginnings, middles, endings):
	status = set()
	if string in words:
		status.add("words")
	if string in beginnings:
		status.add("beginning")
	if string in middles:
		status.add("middle")
	if string in endings:
		status.add("ending")
	for n in range(1, len(string)):
		result_begin = verify(string[:n], words, beginnings, middles, endings)
		result_end = verify(string[n:], words, beginnings, middles, endings)
		if result_begin.issuperset({"words"}):
			if result_end.issuperset({"words"}):
				status.add("words")
			if not result_end.isdisjoint({"beginning", "words_beginning"}):
				status.add("words_beginning")
		if result_begin.issuperset({"ending"}):
			if result_end.issuperset({"words"}):
				status.add("ending_words")
			if result_end.issuperset({"words_beginning"}):
				status.add("ending_words_beginning")
			if result_end.issuperset({"beginning"}):
				status.add("ending_beginning")
		if result_begin.issuperset({"ending_words"}):
			if result_end.issuperset({"words"}):
				status.add("ending_words")
			if not result_end.isdisjoint({"beginning", "words_beginning"}):
				status.add("ending_words_beginning")
	if status != set():
		return status
	return set("unverified")

class Codon:
	def __init__(self, start, word, expression, status):
		self.start = start
		self.word = word
		self.length = len(word)
		self.expression = expression
		self.status = status

ciphertext = "RDUMRIYWOYNKY"
results = open("no_kill_overkill_brute_force.output", 'w', 1)
results.write("Length\tKey\tPosition\tPlaintext\tStatus\tEvaluation\n")
dictionaryFile = open("resources/dictionaries/3esl.txt", 'r')
nwords = 0
codons = []
for word in dictionaryFile:
	word = word.rstrip().upper()
	n = len(word)
	for x in range(len(ciphertext)-n+1):
		plain = QuagmireIII(alphabet, "KRYPTOS", word, "K").decrypt(ciphertext[x:x+n])
		status = verify(plain, words, beginnings, middles, endings)
		if status != set("unverified"):
			results.write(str(len(word)) + "\t" + word + "\t" + str(x) + "\t" + plain + "\t" + str(status) + "\t" + str(evaluate(plain, frequencies)) + "\n")
			codons.append(Codon(x, word, plain, status))
	nwords += 1
	if nwords % 1000 == 0:
		print(str(nwords) + ": " + word)
dictionaryFile.close()
results.close()

results = open("no_kill_overkill_brute_force_round2.output", 'w', 1)
results.write("Length\tKey\tPosition\tPlaintext\tStatus\n")
outgoing = {"beginning", "ending_beginning", "ending_words_beginning", "words_beginning", "middle"}
incoming = {"ending", "ending_beginning", "ending_words_beginning", "ending_words", "middle"}
blunt_out = {"words", "ending_words"}
blunt_in = {"words", "words_beginning"}
new_codons = []
for codon in codons:
	for following_codon in codons:
		if following_codon.start == codon.start + codon.length:
			if ((not codon.status.isdisjoint(outgoing)) and (not following_codon.status.isdisjoint(incoming))) or ((not codon.status.isdisjoint(blunt_out)) and (not following_codon.status.isdisjoint(blunt_in))):
				status = verify(codon.expression + following_codon.expression, words, middles, beginnings, endings)
				if status != set("unverified"):
					new_codons.append(Codon(codon.start, codon.word + following_codon.word, codon.expression + following_codon.expression, status))
					results.write(str(codon.length + following_codon.length) + "\t" + codon.word + following_codon.word + "\t" + str(codon.start) + "\t" + codon.expression + following_codon.expression + "\t" + str(status) + "\t" + str(evaluate(codon.expression + following_codon.expression, frequencies)) + "\n")
results.close()

results = open("no_kill_overkill_brute_force_round3.output", 'w', 1)
results.write("Length\tKey\tPosition\tPlaintext\tStatus\n")
new_new_codons = []
for codon in codons:
	for following_codon in new_codons:
		if following_codon.start == codon.start + codon.length:
			if ((not codon.status.isdisjoint(outgoing)) and (not following_codon.status.isdisjoint(incoming))) or ((not codon.status.isdisjoint(blunt_out)) and (not following_codon.status.isdisjoint(blunt_in))):
				status = verify(codon.expression + following_codon.expression, words, beginnings, middles, endings)
				if status != set("unverified"):
					new_new_codons.append(Codon(codon.start, codon.word + following_codon.word, codon.expression + following_codon.expression, status))
					results.write(str(codon.length + following_codon.length) + "\t" + codon.word + following_codon.word + "\t" + str(codon.start) + "\t" + codon.expression + following_codon.expression + "\t" + str(status) + "\t" + str(evaluate(codon.expression + following_codon.expression, frequencies)) + "\n")
results.close()
