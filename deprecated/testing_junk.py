#plaintext1 = "THEQUAGONEISAPERIODICCIPHERWITHAKEYEDPLAINALPHABETRUNAGAINSTASTRAIGHTCIPHERALPHABET"
#encryption1 = QuagmireI(alphabet, "SPRINGFEVER", "FLOWER", "A")
#print encryption1.encrypt(plaintext1)
#print encryption1.decrypt(encryption1.encrypt(plaintext1))

#plaintext2 = "INTHEQUAGTWOASTRAIGHTPLAINALPHABETISRUNAGAINSTAKEYEDCIPHERALPHABET"
#encryption2 = QuagmireII(alphabet, "SPRINGFEVER", "FLOWER", "A")
#print encryption2.encrypt(plaintext2)
#print encryption2.decrypt(encryption2.encrypt(plaintext2))

#plaintext3 = "THESAMEKEYEDALPHABETISUSEDFORPLAINANDCIPHERALPHABETS"
#encryption3 = QuagmireIII(alphabet, "AUTOMOBILE", "HIGHWAY", "A")
#print encryption3.encrypt(plaintext3)
#print encryption3.decrypt(encryption3.encrypt(plaintext3))

#plaintext4 = "THISONEEMPLOYSTHREEKEYWORDS"
#encryption4 = QuagmireIV(alphabet, "SENSORY", "PERCEPTION", "EXTRA", "S")
#print encryption4.encrypt(plaintext4)
#print encryption4.decrypt(encryption4.encrypt(plaintext4))

#import re
#from statistics import *

#ciphertext = open("ciphertexts/kryptos4.txt", 'r')
#string = ciphertext.read()
#string = re.sub('[^A-Z]', '', string)
#alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#referenceDistribution = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

#print distributionDeviation(string, alphabet, referenceDistribution)

#from hill import *

#modulus = 25

#mapping = loadMappingZeroIndexed("mappings/mapping1.txt") #26
#mapping = loadMappingZeroIndexed("mapping2.txt") #26
#mapping = loadMappingZeroIndexed("mapping3.txt") #25
#mapping = loadMappingZeroIndexed("mapping4.txt") #25
#mapping = loadMappingZeroIndexed("mappings/mapping5.txt") #26
#mapping = loadMappingZeroIndexed("mappings/mapping6.txt") #25

#key = recoverKey("NYPV", "BERL", mapping, modulus)
#key = recoverKey("YPVT", "ERLI", mapping, modulus)

#key = recoverKey("TMZF", "NCLO", mapping, modulus)

#key = recoverKey("NYPVTTMZF", "BERLINCLO", mapping, modulus)
#key = recoverKey("YPVTTMZFP", "ERLINCLOC", mapping, modulus)
#key = recoverKey("PVTTMZFPK", "RLINCLOCK", mapping, modulus)

#key = recoverKey("FQVDALQLA", "BERLINCLO", mapping, modulus)
#key = recoverKey("QVDALQLAV", "ERLINCLOC", mapping, modulus)
#key = recoverKey("VDALQLAVH", "RLINCLOCK", mapping, modulus)

#print key
#print decode(key.flatten(), mapping)
#otherKey = modularIntegerInversion(key, modulus)
#print otherKey
#print decode(otherKey.flatten(), mapping)

#testString = "NYP"
#print decode(applyKey(testString, "CIAKGBNSA", mapping, modulus), mapping)
#print decode(applyKey(testString, "CIANSAKGB", mapping, modulus), mapping)
#print decode(applyKey(testString, "KGBCIANSA", mapping, modulus), mapping)
#print decode(applyKey(testString, "KGBNSACIA", mapping, modulus), mapping)
#print decode(applyKey(testString, "NSACIAKGB", mapping, modulus), mapping)
#print decode(applyKey(testString, "NSAKGBCIA", mapping, modulus), mapping)
