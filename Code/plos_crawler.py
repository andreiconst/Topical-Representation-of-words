#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 11:49:43 2017

@author: andrei
"""

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
from random import shuffle, randint, seed
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="path to file of words to lookup")
parser.add_argument("-max_time", nargs='?', help="max number of seconds to wait before to initiate query")

args = parser.parse_args()


def create_url_list():
    journals_dict = dict()
    journals_dict['biology']=['http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.100', 2600]
    journals_dict['medecine']=['http://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.100', 2370]
    journals_dict['computational_biology']=['http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.100', 5725]
    journals_dict['genetics']=['http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.100', 6990]
    journals_dict['neglected_tropical_diseases']=['http://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.000', 5870]
    journals_dict['pathogens']=['http://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.100', 6570]
    
    
    all_urls_plos = list()
    for fields in journals_dict.keys():
        for i in range(1,journals_dict[fields][1]+1):
            if i < 10:
                url = journals_dict[fields][0] + str('000') + str(i)
            elif i < 100:
                url = journals_dict[fields][0] + str('00') +str(i)
            elif i < 1000:
                url = journals_dict[fields][0] + str('0') +str(i)
            else:
                url = journals_dict[fields][0] + str(i)
            all_urls_plos.append(url)
    
    
    seed(12345)
    shuffle(all_urls_plos)

    
    return all_urls_plos


def plos_crawler(list_of_urls = None, max_time = 10):
    if type(list_of_urls) == None:
        url_list = create_url_list()
    else:
        with open(list_of_urls) as f:
            url_list = f.read().split(',')


    try:
        plos_database = pd.read_csv('plos_database.csv', sep=',')
        plos_database = plos_database[['url', 'field','abstract','summary']]
        so_far = len(plos_database)
    except:
        plos_database = pd.DataFrame(columns=('url', 'field','abstract','summary',))
        so_far = 0
        
    new_url_list = url_list[so_far:len(url_list)]
    
    for url in new_url_list:
        
        wait_time = randint(0, max_time)
        time.sleep(wait_time)
        
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
        abstract = re.findall(r'(?s)Abstract(.*?)Author Summary', text)
        summary = re.findall(r'(?s)Author Summary(.*?)Citation', text)
    
    
        if len(abstract)==0:
            abstract_final = 'abstract not found'
        else:
            abstract_final = abstract[0]
        
        if len(summary)==0:
            summary_final = 'summary not found'
        else:
            summary_final = summary[0]
        
        field = re.findall(r'.org/(.*?)/article', url)
        
        plos_database.loc[so_far] = [url, field[0], abstract_final,summary_final]
        
        so_far += 1
        
        if so_far %50==0:
            print so_far
            plos_database[['url', 'field','abstract','summary']].to_csv('plos_database.csv', sep=',', encoding='utf-8')
    plos_database[['url', 'field','abstract','summary']].to_csv('plos_database.csv', sep=',', encoding='utf-8')
        
        
if __name__ == "__main__":
    if type(args.max_time) == type(str()):
        plos_crawler(args.file_name, np.int(args.max_time))
    else:
        plos_crawler(args.file_name)
        

