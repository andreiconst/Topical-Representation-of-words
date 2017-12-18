#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:17:48 2017

@author: andrei
"""


import numpy as np
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
import csv
csv.field_size_limit(sys.maxsize)
from toolbox import * 
import os


cwd = os.getcwd()
directory = os.path.dirname(cwd) + '/Data/'
directory_nyt = directory + 'descriptors_count_dimensions/'

def import_score_lexicon(dimensions = 100, threshold = 10):
    
    #Open NYT lexicon
    NYT_lexicon = dict()

    with open(directory + 'descriptors_nyt.csv', 'rb') as csvfile:
        fi = csv.reader(csvfile, delimiter=',')
        topics = list()
        for i, row in enumerate(fi):
            if i != 0:
                topics.append(row[1]) 
    topics = [topics[j] + 'counter' for j in range(dimensions)]
        
    
    dict_ref = import_total_count()
    
    for i, topic in enumerate(topics):
        name_file = directory_nyt + topic + '.csv'
        dict_temp = dict()
        with open(name_file, 'rb') as csvfile :
            fi = csv.reader(csvfile, delimiter=',')
            for row in fi:
                if np.float(row[1]) > threshold:
                    dict_temp[row[0]] = np.float(row[1])

            
        words, score = compute_logodds(dict_temp, dict_ref, include_all = True)
        
        
                    
        words_to_add = list(set(words) - set(NYT_lexicon.keys()))
        words_already_there = list(set(NYT_lexicon.keys()).intersection(set(words)))
        for w in words_to_add:
               NYT_lexicon[w] = np.zeros(len(topics))
               NYT_lexicon[w][i] = score[words.index(w)]
        for w in words_already_there:
               NYT_lexicon[w][i] = score[words.index(w)] 
    return NYT_lexicon


temp = import_score_lexicon()