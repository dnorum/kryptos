# Requires alphabet.

class Error(Exception):
	# Base class for exceptions in this module.
	pass

class Language:

	def __init__(self, words, beginnings, middles, endings):
		self.words = words
		self.beginnings = beginnings
		self.middles = middles
		self.endings = endings

	def verify(self, string):
		status = set()
		if string in self.words:
			status.add("words")
		if string in self.beginnings:
			status.add("beginning")
		if string in self.middles:
			status.add("middle")
		if string in self.endings:
			status.add("ending")
		for n in range(1, len(string)):
			result_begin = self.verify(string[:n])
			result_end = self.verify(string[n:])
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
	def __init__(self, start, sequence, expression, status):
		self.start = start
		self.sequence = sequence
		self.length = len(sequence)
		self.expression = expression
		self.status = status

	def toString(self, separator):
		return str(self.length) + separator + self.sequence + separator + str(self.start) + separator + self.expression + separator + str(self.status)

	def openTail(self):
		return not self.status.isdisjoint({"beginning", "ending_beginning", "ending_words_beginning", "words_beginning", "middle"})

	def openHead(self):
		return not self.status.isdisjoint({"ending", "ending_beginning", "ending_words_beginning", "ending_words", "middle"})

	def closedTail(self):
		return not self.status.isdisjoint({"words", "ending_words"})

	def closedHead(self):
		return not self.status.isdisjoint({"words", "words_beginning"})		

	def add(self, tail, language):
		if tail.start == (self.start + self.length):
			if (self.openTail() and tail.openHead()) or (self.closedTail() and tail.closedHead()):
				newExpression = self.expression + tail.expression
				status = language.verify(newExpression)
				if status != set("unverified"):
					return Codon(self.start, self.sequence + tail.sequence, newExpression, status)
		return self

def loadLanguage(fileName):
	dictionaryFile = open(fileName, 'r')
	words = dict()
	beginnings = dict()
	middles = dict()
	endings = dict()
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
	return Language(words, beginnings, middles, endings)

def loadFrequenciesFromCounts(filename, separator, alphabet, baseline):
	frequencyFile = open(filename, 'r')
	frequencies = dict()
	for line in frequencyFile:
		line_array = line.split(separator)
		frequencies[alphabet.scrub(line_array[1].upper())] = float(line_array[0])/float(baseline)
	frequencyFile.close()
	return frequencies

def loadRanksFromCounts(filename, separator, alphabet):
	rankFile = open(filename, 'r')
	ranks = dict()
	rank = 1
	for line in rankFile:
		line_array = line.split(separator)
		word = alphabet.scrub(line_array[1].upper())
		if word not in ranks:
			ranks[word] = rank
			rank += 1
	rankFile.close()
	return ranks

def evaluateFrequency(string, frequencies):
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

def evaluateRank(string, ranks):
	rankTotal = 0
	rankHits = 0
	if string in ranks:
		rankTotal += ranks[string]
		rankHits += 1
	for n in range(len(string)-1):
		if string[:n+1] in ranks:
			rankTotal += ranks[string[:n+1]]
			rankHits += 1
		if string[len(string)-n-1:] in ranks:
			rankTotal += ranks[string[len(string)-n-1:]]
			rankHits += 1
		for k in range(1,n+1):
			if string[k:n+1] in ranks:
				rankTotal += ranks[string[k:n+1]]
				rankHits += 1
	if rankHits != 0:
		rankTotal = float(rankTotal) / float(rankHits)
	return rankTotal
