# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 10:39:38 2019

@author: Omar
"""

try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Japanese NLP")
except:
    pass

from sudachipy import tokenizer
from sudachipy import dictionary

from my_functions import histogramizeKanji, histogramizeWords, dataframizeKanji, dataframizeWords, zipf_plot, sortList, printToFile, sumTotalWords
from text import filtered, kids, filtered_old

gendai_kanji = histogramizeKanji(filtered, line_occurrence = 'multiple')
old_kanji = histogramizeKanji(filtered_old, line_occurrence = 'multiple')
kids_kanji = histogramizeKanji(kids, line_occurrence = 'multiple')

gendai_kanji.to_csv(r'gendai_kanji.txt', header=None, index=None, sep='\t', mode='a')
old_kanji.to_csv(r'old_kanji.txt', header=None, index=None, sep='\t', mode='a')
kids_kanji.to_csv(r'kids_kanji.txt', header=None, index=None, sep='\t', mode='a')

print(gendai_kanji.sum(axis=0, skipna = True))
print(old_kanji.sum(axis=0, skipna = True))
print(kids_kanji.sum(axis=0, skipna = True))


full_word_list = histogramizeWords(filtered)
kids_word_list = histogramizeWords(kids)
old_word_list = histogramizeWords(filtered_old)

words_gendai = sortList(full_word_list[0])
stems_gendai = sortList(full_word_list[1])



words_kids = sortList(kids_word_list[0])
stems_kids = sortList(kids_word_list[1])

words_showa = sortList(old_word_list[0])
stems_showa = sortList(old_word_list[1])


printToFile(words_gendai, "words_gendai.txt")
printToFile(stems_gendai, "stems_gendai.txt")
printToFile(words_kids, "words_kids.txt")
printToFile(stems_kids, "stems_kids.txt")
printToFile(words_showa, "words_showa.txt")
printToFile(stems_showa, "stems_showa.txt")

printToFile(full_word_list, "gendai_parts.txt", mode ="parts")
printToFile(old_word_list, "showa_parts.txt", mode ="parts")
printToFile(kids_word_list, "kids_parts.txt", mode ="parts")


print(len(full_word_list[2][0]))
print(len(full_word_list[3][0]))

print(sumTotalWords(full_word_list))
print(sumTotalWords(old_word_list))
print(sumTotalWords(kids_word_list))

print(words_gendai)

print(len(old_word_list[2]))
for i in range(0, len(old_word_list[2][0])):
    print(old_word_list[2][0][i])
    print(old_word_list[3][0][i])
    print("*")
    print(old_word_list[2][1][i])
    print(old_word_list[3][1][i])
    print("********")




word_dataframe = dataframizeWords(full_word_list[1])
type_dataframe = dataframizeKanji(full_word_list[2])

kids_kanji_dataframe = dataframizeKanji(kids_kanji_list)


kids_word_dataframe = dataframizeWords(kids_word_list[1])


kids_type_dataframe = dataframizeKanji(kids_word_list[2])




print(full_kanji_dataframe)
print(full_kanji_dataframe2)

print("食" in full_kanji_dataframe["Kanji"].values)
    
print(word_dataframe)
print(type_dataframe)

print(kids_kanji_dataframe)
print(kids_word_dataframe)
print(kids_type_dataframe)



zipf_plot(kanji_dataframe)

zipf_plot(word_dataframe)

zipf_plot(type_dataframe)

zipf_plot(kids_kanji_dataframe)

zipf_plot(kids_word_dataframe)

zipf_plot(kids_type_dataframe)



tokenizer_obj = dictionary.Dictionary().create()

txt = "うん。そうだよ。"


mode = tokenizer.Tokenizer.SplitMode.A

for m in tokenizer_obj.tokenize(txt, mode):
    print(m)
    print("{0}\t{1}".format(m.surface(), m.part_of_speech()[0]))
    
print("**************")

for m in tokenizer_obj.tokenize(txt, mode):
    print("{0}\t{1}".format(m.dictionary_form(), m.part_of_speech()[0]))

