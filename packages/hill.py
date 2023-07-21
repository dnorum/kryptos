import numpy

class Error(Exception):
	# Base class for exceptions in this module.
	pass

class LengthMismatchError(Error):
	# Error resulting from mismatched lengths.
	# Attributes:
	#	length1 -- The first length
	#	length2 -- The second length
	def __init__(self, length1, length2):
		self.length1 = length1
		self.length2 = length2

def recoverKey(cipher, plain, modulus):
	# Ensure texts have the same length and modulus
	if not len(cipher) == len(plain):
		raise LengthMismatchError(len(cipher), len(plain))
	cipher = [ element % modulus for element in cipher ]
	plain = [ element % modulus for element in plain ]
	# Turn into square matrices
	cipher = numpy.transpose(fillSquareMatrix(cipher))
	plain = numpy.transpose(fillSquareMatrix(plain))
	#Use identity:
	#KEY dot PLAIN = CIPHER mod MODULUS
	#KEY = CIPHER dot PLAIN^-1 mod MODULUS
	return numpy.dot(cipher, modularIntegerInversion(plain, modulus)) % modulus

def hillKernel(inputString, key, modulus):
	inputString = numpy.transpose(inputString)
	output = numpy.dot(key, inputString) % modulus
	return numpy.transpose(output).astype(int)

def hillKernelRepeat(inputString, key, modulus):
	length = len(key)
	output = []
	i = 0
	while i < len(inputString):
		output.extend(hillKernel(inputString[i:i+length], key, modulus))
		i += length
	return numpy.asarray(output)

def partialMatch(inputString, key, modulus, outputString, wildcard):
	if not len(inputString) == len(outputString):
		raise LengthMismatchError(len(inputString), len(outputString))
	output = hillKernel(inputString, key, modulus)
	for i in range(0, len(output)):
		if (not output[i] == outputString[i]) and not outputString[i] == wildcard:
			return False
	return True

def keyToString(key):
	string = "["
	for row in key:
		for element in row:
			string += str(int(element)) + ","
		string = string[:-1] + " / "
	string = string[:-3] + "]"
	return string
