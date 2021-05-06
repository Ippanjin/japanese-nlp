# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:12:24 2019

@author: Omar
"""

try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Japanese NLP")
except:
    pass

from operator import itemgetter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sudachipy import tokenizer
from sudachipy import dictionary
from text import all_full


class DataMismatchError(Exception):
    pass


"""
This function gets an array of text entries as input and removes all characters included in garbage from the text body.
Next the function replaces the characters in target with the text in marker.
"""
def cleanStringSet(stringSet, garbage = '\t\n', target = '', marker = '***'):
    #loop through text entries
    garbage_lines = []
    for j in range(len(stringSet)): 
        
        if stringSet[j][0] in ' 　ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\n':
            garbage_lines.append(j)
            continue
        
        adjustment = 0
        #loop through each character of the current text entry
        for i in range(len(stringSet[j])): 
            index = i + adjustment
            try:
                if stringSet[j][index] in garbage:  
                    """remove the garbage by creating a text entry that is the conjunction 
                    of all text before and after the garbage character"""
                    newline = stringSet[j][:index] + stringSet[j][index+1:]
                    stringSet[j] = newline
                

                elif stringSet[j][index] in target:
                    """replace marker with target by creating a newline with marker text sandwiched 
                    between text before and after the target character"""
                    newline = stringSet[j][:index] + marker + stringSet[j][index+1:]
                    stringSet[j] = newline
                    adjustment += len(marker)-1
                
              
                                
            except IndexError:
                pass
    
    for i in range(len(garbage_lines)):
        stringSet.pop(garbage_lines[i]-i)

    return stringSet


"""

This functions takes and array of text entries as input, loops thourgh each entry and counts all 
the chinese characters in all entries, and returns an array with the character and 
its number of appearences in the input text entries.

Line occurence: if set to 'multiple' chinese characters that appear more than one time in a sentence
will be all counted as they are. If set to 'single', then characters will be only counted once in a
given sentence.

multiple: これ…食‐食‐食べたくない！　⇒　['食', 3] 
single: これ…食‐食‐食べたくない！　⇒　['食', 1]

WARNING: DON'T USE SINGLE IF INPUT DATA IS A SINGLE HUGE BODY OF TEXT

Return type: if set to 'list', the frequency list would be returned a list variable. If set to
'dataframe', then it will be returned as Pandas dataframe
"""
def histogramizeKanji(set_of_lines, line_occurrence = 'multiple', descending = True, return_type = 'dataframe'):
    
    #create two arrays to store kanji and their respective frequency
    kanji_list = []
    frequency_list = []
    
    for line in set_of_lines:
        
        #temporay kanji list to count kanji one per text entry
        temp_kanji = []
        for character in line:
            
            #check if the character is a kanji or not
            if character not in all_full and character.isalnum():
    
                if character not in kanji_list:
                    #if the kanji is not in the list create a new entry with a frequency of 1, and add to temp list
                    kanji_list.append(character)
                    temp_kanji.append(character)
                    frequency_list.append(1)
                    
                elif character in kanji_list:
                    
                    if line_occurrence == 'multiple':
                        #if the kanji is in the list, then just increment the respective frequency by 1 (multiple mode)
                        frequency_list[kanji_list.index(character)] += 1
                        
                    elif line_occurrence == 'single':
                        if character not in temp_kanji:
                            #if the kanji is in the list, and only appeared once in the entry, increment frequency by one (single mode)
                            frequency_list[kanji_list.index(character)] += 1
                            temp_kanji.append(character)
    
    
    #if for some reason data mismatch occurs raise mismatch error
    if len(kanji_list) != len(frequency_list):
        raise DataMismatchError("Kanji frequencies are not equal to the number of characters")
        
    #combine kanji and frequencies list to make into one list
    histogram = []
    for i in range(0, len(kanji_list)):
        histogram.append([kanji_list[i], frequency_list[i]])
    
    #reorder the list to make a histogram
    histogram = sorted(histogram, key = itemgetter(1), reverse = descending)
            
    if return_type == 'list':
        return histogram
    
    elif return_type == 'dataframe':
        
        frequencies_sum = 0
        for element in histogram:
            frequencies_sum += element[1]
        
        dataframe = pd.DataFrame(histogram, columns = ['Kanji', 'Frequency'])
        dataframe['Rank'] = dataframe.index + 1
        dataframe = dataframe.reindex(columns = ['Kanji', 'Rank', 'Frequency'])
        dataframe['Expected'] = histogram[0][1]*(1/dataframe['Rank'])
        dataframe['Usage'] = 100*dataframe['Frequency']/frequencies_sum

        return dataframe



def histogramizeWords(set_of_lines, line_occurrence = 'multiple', descending = True, return_type = 'list'):
    
    words = [[],[]]
    stems = [[], []]
    parts_of_speech = [[],[]]
    parts_freq = [[],[]]

    length = len(set_of_lines)
    counter = 0
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.B
    
    for line in set_of_lines:
        counter += 1
        if counter % 20 == 0:
            print("(%d/%d)"%(counter, length))

        for m in tokenizer_obj.tokenize(line, mode):
            
            word, stem = m.surface(), m.dictionary_form()
            if stem in all_full:
                continue
            
            types = m.part_of_speech()
            
            if stem not in stems[0]:
                stems[0].append(stem)
                stems[1].append(1)
            else:
                stems[1][stems[0].index(stem)] += 1

            if word not in words[0]:
                words[0].append(word)
                words[1].append(1)
            else:
                words[1][words[0].index(word)] += 1
            
            if types[0] not in parts_of_speech[0]:
                parts_of_speech[0].append(types[0])
                parts_freq[0].append(0)
                parts_of_speech[1].append([[x] for x in types[1:]])
                parts_freq[1].append([[1],[1],[1],[1],[1]])
            
            else:
                index = parts_of_speech[0].index(types[0])
                parts_freq[0][index] += 1
                for j in range(0, 5):
                    if types[j+1] in parts_of_speech[1][index][j] and types[j+1] != '*':
                        parts_freq[1][index][j][parts_of_speech[1][index][j].index(types[j+1])] += 1
                    
                    if types[j+1] not in parts_of_speech[1][index][j] and types[j+1] != '*':
                        parts_of_speech[1][index][j].append(types[j+1])
                        parts_freq[1][index][j].append(1)
                

                
                
    return [words,stems,parts_of_speech,parts_freq]
    
    
def sortList(word_list):
    histogram = []
    for i in range(0, len(word_list[0])):
        histogram.append([word_list[0][i], word_list[1][i]])

    #reorder the list to make a histogram
    histogram = sorted(histogram, key = itemgetter(1), reverse = True)
    return histogram          


def printToFile(word_list, name, mode = "words"):
    
    f= open(name,"w+", encoding="utf8")
    if mode == "words":
        for i in word_list:
            f.write("%s\t%s\n" % (i[0], i[1]))
        
    elif mode == "parts":
        main_part_list = []
        for i in range(15):
            main_part_list.append([word_list[2][0][i], word_list[3][0][i], word_list[2][1][i], word_list[3][1][i]])
            main_part_list = sorted(main_part_list, key = itemgetter(1), reverse = True)
            
        for i in range(15):    
            f.write("\n##############################\n")
            f.write("%s\t%s\n" % (main_part_list[i][0], main_part_list[i][1]))
                        
            for j in range(5):
                sub_part_list = []

                for k in range(len(main_part_list[i][2][j])):
                    sub_part_list.append([main_part_list[i][2][j][k], main_part_list[i][3][j][k]])
                
                sub_part_list = sorted(sub_part_list, key = itemgetter(1), reverse = True)
                
                
                for k in range(len(sub_part_list)):
                    if sub_part_list[k][0] != '*':
                        f.write("------------------------(%d)\n"%(j+1))
                        break
                for k in range(len(sub_part_list)):
                    if sub_part_list[k][0] != '*':
                        f.write("%s\t%s\n" % (sub_part_list[k][0], sub_part_list[k][1]))
                
        
    f.close() 
 
def sumTotalWords(word_list):
    sum_stem = 0
    sum_words = 0
    for i in word_list[0][1]:
        sum_stem += i
    for i in word_list[1][1]:
        sum_words += i
    
    return [sum_stem, sum_words]
    
 

def dataframizeKanji(histogram):
        total_frequency = 0
        for element in histogram:
            total_frequency += element[1]
        dataframe = pd.DataFrame(histogram, columns = ['Unit', 'Frequency'])
        dataframe['Rank'] = dataframe.index + 1
        dataframe['Usage'] = 100*dataframe['Frequency']/total_frequency
        dataframe['Expected'] = histogram[0][1]*(1/dataframe['Rank'])
    
        return dataframe
    
def dataframizeWords(histogram):
        total_frequency = 0
        for element in histogram:
            total_frequency += element[2]
        dataframe = pd.DataFrame(histogram, columns = ['Unit', 'Type', 'Frequency'])
        dataframe['Rank'] = dataframe.index + 1
        dataframe['Usage'] = 100*dataframe['Frequency']/total_frequency
        dataframe['Expected'] = dataframe['Frequency']*(1/dataframe['Rank'])
    
        return dataframe



def independentize(data, sampling_width = 20):
    filtered = []
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if data[i][j] == '*':
                try:
                    if data[i][j:j+3] + data[i][j+5:j+7] == "*****":
                        isMatching = 0
                        for k in range(0, len(filtered)):
                            if data[i][j-sampling_width:j] in filtered[k] or data[i][j+6:j+6+sampling_width] in filtered[k]:
                                isMatching = 1
                                break
                            else:
                                isMatching = 0
                        if not isMatching:
                            filtered.insert(0, data[i])
                except:
                    pass
    return filtered
            
def zipf_plot(dataframe):
    plt.scatter(dataframe['Rank'], dataframe['Frequency'], color = 'red')
    plt.scatter(dataframe['Rank'], dataframe['Expected'], color = 'blue')
    plt.title('Frequency vs Rank')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.show()
    
    plt.scatter(dataframe['Rank'], dataframe['Frequency'], color = 'red')
    plt.scatter(dataframe['Rank'], dataframe['Expected'], color = 'blue')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Frequency vs Rank')
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.show()
        