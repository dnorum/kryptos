import numpy

def vignereIndexesOfCoincidence(string, period, alphabet):
	substringIndexes = []
	for i in range(0, period):
		substringIndexes.append(indexOfCoincidence(everyNth(string, i, period), alphabet))
	return substringIndexes

def vignereIndexOfCoincidence(substringIndexes):
	index = []
	index.append(sum(substringIndexes)/float(len(substringIndexes)))
	index.append(numpy.std(substringIndexes))
	return index
