# Open the raw log file.
hitFile = open("hill3_cribbed_no_j.hits", 'r')

# Open the output file.
outputFile = open("hill3_cribbed_no_j_scrubbed.output", 'w', 1)

hits = []
for line in hitFile:

	line = line.rstrip()
	if line[0] == ">":
		if not line[1:] in hits:
			hits.append(line[1:])

hits = sorted(hits)

for hit in hits:
	outputFile.write(hit + "\n")

hitFile.close()
outputFile.close()
