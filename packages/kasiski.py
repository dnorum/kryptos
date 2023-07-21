def possibleStrings( characters, length ):
	strings = set(character for character in characters)
	if length == 1:
		return strings
	currLength = 1
	while currLength < length:
		newStrings = set()
		for string in strings:
			newStrings = newStrings.union(set(string + character for character in characters))
		strings = newStrings
		currLength += 1
	return sorted(strings)

def indices( string, substring ):
	indices = []
	start = 0
	while True:
		nextIndex = string.find(substring, start)
		if nextIndex == -1:
			return indices
		indices.append(nextIndex)
		#start = nextIndex + len(substring)
		start = nextIndex + 1

def kasiski( text, maxLength ):
	characters = sorted(set(character for character in text))
	repetitions = []
	for length in range(2, maxLength+1):
		substrings = possibleStrings(characters, length)
		for string in substrings:
			occurrences = indices(text, string)
			if len(occurrences) > 1:
				repetitions.append([string, occurrences])
	return repetitions
