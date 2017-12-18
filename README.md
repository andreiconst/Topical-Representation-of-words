# Topical-Representation-of-words
Research project conducted at the University of Pennsylvania

# Code
## 1 - toolbox
Necessary function to run the other codes, mainly include loading data

## 2 - topical_lexicon
Computes the topical representation without extension of glove features

Parameters:
dimensions : number of dimensions, from 0 to 300, default 100
threshold : threshold of counts. Words in the topical corpus chose count is below this threshold are not considered, default 10

Returns:
topical representation of words, dictionary whose keys are words, and values are the vector of its topical representation

## 3 topical_lexicon_augmented
Computes the topical representation with an extension based on glove features

Parameters:
words_corpus : words whose representation is needed, if none is provided then computes representation for all words present in glove, which is usually a lengthy process
dimensions : number of dimensions, from 0 to 300, default 100
threshold : threshold of counts. Words in the topical corpus chose count is below this threshold are not considered, default 10
a : value of the regularizer, default 1e-5
dimensions_glove : number of glove dimension representation with which to infer topical scores. To save space we only included the 100 dimensional distributed representation, default 100
return_r = Return the r_pearson and r_spearman coefficients for each topic

Return:
1 - topical representation of words, dictionary whose keys are words, and values are the vector of its topical representation
2 - if return_r = True, returns as well the r_pearson and r_spearman coefficients for each topic


# Datasets
## 1 - Extended topical representation of words for 50 000 words
/Data/300_dim_topical.csv

[Column 1] = word
[Column 2 to end] = score of association of word to the topic
To get partial topical representation of words, truncate the vector

## 2 - PLOS Abstract summary pairs
/Data/plos_abstract_summary.csv
[Column 1] = url
[Column 2] = field, i.e. the subjournal the article was extracted from
[Column 2] = abstract
[Column 3] = summary
Number of abstract / summary pairs : 20 000 

## 3 - Meriam webster defition
/Data/meriam_webster_definitions.csv
[Column 1] = word
[Column 2] = definition in Meriam Webster learner dictionary
Number of definitions: 36 000

