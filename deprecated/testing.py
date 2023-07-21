import numpy

# Load all necessary packages.
execfile("packages/alphabet.py")
execfile("packages/formatting.py")
execfile("packages/hill.py")
execfile("packages/statistics.py")
execfile("packages/vigenere.py")
execfile("packages/modular.py")
execfile("packages/quagmire.py")

# Define the alphabets.
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
modAlphabet = alphabet.modulus()
cipherAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
cipherAlphabet.key("KRYPTOS")
plainAlphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plainAlphabet.key("KRYPTOS")

ciphertext = "FLRVQQPRNGKSS"
key = "RDUMRIYWOYNKY"

print QuagmireIII(alphabet, "KRYPTOS", key, "K").decrypt(ciphertext) #Checks.
