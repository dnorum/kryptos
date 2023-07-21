import numpy

class Error(Exception):
	# Base class for exceptions in this module.
	pass

class IntegerError(Error):
	# Error resulting from a non-integer number.
	# Attributes:
	#	value -- The non-integer value
	def __init__(self, value):
		self.value = value

class ModularInvertibilityError(Error):
	# Error resulting from a non-modularly-invertible value.
	# Attributes:
	#	value -- The non-invertible value
	#	modulus -- The modular base
	def __init__(self, value, modulus):
		self.value = value
		self.modulus = modulus

def modularInverse( number, modulus ):
	# Make sure that the number is an integer
	if not int(number) == number:
		raise IntegerError(number)
	# Same for the modulus
	if not int(modulus) == modulus:
		raise IntegerError(modulus)
	# Make sure that we start between 0 and [modulus]
	start = number % modulus
	# If the number is its own modular inverse, we're done
	if start == 1:
		return 1
	# Keep running tally of [multiple = number * inverse (mod modulus)]
	inverse = 1
	multiple = start
	# Add the number to itself until [multiple = number * inverse = 1 (mod modulus)]
	while (multiple != 1):
		inverse += 1
		multiple += number
		multiple %= modulus
		# If it begins to cycle, then GCD(number, modulus) != 1
		if multiple == start:
			raise ModularInvertibilityError(number, modulus)
	return int(inverse)

def modularIntegerInversion( matrix, modulus ):
	# Make sure that matrix is in fact integer-valued
	# (Matrix CAN have values outside of [0, modulus-1], but really SHOULDN'T)
	for element in numpy.nditer(matrix):
		if not int(element) == element:
			raise IntegerError(element)
	# Same for the modulus
	if not int(modulus) == modulus:
		raise IntegerError(modulus)
	det = round(numpy.linalg.det(matrix))
	detInverse = modularInverse(det, modulus)
	# Calculate the modular integer version of the inverse matrix
	inverse = numpy.linalg.inv(matrix)
	inverse = inverse * detInverse * det
	# Take care of any .000000000001 floating point nonsense	
	inverse = numpy.matrix.round(inverse)
	return numpy.asarray(inverse).astype(int) % modulus
