#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:15:00 2017

@author: andrei
"""


import numpy as np
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
import csv
csv.field_size_limit(sys.maxsize)

from nltk.corpus import stopwords
stopwords = stopwords.words('english')

cwd = os.getcwd()
directory = os.path.dirname(cwd) + '/Data/'

def compute_logodds(dict_docs, corpus_ref, include_all = False):
    
    for word in stopwords:
        try:
            dict_docs.pop(word, None)
            corpus_ref.pop(word, None) 
        except:
            pass
    
    total_ref = sum(corpus_ref[key] for key in corpus_ref.keys())
    total_doc = sum(dict_docs[key] for key in dict_docs.keys())
    
    significative_words = list()
    list_values = list()
    keys_ordered = dict_docs.keys()
    
    for word in keys_ordered:
        try : 
            corpus_ref[word]
        except :
            corpus_ref[word] = 1
            
        log_odd = np.log(dict_docs[word]) - np.log(total_doc) - np.log(corpus_ref[word]) + np.log(total_ref)

        if include_all == False:   
            if log_odd > 0:
                list_values.append(log_odd)
                significative_words.append(word)
        else :
            list_values.append(log_odd)
            significative_words.append(word)
                
    return significative_words, list_values

def import_total_count():
    total_count = dict()
    cwd = os.getcwd()
    directory = os.path.dirname(cwd) + '/Data/'
    with open(directory + 'nyt_frequency.csv', 'rb') as csvfile:
        fi = csv.reader(csvfile, delimiter=',')
    
        for row in fi:
            total_count[row[0]] = np.float(row[1])

    return total_count


#Open glove Word2vec embedding
def load_glove(dimension):

    glove = dict()
    namefile = directory + 'glove.6B.' + str(dimension) + 'd.txt'
    with open(namefile, 'r') as csvfile:
        fi = csvfile.read().splitlines() 
        for row in fi:
            row = row.split(' ')
            glove[row[0]] = np.array([float(x) for x in row[1::]])
        return glove

def load_oxford_core():
    with open(directory + 'core_oxford.txt') as f:
        core_words = f.read().split(';')
    return core_words

def load_meriam_core():
    with open(directory + 'core_meriam.txt') as f:
        core_words = f.read().split(';')
    return core_words


def import_bbcdict():

    dict_final = dict()
    with open(directory +'BBCData.csv', 'rb') as csvfile :
        fi = csv.reader(csvfile, delimiter=',')
        for row in fi:
            dict_final[row[0]] = np.float(row[1])
        
    return dict_final


def import_aoa():
    dict_final = dict()
    with open(directory +'aoa.csv', 'rb') as csvfile :
        fi = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(fi):
            if i != 0:
                try:
                    dict_final[row[0]] = np.float(row[4])
                    
                except:
                    pass
        
    return dict_final

#Open topical representation of words
def load_topical_representation(dimension):
    topical_representation = dict()
    namefile = directory + str(dimension) + '_dim_topical.csv'
    with open(namefile, 'r') as csvfile:
        fi = csvfile.read().splitlines() 
        for row in fi:
            row = row.split(',')
            topical_representation[row[0]] = np.array([float(x) for x in row[1::]])
    return topical_representation