class QuagmireIII:

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
		plaintextAlphabet.key(self.key)

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
		plaintextAlphabet.key(self.key)

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
QUAGMIRE III (period times 20-25 lines deep)
The Quagmires are numbered in the same way as keywords (See Chapter 8). Thus a
Quagmire 3 uses a K3 keyword plan. An indicator keyword is also used to
determine the period and the ciphertext alphabet settings. It may appear
vertically under any letter of the plaintext alphabet. The encipherments follow
each letter of the indicator key in turn.

pt: The same keyed alphabet is used for plain and cipher alphabets.

Key: AUTOMOBILE

Indicator key shown here under plaintext A is HIGHWAY (period 7).

  A U T O M B I L E C D F G H J K N P Q R S V W X Y Z	pt
1 H J K N P Q R S V W X Y Z A U T O M B I L E C D F G
2 I L E C D F G H J K N P Q R S V W X Y Z A U T O M B
3 G H J K N P Q R S V W X Y Z A U T O M B I L E C D F	CT
4 H J K N P Q R S V W X Y Z A U T O M B I L E C D F G
5 W X Y Z A U T O M B I L E C D F G H J K N P Q R S V
6 A U T O M B I L E C D F G H J K N P Q R S V W X Y Z
7 Y Z A U T O M B I L E C D F G H J K N P Q R S V W X

    1 2 3 4 5 6 7
pt: t h e s a m e	CT: K R S L W M I
    k e y e d a l	    T J D V I A B
    p h a b e t i	    M R G Q M T M
    s u s e d f o	    L L I V I F U
    r p l a i n a	    I X R H T N Y
    n d c i p h e	    O N V R H H I
    r a l p h a b	    I I R M C A O
    e t s		    V E I

CT:	KRSLW MITJD VIABM RGQMT MLLIV IFUIX RHTNY ONVRH HIIIR MCAOV EI.
"""
