class QuagmireI:

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
QUAGMIRE I (period times 15-18 lines deep)
The Quagmires are numbered in the same way as keywords (See Chapter 8). Thus, a
Quagmire 1 uses a K1 keyword plan. An indicator keyword is also used to
determine the period and the ciphertext alphabet settings. It may appear
vertically under any letter of the plaintext alphabet. The encipherments follow
each letter of the indicator key in turn.

pt:	The Quag One is a periodic cipher with a keyed plain alphabet run
	against a straight cipher alphabet.

Key: SPRINGFEV(ER)

Indicator key under A is FLOWER (period 6).

Keyed pt S P R I N G F E V A B C D H J K L M O Q T U W X Y Z
     C 1 W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
     I 2 C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
     P 3 F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
     H 4 N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
     E 5 V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
     R 6 I J K L M N O P Q R S T U V W X Y Z A B C D E F G H

    1 2 3 4 5 6
pt: t h e q u a		CT: Q P M G Q R
    g o n e i s		    B U J U Y I
    a p e r i o		    F D M P Y A
    d i c c i p		    I F Q Y Y J
    h e r w i t		    J J H J Y C
    h a k e y e		    J L U U T P
    d p l a i n		    I D V W Y M
    a l p h a b		    F S G A E S
    e t r u n a		    D W H I Z R
    g a i n s t		    B L I R V C
    a s t r a i		    F C Z P E L
    g h t c i p		    B P Z Y Y J
    h e r a l p		    J J H W L J
    h a b e t		    J L P U P

CT:	QPMGQ RBUJU YIFDM PYAIF QYYJJ JHJYC JLUUT PIDVW YMFSG AESDW HIZRB
	LIRVC FCZPE LBPZY YJJJH WLJJL PUP.
"""
