# Open the processed log file.
scrubbedFile = open("hill3_cribbed_no_j_scrubbed.output", 'r')

# Open the output file.
outputFile = open("hill3_cribbed_no_j_scrubbed_dict.output", 'w', 1)

with open("resources/dictionaries/words_alpha.txt", 'r') as dictionary:
	words = set(word.rstrip() for word in dictionary)

def is_word(word):
	return word in words

crib = "BERLINCLOCK"

for line in scrubbedFile:
	line = line.rstrip()
	for i in range(0,len(crib)):
		if line.find(crib[i:]) == 0:
			remainder = line[len(crib)-i:]
	for i in range(0, len(remainder)):
		if is_word(remainder[0:-i]):
			remainder2 = remainder[-i+1:]
			for j in range(0, len(remainder2)):
				if is_word(remainder2[0:-j]):
					print line, remainder, str(len(remainder)-i + len(remainder2)-j), "\n"
					outputFile.write(line + ", " + remainder + "," + str(len(remainder)-i + len(remainder2)-j) + "\n")

scrubbedFile.close()
outputFile.close()
