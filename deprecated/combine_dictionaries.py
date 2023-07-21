with open("zaliznjak_forms_transliterated.txt", 'r') as russianDictionary:
	russianWords = set(word.rstrip() for word in russianDictionary)

with open("words_alpha.txt", 'r') as englishDictionary:
	englishWords = set(word.rstrip() for word in englishDictionary)

combinedDictionary = open("dictionary_english_russian.txt", 'w')

combinedWords = englishWords.union(russianWords)
for word in sorted(combinedWords):
	combinedDictionary.write(word + "\n")

combinedDictionary.close()
