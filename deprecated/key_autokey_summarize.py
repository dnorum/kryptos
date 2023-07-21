import csv

fileName = "key_autokey_10kwords_copy.output"
outputFileName = "key_autokey_summarize_10kwords_copy.output"

# Define class to make things easier.
class hit:
	def __init__(self, length, key, keySegment, word, keystream):
		self.length = length
		self.key = key
		self.keySegment = keySegment
		self.word = word
		self.keystream = keystream

class key:
	def __init__(self, key, maxLength, numWords):
		self.key = key
		self.maxLength = maxLength
		self.numWords = numWords
	def output(self):
		return self.key + "\t" + str(self.maxLength) + "\t" + str(self.numWords)

# Load the data for processing.
hits = set()
with open(fileName) as source:
	reader = csv.reader(source, delimiter="\t")
	# Clear headers.
	next(reader)
	for line in reader:
		hits.add(hit(line[0], line[1], line[2], line[3], line[4]))

# Process based on keyword.
summaries = {}
for hit in hits:
	if hit.key in summaries:
		summaries[hit.key] = key(hit.key, max(hit.length, summaries[hit.key].maxLength), summaries[hit.key].numWords + 1)
	else:
		summaries[hit.key] = key(hit.key, hit.length, 1)

# Output the results.
outputFile = open(outputFileName, "w")
outputFile.write("Key\tMaxLength\tNumWords\n")
for summary in summaries:
	outputFile.write(summaries[summary].output() + "\n")
outputFile.close()
