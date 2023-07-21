# Open the raw log file.
indicatorFile = open("cribbed_quagmire1-4_indicators.output", 'r')

# Define the max period (length of crib).
maxPeriod = 11

# Open the breakout files.
breakoutFiles = []
for i in range(1, maxPeriod+1):
	fileName = "cribbed_quagmire1-4_indicators_period" + str(i) + ".output"
	breakoutFiles.append(open(fileName, 'w', -1))

# Divvy up the indicators.
for line in indicatorFile:
	period = int(line[line.rfind(",")+1:-1])
	breakoutFiles[period-1].write(line)

# Close the files.
indicatorFile.close()
for breakoutFile in breakoutFiles:
	breakoutFile.close()
