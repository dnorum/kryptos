# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/formatting.py")
execfile("packages/hill.py")
execfile("packages/modular.py")

# Define Hill(-3) specifics.
hillDimension = 3
wildcard = "*"
length = hillDimension**2

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIKLMNOPQRSTUVWXYZ")
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIKLMNOPQRSTUVWXYZ")
plainAlphabet = Alphabet("ABCDEFGHIKLMNOPQRSTUVWXYZ")

# Load and process the crib.
# Note that this assumes ^[wildcard]*[^wildcard]+[wildcard]*$
cribFile = open("resources/cribs/kryptos4_hill3.txt", 'r')
ciphertext = cribFile.readline().replace("J", "I")
plaintext = cribFile.readline()
cribFile.close()
assert len(ciphertext) == len(plaintext)
plainStart = 0
while plaintext[plainStart] == wildcard:
	plainStart += 1
plainEnd = plainStart
while not plaintext[plainEnd] == wildcard:
	plainEnd += 1
assert (plainEnd - plainStart + 1) >= length
plainPreChecks = []
cipherPreChecks = []
plainCribs = []
cipherCribs = []
plainPostChecks = []
cipherPostChecks = []
for offset in range(0, hillDimension):
	plainPreChecks.append(plaintext[plainStart-3+offset:plainStart+offset])
	cipherPreChecks.append(ciphertext[plainStart-3+offset:plainStart+offset])
	plainCribs.append(plaintext[plainStart+offset:plainStart+length+offset])
	cipherCribs.append(ciphertext[plainStart+offset:plainStart+length+offset])
	plainPostChecks.append(plaintext[plainStart+length+offset:plainStart+length+offset+3])
	cipherPostChecks.append(ciphertext[plainStart+length+offset:plainStart+length+offset+3])

# Set up the output file.
outputFile = open("hill3_cribbed_no_j.output", 'w', 1)

# Loop over the dictionary.
with open("resources/dictionaries/dictionary_english_russian.txt", 'r') as dictionary:
	words = set(word.rstrip().replace("J", "I") for word in dictionary)
words = sorted(words)

nWords = 1
for word in words:
	for offset in range(0, hillDimension):

		# Keyword I
		plainAlphabet.key(word)
		cipherAlphabet.sort()
		plain = plainAlphabet.encodeStringWildcard(plainCribs[offset], wildcard)
		plainPre = plainAlphabet.encodeStringWildcard(plainPreChecks[offset], wildcard)
		plainPost = plainAlphabet.encodeStringWildcard(plainPostChecks[offset], wildcard)
		cipher = cipherAlphabet.encodeStringWildcard(cipherCribs[offset], wildcard)
		cipherPre = cipherAlphabet.encodeStringWildcard(cipherPreChecks[offset], wildcard)
		cipherPost = cipherAlphabet.encodeStringWildcard(cipherPostChecks[offset], wildcard)
		try:
			key = recoverKey(cipher, plain, modAlphabet)
			inverseKey = modularIntegerInversion(key, modAlphabet)
			if (partialMatch(cipherPre, inverseKey, modAlphabet, plainPre, wildcard) and partialMatch(cipherPost, inverseKey, modAlphabet, plainPost, wildcard)):
				outputFile.write("K1\t" + "\t" + word + "\t" + keyToString(key) + "\t" + str(offset) + "\n")
				print("".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))))
				outputFile.write(">" + "".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))) + "\n")
		except (ModularInvertibilityError):
			pass

		# Keyword II
		plainAlphabet.sort()
		cipherAlphabet.key(word)
		plain = plainAlphabet.encodeStringWildcard(plainCribs[offset], wildcard)
		plainPre = plainAlphabet.encodeStringWildcard(plainPreChecks[offset], wildcard)
		plainPost = plainAlphabet.encodeStringWildcard(plainPostChecks[offset], wildcard)
		cipher = cipherAlphabet.encodeStringWildcard(cipherCribs[offset], wildcard)
		cipherPre = cipherAlphabet.encodeStringWildcard(cipherPreChecks[offset], wildcard)
		cipherPost = cipherAlphabet.encodeStringWildcard(cipherPostChecks[offset], wildcard)
		try:
			key = recoverKey(cipher, plain, modAlphabet)
			inverseKey = modularIntegerInversion(key, modAlphabet)
			if (partialMatch(cipherPre, inverseKey, modAlphabet, plainPre, wildcard) and partialMatch(cipherPost, inverseKey, modAlphabet, plainPost, wildcard)):
				outputFile.write("K2\t" + "\t" + word + "\t" + keyToString(key) + "\t" + str(offset) + "\n")
				print("".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))))
				outputFile.write(">" + "".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))) + "\n")
		except (ModularInvertibilityError):
			pass

		# Keyword III
		plainAlphabet.key(word)
		cipherAlphabet.key(word)
		plain = plainAlphabet.encodeStringWildcard(plainCribs[offset], wildcard)
		plainPre = plainAlphabet.encodeStringWildcard(plainPreChecks[offset], wildcard)
		plainPost = plainAlphabet.encodeStringWildcard(plainPostChecks[offset], wildcard)
		cipher = cipherAlphabet.encodeStringWildcard(cipherCribs[offset], wildcard)
		cipherPre = cipherAlphabet.encodeStringWildcard(cipherPreChecks[offset], wildcard)
		cipherPost = cipherAlphabet.encodeStringWildcard(cipherPostChecks[offset], wildcard)
		try:
			key = recoverKey(cipher, plain, modAlphabet)
			inverseKey = modularIntegerInversion(key, modAlphabet)
			if (partialMatch(cipherPre, inverseKey, modAlphabet, plainPre, wildcard) and partialMatch(cipherPost, inverseKey, modAlphabet, plainPost, wildcard)):
				outputFile.write("K3\t" + "\t" + word + "\t" + keyToString(key) + "\t" + str(offset) + "\n")
				print("".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))))
				outputFile.write(">" + "".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))) + "\n")
		except (ModularInvertibilityError):
			pass

		# Keyword IV
		for keyword in ["KRYPTOS", "KOMITET"]:
			plainAlphabet.key(word)
			cipherAlphabet.key(keyword)
			plain = plainAlphabet.encodeStringWildcard(plainCribs[offset], wildcard)
			plainPre = plainAlphabet.encodeStringWildcard(plainPreChecks[offset], wildcard)
			plainPost = plainAlphabet.encodeStringWildcard(plainPostChecks[offset], wildcard)
			cipher = cipherAlphabet.encodeStringWildcard(cipherCribs[offset], wildcard)
			cipherPre = cipherAlphabet.encodeStringWildcard(cipherPreChecks[offset], wildcard)
			cipherPost = cipherAlphabet.encodeStringWildcard(cipherPostChecks[offset], wildcard)
			try:
				key = recoverKey(cipher, plain, modAlphabet)
				inverseKey = modularIntegerInversion(key, modAlphabet)
				if (partialMatch(cipherPre, inverseKey, modAlphabet, plainPre, wildcard) and partialMatch(cipherPost, inverseKey, modAlphabet, plainPost, wildcard)):
					outputFile.write("K4\t" + "\t" + word + "\t" + keyword + "\t" + keyToString(key) + "\t" + str(offset) + "\n")
					print("".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))))
					outputFile.write(">" + "".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))) + "\n")
			except (ModularInvertibilityError):
				pass
			plainAlphabet.key(keyword)
			cipherAlphabet.key(word)
			plain = plainAlphabet.encodeStringWildcard(plainCribs[offset], wildcard)
			plainPre = plainAlphabet.encodeStringWildcard(plainPreChecks[offset], wildcard)
			plainPost = plainAlphabet.encodeStringWildcard(plainPostChecks[offset], wildcard)
			cipher = cipherAlphabet.encodeStringWildcard(cipherCribs[offset], wildcard)
			cipherPre = cipherAlphabet.encodeStringWildcard(cipherPreChecks[offset], wildcard)
			cipherPost = cipherAlphabet.encodeStringWildcard(cipherPostChecks[offset], wildcard)
			try:
				key = recoverKey(cipher, plain, modAlphabet)
				inverseKey = modularIntegerInversion(key, modAlphabet)
				if (partialMatch(cipherPre, inverseKey, modAlphabet, plainPre, wildcard) and partialMatch(cipherPost, inverseKey, modAlphabet, plainPost, wildcard)):
					outputFile.write("K4\t" + "\t" + keyword + "\t" + word + "\t" + keyToString(key) + "\t" + str(offset) + "\n")
					print("".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))))
					outputFile.write(">" + "".join(plainAlphabet.decodeString(hillKernelRepeat(cipherAlphabet.encodeString(ciphertext[plainStart+offset:plainStart+offset+hillDimension**3]), inverseKey, modAlphabet))) + "\n")
			except (ModularInvertibilityError):
				pass

	if nWords % 10000 == 0:
		print str(nWords) + ", " + word
	nWords += 1

# Close the file.
outputFile.close()
