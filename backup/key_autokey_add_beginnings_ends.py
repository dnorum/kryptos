import csv

fileName = "key_autokey_patchwork_10kwords.output3"
beginningFileName = "key_autokey_beginnings_10kwords.output"
endFileName = "key_autokey_ends_10kwords.output"
outputFileName = "key_autokey_add_beginnings_ends_10kwords.output"

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

beginnings = set()
with open(beginningFileName) as source:
	reader = csv.reader(source, delimiter="\t")
	# Clear header.
	next(reader)
	for line in reader:
		beginnings.add(hit(line[0], line[1], line[2], line[3], line[4]))

ends = set()
with open(endFileName) as source:
	reader = csv.reader(source, delimiter="\t")
	# Clear header.
	next(reader)
	for line in reader:
		ends.add(hit(line[0], line[1], line[2], line[3], line[4]))

# Process based on keyword.
keywords = set()
for hit in hits:
	keywords.add(hit.key)
for keyword in keywords:
	keywordHits = set()
	beginningHits = set()
	endHits = set()
	for hit in hits:
		if hit.key == keyword:
			keywordHits.add(hit)
	for end in ends:
		if end.key == keyword:
			endHits.add(hit)
	for beginning in beginnings:
		if beginning.key == keyword:
			beginningHits.add(hit)

	for keywordHit in keywordHits:
		for endHit in endHits:
			for beginningHit in beginningHits:
				combinedKeySegment = beginningHit.keySegment + keywordHit.keySegment + endHit.keySegment
				combinedKeystream = beginningHit.keystream + keywordHit.keystream + endHit.keystream
				combinedWords = beginningHit.word + keywordHit.word + endHit.word
				if (combinedKeySegment in (keyword * max(len(segment1), len(segment2)))) and (combinedKeystream == segment1 or combinedKeystream == segment2):
					outputFile.write(str(len(combinedWords)) + "\t" + keyword + "\t" + combinedKeySegment + "\t" + combinedWords + "\t" + combinedKeystream + "\n")
outputFile.close()
