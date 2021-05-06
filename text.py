# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:25:57 2019

@author: Omar
"""

try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Japanese NLP")
except:
    pass


nodaku_hira = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
small_hira = "ぁぃぅぇぉゃゅょっ"
dakuon_hira = "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
hiragana = nodaku_hira + small_hira + dakuon_hira

nodaku_kata = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンー"
small_kata = "ァィゥェォャュョッ"
dakuon_kata = "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"
katakana = nodaku_kata + small_kata + dakuon_kata

half_nodaku = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｰ"
half_small = "ｧｨｩｪｫｬｭｮｯ"
half_daku = "ｶﾞｷﾞｸﾞｹﾞｺﾞｻﾞｼﾞｽﾞｾﾞｿﾞﾀﾞﾁﾞﾂﾞﾃﾞﾄﾞﾊﾞﾋﾞﾌﾞﾍﾞﾎﾞﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ"
half_katakana = half_nodaku + half_small + half_daku
all_katakana = half_katakana + katakana
kana = hiragana + all_katakana

full_symbols = "、 。 ・ 「 」！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～｟｠￠￡￢￣￤￥￦│←↑→↓■○　【】『』"
half_symbols = " !\"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~"

full_characters = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９"
half_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

all_full = full_symbols + full_characters + kana
all_half = half_symbols + half_characters


all_english = all_half + all_full
all_japanese = hiragana + all_katakana


try:
    from my_functions import cleanStringSet, independentize

except:
    pass


with open('text\de_50.txt', 'r', encoding="utf8") as file:
    de_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')
    
with open('text\ga_50.txt', 'r', encoding="utf8") as file:
    ga_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\ha_50.txt', 'r', encoding="utf8") as file:
    ha_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\he_50.txt', 'r', encoding="utf8") as file:
    he_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\kara_50.txt', 'r', encoding="utf8") as file:
    kara_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\made_50.txt', 'r', encoding="utf8") as file:
    made_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\mo_50.txt', 'r', encoding="utf8") as file:
    mo_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\\na_50.txt', 'r', encoding="utf8") as file:
    na_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\\ni_50.txt', 'r', encoding="utf8") as file:
    ni_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\\no_50.txt', 'r', encoding="utf8") as file:
    no_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\wo_50.txt', 'r', encoding="utf8") as file:
    wo_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')
    
with open('text\\no_50.txt', 'r', encoding="utf8") as file:
    yori_50 = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')
    
all_50 = de_50 + ga_50 + ha_50 + he_50 + kara_50 + made_50 + mo_50 + na_50 + ni_50 + no_50 + yori_50



with open('text\Showa\de_50_old.txt', 'r', encoding="utf8") as file:
    de_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')
    
with open('text\Showa\ga_50_old.txt', 'r', encoding="utf8") as file:
    ga_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\ha_50_old.txt', 'r', encoding="utf8") as file:
    ha_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\he_50_old.txt', 'r', encoding="utf8") as file:
    he_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\kara_50_old.txt', 'r', encoding="utf8") as file:
    kara_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\made_50_old.txt', 'r', encoding="utf8") as file:
    made_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\mo_50_old.txt', 'r', encoding="utf8") as file:
    mo_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\\na_50_old.txt', 'r', encoding="utf8") as file:
    na_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\\ni_50_old.txt', 'r', encoding="utf8") as file:
    ni_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\\no_50_old.txt', 'r', encoding="utf8") as file:
    no_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

with open('text\Showa\wo_50_old.txt', 'r', encoding="utf8") as file:
    wo_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')
    
with open('text\Showa\\no_50_old.txt', 'r', encoding="utf8") as file:
    yori_50_old = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

all_50_old = de_50_old + ga_50_old + ha_50_old + he_50_old + kara_50_old + made_50_old + mo_50_old + na_50_old + ni_50_old + no_50_old + yori_50_old



sum_gendai = 0
sum_showa = 0
for item in all_50:
    sum_gendai += len(item)
for item in all_50_old:
    sum_showa += len(item)

print("before")
print(sum_gendai)
print(sum_showa)

filtered = independentize(all_50)
filtered_old = independentize(all_50_old)

sum_gendai = 0
sum_showa = 0

for item in filtered:
    sum_gendai += len(item)
for item in filtered_old:
    sum_showa += len(item)

print("after") 
print(sum_gendai)
print(sum_showa)


Okayama = []
for i in range(1, 33):
    filename = "D:\(PC)\Desktop\Coding\Python\Japanese NLP\%shild\%skayama\%s (%d).cha"%('c','O','f',i)
    with open(filename, 'r', encoding="utf8") as file:
        Okayama.append(cleanStringSet(file.readlines(), garbage = '\n', target = '\t'))
        
Hamasaki = []
for i in range(1, 33):
    filename = "D:\(PC)\Desktop\Coding\Python\Japanese NLP\%shild\%samasaki\%s (%d).cha"%('c','H','a',i)
    with open(filename, 'r', encoding="utf8") as file:
        Hamasaki.append(cleanStringSet(file.readlines(), garbage = '\n', target = '\t'))

with open('kids.txt', 'r', encoding="utf8") as file:
    kids = cleanStringSet(file.readlines(), garbage = '\n', target = '\t')

#
#kids = []
#for block in Okayama:
#    kids += block
#
#
#test = []
#for i in range(0, len(kids)):
#    try:
#        if "MOT" in kids[i] or "JIR" in kids[i]:
#            while "CHI" not in kids[i]:
#                kids.pop(i)
#        
#        elif "act" in kids[i] or "CHI" in kids[i]:
#            kids.pop(i)
#
#        else:
#            pass
#            newline = ""
#            for character in kids[i]:
#                if character not in all_characters:
#                    newline += character
#            test.append(newline)
#    except:
#        pass
#print(test)
#
#
#
#
#
#
#print(save)
#
#f=open("kids.txt", "a+", encoding = "utf8")
#for line in filtered_kids:
#    f.write(line)
#    f.write('\n')
#f.close()


