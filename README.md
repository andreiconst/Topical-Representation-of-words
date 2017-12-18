# Files and code description

## Code
### 1 - toolbox
Necessary function to run the other codes, mainly include loading data

### 2 - topical_lexicon
Computes the topical representation of words

Parameters:<br />
**dimensions :** number of dimensions, from 0 to 300, default 100<br />
**threshold :** threshold of counts. Words in the topical corpus chose count is below this threshold are not considered, default 10<br /><br />

Returns:<br />
**topical representation of words:** dictionary whose keys are words, and values are the vector of its topical representation

### 3 - topical_lexicon_augmented
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
### 1 - Extended topical representation of words for 50 000 words
The 300-topic representation of words. To get partial topical representation of words, e.g. for only 100 dimensions, truncate the vector<br />
/Data/300_dim_topical.csv<br /><br />

[Column 1] = word<br />
[Column 2 to end] = score of association of word to the topic<br />

### 2 - PLOS Abstract summary pairs
Lay summary and abstract pair from the PLOS journal <br />
/Data/plos_abstract_summary.csv<br /><br />
[Column 1] = url<br />
[Column 2] = field, i.e. the subjournal the article was extracted from<br />
[Column 2] = abstract<br />
[Column 3] = summary<br />
Number of abstract / summary pairs : 20 000 

### 3 - Meriam webster defition
Definitions of words from the Meriam Webster Learner dictionary <br />
/Data/meriam_webster_definitions.csv<br /><br />
[Column 1] = word<br />
[Column 2] = definition in Meriam Webster learner dictionary<br />
Number of definitions: 36 000<br />

