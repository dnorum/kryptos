import codecs
import io
import re
import string
from transliterate import get_translit_function

translit_ru = get_translit_function('ru')

russianFile = codecs.open("zaliznjak_forms.txt", encoding='utf-8')
englishFile = codecs.open("zaliznjak_forms_transliterated.txt", 'w')

for line in russianFile:
	english = translit_ru(line.rstrip(), reversed=True).upper()
	words = english.split(',')
	for word in words:
		englishFile.write(re.sub('[^A-Z]', '', word) + "\n")

russianFile.close()
englishFile.close()
