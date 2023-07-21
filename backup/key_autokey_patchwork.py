import csv

fileName = "key_autokey_patchwork_10kwords.output2"
outputFileName = "key_autokey_patchwork_10kwords.output"

# Define class to make things easier.
class hit:
	def __init__(self, length, key, keySegment, word, keystream):
		self.length = length
		self.key = key
		self.keySegment = keySegment
		self.word = word
		self.keystream = keystream

# Define the two segments of keystream.
segment1 = "RDUMRIYWOYNKY"
segment2 = "ELYOIECBAQK"

# Load the data for processing and initialize the output file.
outputFile = open(outputFileName, "w")
outputFile.write("Length\tKey\tKey Segment\tWord\tKeystream\n")
hits = set()
with open(fileName) as source:
	reader = csv.reader(source, delimiter="\t")
	# Clear header.
	next(reader)
	for line in reader:
		hits.add(hit(line[0], line[1], line[2], line[3], line[4]))
		outputFile.write(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\n")

# Process based on keyword.
keywords = set()
for hit in hits:
	keywords.add(hit.key)
for keyword in keywords:
	keywordHits = set()
	for hit in hits:
		if hit.key == keyword:
			keywordHits.add(hit)
	keywordHits1 = keywordHits
	keywordHits2 = keywordHits
	for keyword1 in keywordHits1:
		for keyword2 in keywordHits2:
			combinedKeySegment = keyword1.keySegment + keyword2.keySegment
			combinedKeystream = keyword1.keystream + keyword2.keystream
			combinedWords = keyword1.word + keyword2.word
			if (combinedKeySegment in (keyword * 2)) and (combinedKeystream in segment1 or combinedKeystream in segment2):
				outputFile.write(str(len(combinedWords)) + "\t" + keyword + "\t" + combinedKeySegment + "\t" + combinedWords + "\t" + combinedKeystream + "\n")
outputFile.close()
