import math

class Error(Exception):
	# Base class for exceptions in this module.
	pass

class PerfectSquareError(Error):
	# Error resulting from a number not being a perfect square.
	# Attributes:
	#	number -- The number that is not a perfect square
	def __init__(self, number):
		self.number = number

def fillSquareMatrix(array):
	if not math.sqrt(len(array)) == round(math.sqrt(len(array))):
		raise PerfectSquareError(len(array))
	n = int(math.sqrt(len(array)))
	matrix = []
	for i in range(0, n):
		row = []
		for j in range(0, n):
			row.append(array[j+i*n])
		matrix.append(row)
	return numpy.asarray(matrix)

def everyNth(string, start, length):
	substring = ''
	i = start
	while i < len(string):
		substring += string[i]
		i += length
	return substring

def beginsWith(string1, string2):
	if len(string2) > len(string1):
		return False
	for i in range(0,len(string2)):
		if not string1[i] == string2[i]:
			return False
	return True

def periodicities(string):
	periodicities = []
	maxLength = len(string)
	for i in range(1,maxLength+1):
		substring = string[0:i]
		repeatedSubstring = substring
		while len(repeatedSubstring) < maxLength:
			repeatedSubstring.extend(substring)
		if beginsWith(repeatedSubstring, string):
			periodicities.append(i)
	return periodicities
