import csv

fileName = "key_autokey_patchwork_10kwords.output3"
outputFileName = "key_autokey_patchwork_summary_10kwords.output"

# Define class to make things easier.
class hit:
	def __init__(self, length, key, keySegment, word, keystream):
		self.length = length
		self.key = key
		self.keySegment = keySegment
		self.word = word
		self.keystream = keystream

class key:
	def __init__(self, key, maxLength1, maxLength2):
		self.key = key
		self.maxLength1 = maxLength1
		self.maxLength2 = maxLength2

# Define the two segments of keystream.
segment1 = "RDUMRIYWOYNKY"
segment2 = "ELYOIECBAQK"

# Load the data for processing and initialize the output file.
outputFile = open(outputFileName, "w")
outputFile.write("Total Length\tLength1\tLength2\tKey\n")
hits = set()
with open(fileName) as source:
	reader = csv.reader(source, delimiter="\t")
	# Clear header.
	next(reader)
	for line in reader:
		hits.add(hit(int(line[0]), line[1], line[2], line[3], line[4]))

# Process based on keyword.
keywords = set()
for hit in hits:
	keywords.add(hit.key)
summaries = {}
for keyword in keywords:
	summaries[keyword] = key(keyword, 0, 0)
	for hit in hits:
		if hit.key == keyword:
			if hit.keystream in segment1:
				summaries[keyword].maxLength1 = max(summaries[keyword].maxLength1, hit.length)
			if hit.keystream in segment2:
				summaries[keyword].maxLength2 = max(summaries[keyword].maxLength2, hit.length)

for summary in summaries:
	outputFile.write(str(summaries[summary].maxLength1 + summaries[summary].maxLength2) + "\t" + str(summaries[summary].maxLength1) + "\t" + str(summaries[summary].maxLength2) + "\t" + summaries[summary].key + "\n")

outputFile.close()
