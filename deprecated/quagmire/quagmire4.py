class QuagmireIV:

	def __init__(self, alphabet, plainKey, cipherKey, indicatorKey, indicatorKeyLetter):
		self.alphabet = alphabet
		self.alphabet.sort()
		self.plainKey = plainKey
		self.cipherKey = cipherKey
		self.indicatorKey = indicatorKey
		self.indicatorKeyLetter = indicatorKeyLetter
		self.period = len(indicatorKey)

	def encrypt(self, plaintext):
		self.alphabet.check(plaintext)

		plaintextAlphabet = Alphabet(self.alphabet.characters)
		plaintextAlphabet.key(self.plainKey)

		ciphertextAlphabet = Alphabet(self.alphabet.characters)
		ciphertextAlphabet.key(self.cipherKey)

		indicatorZero = plaintextAlphabet.encodeCharacter(self.indicatorKeyLetter)
		indicatorOffset = ciphertextAlphabet.encodeString(self.indicatorKey)

		ciphertext = ""
		for i in range(0,len(plaintext)):
			cipher = \
			plaintextAlphabet.encodeCharacter(plaintext[i]) \
			- indicatorZero + indicatorOffset[i % self.period]
			cipher %= self.alphabet.modulus()
			ciphertext += ciphertextAlphabet.decodeCharacter(cipher)
		return ciphertext

	def decrypt(self, ciphertext):
		self.alphabet.check(ciphertext)

		plaintextAlphabet = Alphabet(self.alphabet.characters)
		plaintextAlphabet.key(self.plainKey)

		ciphertextAlphabet = Alphabet(self.alphabet.characters)
		ciphertextAlphabet.key(self.cipherKey)

		indicatorZero = plaintextAlphabet.encodeCharacter(self.indicatorKeyLetter)
		indicatorOffset = ciphertextAlphabet.encodeString(self.indicatorKey)

		plaintext = ""
		for i in range(0,len(ciphertext)):
			plain = \
			ciphertextAlphabet.encodeCharacter(ciphertext[i]) \
			+ indicatorZero - indicatorOffset[i % self.period]
			plain %= self.alphabet.modulus()
			plaintext += plaintextAlphabet.decodeCharacter(plain)
		return plaintext			

"""
QUAGMIRE IV (period times 25-30 lines deep)
The Quagmires are numbered in the same way as keywords (See Chapter 8). Thus a
Quagmire 4 uses a K4 keyword plan. An indicator keyword is also used to
determine the period and the ciphertext alphabet settings. It may appear
vertically under any letter of the plaintext alphabet. The encipherments follow
each letter of the indicator key in turn.

pt: This one employs three keywords

Key: (pt): SENSORY, (CT): PERC(EP)TION

Indicator shown here under plaintext S is EXTRA (period 5).

  S E N O R Y A B C D F G H I J K L M P Q T U V W X Z	pt
1 E R C T I O N A B D F G H J K L M Q S U V W X Y Z P
2 X Y Z P E R C T I O N A B D F G H J K L M Q S U V W
3 T I O N A B D F G H J K L M Q S U V W X Y Z P E R C	CT
4 R C T I O N A B D F G H J K L M Q S U V W X Y Z P E
5 A B D F G H J K L M Q S U V W X Y Z P E R C T I O N

    1 2 3 4 5
pt: t h i s o	CT: V B M R F
    n e e m p	    C Y I S P
    l o y s t	    M P B R R
    h r e e k	    H E I C X
    e y w o r	    R R E I G
    d s		    D X

CT:	VBMRF CYISP MPBRR HEICX RREIG DX.
"""
