#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:17:53 2017

@author: andrei
"""

import pandas as pd
import urllib
from bs4 import BeautifulSoup
import re
import time
from random import randint
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="path to file of words to lookup")
parser.add_argument("-max_time", nargs='?', help="max number of seconds to wait before to initiate query")

args = parser.parse_args()


#bbc_words = pd.read_csv('BBCData.csv', sep=',')
#bbc_words = bbc_words.dropna()
#bbc_words = pd.DataFrame.reset_index(bbc_words)

#list_of_words = list()
#for i in range(len(bbc_words)):
#    if bbc_words['Frequency'][i] >=10: 
#        list_of_words.append(bbc_words['Word'][i])
#
#random.seed(12345)
#test = shuffle(list_of_words)
#list_to_save = ','.join(list_of_words)

#f = open("words_to_lookup.txt", "a");
#f.write(list_to_save)
#f.close()
name_file = 'test_words.txt'

def crawl_meriam_webster(name_file, max_time = 10):
    with open(name_file) as f:
        words_list = f.read().split(',')
    
    try:
        meriam_dictionary_learner = pd.read_csv('meriam_webster.csv', sep=',')
        meriam_dictionary_learner = meriam_dictionary_learner[['word', 'extracted_definition']]
        so_far = len(meriam_dictionary_learner)
    
    except :
        meriam_dictionary_learner =  pd.DataFrame(columns=['word', 'extracted_definition'])
        so_far = 0
    
    count = so_far
    new_list = words_list[so_far:len(words_list)]
    
    for word in new_list:
        
        wait_time = np.random.randint(0, max_time)
        time.sleep(wait_time)
        
        url = "http://learnersdictionary.com/definition/" + word
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
    
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        
        # get text
        text = soup.get_text()
        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        final_text = re.findall(r'(?s)Save\n(.*?)Comments & Questions', text)
        if len(final_text)==0:
            meriam_dictionary_learner.loc[count] = [word, 'definition not found']
        else:
            meriam_dictionary_learner.loc[count] = [word, str(final_text[0].encode('utf-8'))]
        count+=1
        
        if count %50==0:
            print count
            meriam_dictionary_learner[['word', 'extracted_definition']].to_csv('meriam_webster.csv', sep=',')
    meriam_dictionary_learner[['word', 'extracted_definition']].to_csv('meriam_webster.csv', sep=',')

if __name__ == "__main__":
    if type(args.max_time) == type(str()):
        crawl_meriam_webster(args.file_name, np.int(args.max_time))
    else:
        crawl_meriam_webster(args.file_name)


