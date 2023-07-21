import csv
import datetime

beginningFileName = "key_autokey_beginnings_10kwords.output"
middleFileName = "key_autokey_patchwork_10kwords.output3"
endFileName = "key_autokey_ends_10kwords.output"
outputFileName = "key_autokey_add_beginnings_ends_10kwords.output"

attemptsPerMessage = 10000

# Define class to make things easier.
class fragment:
	def __init__(self, length, keyword, key, word, keystream):
		self.length = length
		self.keyword = keyword
		self.key = key
		self.word = word
		self.keystream = keystream

# Same for loading function and for keywords.
def loadFragments(fileName):
	fragments = set()
	with open(fileName) as source:
		reader = csv.reader(source, delimiter="\t")
		# Clear header.
		next(reader)
		for line in reader:
			fragments.add(fragment(line[0], line[1], line[2], line[3], line[4]))
	return fragments

def byKeyword(fragments, keyword):
	result = set()
	for fragment in fragments:
		if fragment.keyword == keyword:
			result.add(fragment)
	return result

# Define the two segments of keystream.
keystream1 = "RDUMRIYWOYNKY"
keystream2 = "ELYOIECBAQK"

# Initialize the output file.
outputFile = open(outputFileName, "w")
outputFile.write("Length\tKey\tKey Segment\tWord\tKeystream\n")

# Load the fragments.
beginnings = loadFragments(beginningFileName)
middles = loadFragments(middleFileName)
ends = loadFragments(endFileName)

# Process based on keyword. (Using all just in case we run into beginning + end.)
keywordSet = set()
for beginning in beginnings:
	keywordSet.add(beginning.keyword)
for middle in middles:
	keywordSet.add(middle.keyword)
for end in ends:
	keywordSet.add(end.keyword)
keywords = sorted(keywordSet)

# Test each keyword.
attempts = 0
for keyword in keywords:
	beginningFragments = byKeyword(beginnings, keyword)
	middleFragments = byKeyword(middles, keyword)
	endFragments = byKeyword(ends, keyword)
	# Add "blank" to make looping easier.
	blankFragment = fragment(0, keyword, "", "", "")
	beginningFragments.add(blankFragment)
	middleFragments.add(blankFragment)
	endFragments.add(blankFragment)
	# Create repeated key for checking.
	repeatedKeyword = keyword
	while len(repeatedKeyword) < max(len(keystream1), len(keystream2)):
		repeatedKeyword += keyword
	repeatedKeyword *= 2
	# Loop over combinations.
	for beginningFragment in beginningFragments:
		for middleFragment in middleFragments:
			for endFragment in endFragments:
				combinedKey = beginningFragment.key + middleFragment.key + endFragment.key
				combinedWord = beginningFragment.word + middleFragment.word + endFragment.word
				combinedKeystream = beginningFragment.keystream + middleFragment.keystream + endFragment.keystream
				if (combinedKey in repeatedKeyword) and (combinedKeystream == keystream1 or combinedKeystream == keystream2):
					outputFile.write(str(len(combinedWord)) + "\t" + keyword + "\t" + combinedKey + "\t" + combinedWord + "\t" + combinedKeystream + "\n")
				attempts += 1
				if attempts % attemptsPerMessage == 0:
					print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + keyword)
outputFile.close()
