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
    for j in range(0, len(stringSet)):  
        adjustment = 0
        #loop through each character of the current text entry
        for i in range(0, len(stringSet[j])): 
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
        
        #create two temporary lists to store kanji and respective frequency, and apply occurence modes
        temp_kanji = []
        temp_frequencies = []
        for character in line:
            
            #check if the character is a kanji or not
            if character not in all_full and character.isalnum():
    
                if character not in temp_kanji:
                    #if the kanji is not in the temp list create a new entry with a frequency of 1
                    temp_kanji.append(character)
                    temp_frequencies.append(1)
                    
                elif character in temp_kanji:
                    #if the kanji is in the temp list, then just increment the respective frequency by 1
                    temp_frequencies[temp_kanji.index(character)] += 1
                    
        
        #loop to update the main kanji and frequency lists
        for character in temp_kanji:
            
            
            if character not in kanji_list:
                kanji_list.append(character)
                if line_occurrence == 'multiple':
                    frequency_list.append(temp_frequencies[temp_kanji.index(character)])
                elif line_occurrence == 'single':
                   frequency_list.append(1)
                
            elif character in kanji_list:
                if line_occurrence == 'multiple':
                    frequency_list[kanji_list.index(character)] += temp_frequencies[temp_kanji.index(character)]
                elif line_occurrence == 'single':
                    frequency_list[kanji_list.index(character)] += 1
                
    if len(kanji_list) != len(frequency_list):
        raise DataMismatchError("Kanji frequencies are not equal to the number of characters")
        
    histogram = []
    for i in range(0, len(kanji_list)):
        histogram.append([kanji_list[i], frequency_list[i]])
    
    histogram = sorted(histogram, key = itemgetter(1), reverse = descending)
            
    if return_type == 'list':

        return histogram
    
    elif return_type == 'dataframe':
        dataframe = pd.DataFrame(histogram, columns = ['Kanji', 'Frequency'])
        dataframe['Rank'] = dataframe.index + 1
        dataframe['Expected'] = dataframe['Frequency']*(1/dataframe['Rank'])
    
        return dataframe



def histogramizeWords(set_of_lines, line_occurrence = 'multiple', descending = True, return_type = 'list'):
    unit_list = [[],[]]
    type_list = [[], []]
    frequency_list = [[],[]]
    type_histogram = [[],[]]
    length = len(set_of_lines)
    counter = 0
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.B
    for line in set_of_lines:
        counter += 1
        if counter % 20 == 0:
            print("(%d/%d)"%(counter, length))
        temp_units = [[],[]]
        temp_types = [[],[]]
        temp_frequencies = [[],[]]
        for m in tokenizer_obj.tokenize(line, mode):
            
            if m.dictionary_form() in all_full:
                continue

            if m.surface() not in temp_units[0]:
                temp_units[0].append(m.surface())
                temp_types[0].append(m.part_of_speech()[0])
                temp_frequencies[0].append(1)
            elif m.surface() in temp_units[0]:
                temp_frequencies[0][temp_units[0].index(m.surface())] += 1
                
                
            if m.dictionary_form() not in temp_units[1]:
                temp_units[1].append(m.dictionary_form())
                temp_types[1].append(m.part_of_speech()[0])
                temp_frequencies[1].append(1)
            elif m.dictionary_form() in temp_units[1]:
                temp_frequencies[1][temp_units[1].index(m.dictionary_form())] += 1
                
                
            if m.part_of_speech()[0] not in type_histogram[0]:
                type_histogram[0].append(m.part_of_speech()[0])
                type_histogram[1].append(1)
            elif m.part_of_speech()[0] in type_histogram[0]:
                type_histogram[1][type_histogram[0].index(m.part_of_speech()[0])] += 1                    
                    

        for unit in temp_units[0]:
            if unit not in unit_list[0]:
                unit_list[0].append(unit)
                type_list[0].append(temp_types[0][temp_units[0].index(unit)])
                if line_occurrence == 'multiple':
                    frequency_list[0].append(temp_frequencies[0][temp_units[0].index(unit)])
                elif line_occurrence == 'single':
                   frequency_list[0].append(1)
                
            elif unit in unit_list[0]:
                if line_occurrence == 'multiple':
                    frequency_list[0][unit_list[0].index(unit)] += temp_frequencies[0][temp_units[0].index(unit)]
                elif line_occurrence == 'single':
                    frequency_list[0][unit_list[0].index(unit)] += 1
                
                
        for unit in temp_units[1]:
            if unit not in unit_list[1]:
                unit_list[1].append(unit)
                type_list[1].append(temp_types[1][temp_units[1].index(unit)])
                if line_occurrence == 'multiple':
                    frequency_list[1].append(temp_frequencies[1][temp_units[1].index(unit)])
                elif line_occurrence == 'single':
                   frequency_list[1].append(1)
                
            elif unit in unit_list[1]:
                if line_occurrence == 'multiple':
                    frequency_list[1][unit_list[1].index(unit)] += temp_frequencies[1][temp_units[1].index(unit)]
                elif line_occurrence == 'single':
                    frequency_list[1][unit_list[1].index(unit)] += 1
                
    if len(unit_list[0]) != len(frequency_list[0]):
        raise DataMismatchError("Unit frequencies are not equal to the number of units")
        
    histogram = [[],[],[]]
    for i in range(0, len(unit_list[0])):
        histogram[0].append([unit_list[0][i], type_list[0][i], frequency_list[0][i]])
    
    for i in range(0, len(unit_list[1])):
        histogram[1].append([unit_list[1][i], type_list[1][i], frequency_list[1][i]])
        
    for i in range(0, len(type_histogram[0])):
        histogram[2].append([type_histogram[0][i], type_histogram[1][i]])
        
    
    histogram[0] = sorted(histogram[0], key = itemgetter(2), reverse = descending)
    histogram[1] = sorted(histogram[1], key = itemgetter(2), reverse = descending)
    histogram[2] = sorted(histogram[2], key = itemgetter(1), reverse = descending)
    
            
    if return_type == 'list':

        return histogram
    

def dataframizeKanji(histogram):
        total_frequency = 0
        for element in histogram:
            total_frequency += element[1]
        dataframe = pd.DataFrame(histogram, columns = ['Unit', 'Frequency'])
        dataframe['Rank'] = dataframe.index + 1
        dataframe['Usage'] = 100*dataframe['Frequency']/total_frequency
        dataframe['Expected'] = dataframe['Frequency']*(1/dataframe['Rank'])
    
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
        