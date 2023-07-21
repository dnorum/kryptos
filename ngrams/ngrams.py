import datetime

# Load all necessary packages.
exec(open("../packages/alphabet.py").read())
exec(open("../packages/quagmire.py").read())

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Construct lookup for letters.
lookup = dict()
for letter1 in alphabet.characters:
	for letter2 in alphabet.characters:
		pair = letter1 + letter2
		keystreamLetter = QuagmireIII(alphabet, "KRYPTOS", letter1, "K").decrypt(letter2)
		lookup[pair] = keystreamLetter

def decrypt(lookup, string1, string2):
	if len(string1) != len(string2):
		raise Error
	result = ""
	for i in range(0, len(string1)):
		result += lookup[string1[i] + string2[i]]
	return result

# Define dictionary function.
def loadDictionaryFile(dictionaryFilename):
	dictionary = set()
	with open(dictionaryFilename) as source:
		for line in source:
			dictionary.add(line.strip().upper())
	return sorted(dictionary)

# Define ngram function.
def loadNgramFile(ngramFilename):
	ngrams = dict()
	with open(ngramFilename) as source:
		rank = 1
		for line in source:
			ngrams[line.strip().upper()] = rank
			rank += 1
	return ngrams

# Define the two segments of keystream.
keystreamSegments = ["RDUMRIYWOYNKY", "ELYOIECBAQK"]

# Set logging rate.
attemptsPerMessage = 10000
attempts = 0

for n in range(1, 8):
	# Load ngrams.
	ngramFilename = "../resources/ngrams/" + str(n) + "grams.txt"
	ngrams = loadNgramFile(ngramFilename)
	# Open output file.
	filename = str(n) + "grams.output"
	results = open(filename, 'w', 1)
	results.write("Ngram1\tNgram2\tStream\tRank\n")
	for segment in keystreamSegments:
		segmentLength = len(segment)
		for i in range(0, segmentLength - n + 1):
			snippet = segment[i:i+n]
			for ngram in ngrams:
				ngram2 = decrypt(lookup, ngram, snippet)
				if ngram2 in ngrams:
					results.write(ngram + "\t" + ngram2 + "\t" + snippet + "\t" + str(ngrams[ngram]*ngrams[ngram2]) + "\n")
				attempts += 1
				print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + ngram + ", " + ngram2)
	# Close output file.
	results.close()
