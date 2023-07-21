class Quagmire:

	def __init__(self, alphabet, plainKey, cipherKey, indicatorKey, indicatorKeyLetter):
		self.alphabet = alphabet
		self.plainKey = plainKey
		self.plaintextAlphabet = Alphabet(alphabet.characters)
		self.plaintextAlphabet.key(self.plainKey)
		self.cipherKey = cipherKey
		self.ciphertextAlphabet = Alphabet(alphabet.characters)
		self.ciphertextAlphabet.key(self.cipherKey)
		self.indicatorKeyLetter = indicatorKeyLetter
		self.indicatorKey = indicatorKey
		self.indicatorZero = self.plaintextAlphabet.encodeCharacter(indicatorKeyLetter)
		self.indicatorOffset = self.ciphertextAlphabet.encodeString(indicatorKey)
		self.period = len(indicatorKey)

	def encrypt(self, plaintext):
		self.alphabet.check(plaintext)
		ciphertext = ""
		for i in range(0,len(plaintext)):
			cipher = \
			self.plaintextAlphabet.encodeCharacter(plaintext[i]) \
			- self.indicatorZero + self.indicatorOffset[i % self.period]
			cipher %= self.alphabet.modulus()
			ciphertext += self.ciphertextAlphabet.decodeCharacter(cipher)
		return ciphertext

	def decrypt(self, ciphertext):
		self.alphabet.check(ciphertext)
		plaintext = ""
		for i in range(0,len(ciphertext)):
			plain = \
			self.ciphertextAlphabet.encodeCharacter(ciphertext[i]) \
			+ self.indicatorZero - self.indicatorOffset[i % self.period]
			plain %= self.alphabet.modulus()
			plaintext += self.plaintextAlphabet.decodeCharacter(plain)
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

class QuagmireI(Quagmire):

	def __init__(self, alphabet, key, indicatorKey, indicatorKeyLetter):
		Quagmire.__init__(self, alphabet, key, alphabet.characters, indicatorKey, indicatorKeyLetter)

	def string(self):
		return "QI," + self.plainKey + "," + self.indicatorKey + "," + self.indicatorKeyLetter

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

class QuagmireII(Quagmire):

	def __init__(self, alphabet, key, indicatorKey, indicatorKeyLetter):
		Quagmire.__init__(self, alphabet, alphabet.characters, key, indicatorKey, indicatorKeyLetter)

	def string(self):
		return "QII," + self.cipherKey + "," + self.indicatorKey + "," + self.indicatorKeyLetter

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

class QuagmireIII(Quagmire):

	def __init__(self, alphabet, key, indicatorKey, indicatorKeyLetter):
		Quagmire.__init__(self, alphabet, key, key, indicatorKey, indicatorKeyLetter)

	def string(self):
		return "QIII," + self.plainKey + "," + self.indicatorKey + "," + self.indicatorKeyLetter

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

class QuagmireIV(Quagmire):

	def __init__(self, alphabet, plainKey, cipherKey, indicatorKey, indicatorKeyLetter):
		Quagmire.__init__(self, alphabet, plainKey, cipherKey, indicatorKey, indicatorKeyLetter)

	def string(self):
		return "QIV," + self.plainKey + "," + self.cipherKey + "," + self.indicatorKey + "," + self.indicatorKeyLetter
