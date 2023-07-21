class Crib:
	def __init__(self, ciphertext, plaintext):
		self.ciphertext = ciphertext
		self.plaintext = plaintext

def loadCrib(filename):
	cribFile = open(filename, 'r')
	ciphertext = cribFile.readline()
	plaintext = cribFile.readline()
	return Crib(ciphertext, plaintext)
