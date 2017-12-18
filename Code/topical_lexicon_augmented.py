#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:21:32 2017

@author: andrei
"""

import numpy as np
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
import csv
csv.field_size_limit(sys.maxsize)
from sklearn.linear_model import Ridge
from scipy.stats import spearmanr, pearsonr
from toolbox import * 


cwd = os.getcwd()
directory = os.path.dirname(cwd) + '/Data/'
directory_nyt = directory + 'descriptors_count_dimensions/'

def import_score_lexicon_augmented(words_corpus = None, dimensions = 100, alpha = 1e-5, threshold = 10, dimensions_glove = 100, return_r = False):
    #Open NYT lexicon
    complete_nyt_dict = dict()
    glove = load_glove(dimensions_glove)
    r_scores = list()

    with open(directory + 'descriptors_nyt.csv', 'rb') as csvfile:
        fi = csv.reader(csvfile, delimiter=',')
        topics = list()
        for i, row in enumerate(fi):
            if i != 0:
                topics.append(row[1]) 
    topics = [topics[i] + 'counter' for i in range(dimensions)]


    if type(words_corpus) != None:
        words_tokeep = list(set(words_corpus).intersection(set(glove.keys())))  
    else:
        words_tokeep = glove.keys()
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
        words_topredict = list(set(words_tokeep) - set(words))
        
        x = list()
        y = list()
        
        for j, word in enumerate(words) :
            try:
                x.append(glove[word] / np.sqrt(np.dot(glove[word].T, glove[word])))
                y.append(score[j])
            except:
                pass
        clf = Ridge(alpha=alpha, random_state = 123).fit(x, y)
        
        for j, word in enumerate(words) :
            try:
                if i == 0:
                    complete_nyt_dict[word] = np.zeros(len(topics))
                complete_nyt_dict[word][i] = score[j]
            except:
                pass
        
        if return_r == True:
            predictions = clf.predict(x)
            r_scores.append([pearsonr(predictions, y)[0], spearmanr(predictions, y)[0], len(x)])
        
        temp_list_features = list()
        for word in words_topredict:
            temp_list_features.append(glove[word] / np.sqrt(np.dot(glove[word].T, glove[word])))

        predictions = clf.predict(temp_list_features)
        for k in xrange(len(predictions)):
            if i == 0:
                complete_nyt_dict[words_topredict[k]] = np.zeros(len(topics))
            complete_nyt_dict[words_topredict[k]][i] = predictions[k]  
    if return_r == False:
        return complete_nyt_dict
    else:
        return complete_nyt_dict, r_scores

