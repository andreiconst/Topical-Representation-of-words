# Files and code description

## Code

### 1 - meriam_crawler.py
Crawls the Meriam Webster learner dictionary and extracts definition <br /><br />
Parameters:<br />
**file_name :** file_name with the words to look up, words, comma separated
**max_time :** max number of seconds befond sending the next query, default 10, optional <br /><br />

```
python meriam_crawler.py test_words.txt -max_time 5
```

### 2 - plos_crawler.py
Crawls the PLOS journal webstise dictionary and extracts abstract summary pairs <br /><br />
Parameters:<br />
**file_name :** file_name with the words to look up, words, comma separated
**max_time :** max number of seconds befond sending the next query, default 10, optional <br /><br />

```
python plos_crawler.py test_plos.txt -max_time 5
```

### 3 - toolbox.py
Necessary function to run the other codes, mainly include loading data

### 4 - topical_lexicon.py
Computes the topical representation of words

Parameters:<br />
**dimensions :** number of dimensions, from 0 to 300, default 100<br />
**threshold :** threshold of counts. Words in the topical corpus chose count is below this threshold are not considered, default 10<br /><br />

Returns:<br />
**topical representation of words:** dictionary whose keys are words, and values are the vector of its topical representation

### 5 - topical_lexicon_augmented.py
Computes the topical representation with an extension based on glove features<br /><br />

Parameters:<br />
**words_corpus:** words whose representation is needed, if none is provided then computes representation for all words present in glove, which is usually a lengthy process<br />
**dimensions:** number of dimensions, from 0 to 300, default 100<br />
threshold: threshold of counts. Words in the topical corpus chose count is below this threshold are not considered, default 10<br />
**alpha:** value of the regularizer, default 1e-5<br />
**dimensions_glove:** number of glove dimension representation with which to infer topical scores. To save space we only included the 100 dimensional distributed representation, default 100<br />
**return_r:** Return the r_pearson and r_spearman coefficients for each topic<br /><br />

Return:<br />
**topical representation of words:** dictionary whose keys are words, and values are the vector of its topical representation<br />
**if return_r = True:** returns as well the r_pearson and r_spearman coefficients for each topic, as a list of tuple [r_pearson, r_spearman]


## Datasets
### 1 - Extended topical representation of 50 000 words
The 300-topic representation of words. To get partial topical representation of words, e.g. for only 100 dimensions, truncate the vector<br />
/Data/300_dim_topical.csv<br /><br />

[Column 1] = word<br />
[Column 2 to end] = score of association of word to the topic<br />

### 2 - PLOS Abstract summary pairs
Lay summary and abstract pair from the PLOS journal <br />
/Data/plos_abstract_summary.csv<br /><br />
[Column 1] = url<br />
[Column 2] = field, i.e. the subjournal the article was extracted from<br />
[Column 3] = abstract<br />
[Column 4] = summary<br />
Number of abstract / summary pairs : 20 000 

### 3 - Meriam webster definition
Definitions of words from the Meriam Webster Learner dictionary <br />
/Data/meriam_webster_definitions.csv<br /><br />
[Column 1] = word<br />
[Column 2] = definition in Meriam Webster learner dictionary<br />
Number of definitions: 36 000<br />

### 3 - Meriam webster tags
Definitions of words from the Meriam Webster Learner dictionary <br />
/Data/tag_index_meriam.csv<br /><br />
[Column 1] = tag<br />
[Column 2] = words that belong to the tag, ';' separated <br />
To read the file as a dictionary:
```
import csv
inverted_index_meriam = dict()
with open('tag_index_meriam.csv', 'r') as csvfile:
    fi = csvfile.read().splitlines() 
    for row in fi:
        row = row.split(',')
        inverted_index_meriam[row[0]] = row[1].split(';')
```
