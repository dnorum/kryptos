class QuagmireII:

	def __init__(self, alphabet, key, indicatorKey, indicatorKeyLetter):
		self.alphabet = alphabet
		self.alphabet.sort()
		self.key = key
		self.indicatorKey = indicatorKey
		self.indicatorKeyLetter = indicatorKeyLetter
		self.period = len(indicatorKey)

	def encrypt(self, plaintext):
		self.alphabet.check(plaintext)

		plaintextAlphabet = Alphabet(self.alphabet.characters)

		ciphertextAlphabet = Alphabet(self.alphabet.characters)
		ciphertextAlphabet.key(self.key)

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

		ciphertextAlphabet = Alphabet(self.alphabet.characters)
		ciphertextAlphabet.key(self.key)

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
QUAGMIRE II (period times 15-18 lines deep)
The Quagmires are numbered in the same way as keywords (See Chapter 8). Thus a
Quagmire 2 uses a K2 keyword plan. An indicator keyword is also used to
determine the period and the ciphertext alphabet settings. It may appear
vertically under any letter of the plaintext alphabet. The encipherments follow
each letter of the indicator key in turn.

pt: In the Quag Two a straight plain alphabet is run against a keyed cipher
alphabet.

Key: SPRINGFEV(ER)

Indicator key under plaintext alphabet A is FLOWER (period 6).

  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z	pt
1 F E V A B C D H J K L M O Q T U W X Y Z S P R I N G
2 L M O Q T U W X Y Z S P R I N G F E V A B C D H J K
3 O Q T U W X Y Z S P R I N G F E V A B C D H J K L M	CT
4 W X Y Z S P R I N G F E V A B C D H J K L M O Q T U
5 E V A B C D H J K L M O Q T U W X Y Z S P R I N G F
6 R I N G F E V A B C D H J K L M O Q T U W X Y Z S P

    1 2 3 4 5 6
pt: i n t h e q		CT: J I C I C O
    u a g t w o		    S L Y K I L
    a s t r a i		    F V C H E B
    g h t p l a		    D X C C O R
    i n a l p h		    J I O E W A
    a b e t i s		    F M W K K T
    r u n a g a		    X B G W H R
    i n s t a k		    J I B K E D
    e y e d c i		    B J W Z A B
    p h e r a l		    U X W H E H
    p h a b e t		    U X O X C U

CT:	JICIC OSLYK ILFVC HEBDX CCORJ IOEWA FMWKK TXBGW HRJIB KEDBJ WZABU XWHEH
	UXOXC U.
"""
