# Author: Songhee Kim <songheekim@mcw.edu>

"""This script extracts the transitive (i.e., containing 'dobj') and intransitive (i.e., everything else) counts 
from Google Syntactic Ngram (Unlex Verbargs was used here). The script reads each file, turns it into a dictionary, 
keeps only the data from the year 1950 or later, and then construct a dictionary conataining the number of occurrences of 
(in)transitivity, and finally exports the results to an excel file.  
Link to the Google syntactic N-gram: http://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html """

import pandas as pd
import csv
import os
import sys

csv.field_size_limit(sys.maxsize)

filenames = os.listdir("./unlex")
filenames.sort()
#print (len(filenames))

ngram_dict = {}

for filename in filenames:
    raw_data = []
    with open("/home/songkim/Documents/verb_transitivity/unlex/"+filename) as f:
            reader = csv.reader(f, delimiter='\t')
            raw_data = [r for r in reader]
            df = pd.DataFrame(data=raw_data)
            print (filename, df.shape)
            #print ('the first df shape is :', df.shape)
            df = df.rename(columns={0: 'entry', 1: 'ngram', 2:'totalN'})
            df_dict = df.to_dict(orient='index')
            for k, v in df_dict.items():
                v['totalRecentN'] = 0 ### add a new key here
                for i in range(3, len(v.keys())-1): ## iterate column 3 onward, -1 because we added a key
                    if v[i] != None: 
                        split = v[i].split(',')
                        year = int(split[0])
                        count = int(split[1])
                        if year > 1949:
                            #print(year)
                            v['totalRecentN'] += count
            #print ('df_dict keys N: ', len(df_dict.keys()))
            keys_to_extract = ['entry', 'ngram', 'totalN', 'totalRecentN']
            df_dict_compact = {}
            for k, v in df_dict.items():
                new_v = {key:df_dict[k][key] for key in keys_to_extract}
                df_dict_compact[k] = new_v
            #print ('df_dict_compact has keys: ', len(df_dict_compact.keys()))
            for v in df_dict_compact.values():
                entry = v['entry']
                ngram = v['ngram']
                totalrecentN = v['totalRecentN']
                if entry not in ngram_dict.keys():
                    ngram_dict[entry] = {'transitive': 0, 'intransitive':0, 'totalcount': 0}
                if 'dobj' in ngram:
                    ngram_dict[entry]['transitive'] += totalrecentN
                else:
                    ngram_dict[entry]['intransitive'] += totalrecentN
                ngram_dict[entry]['totalcount'] += totalrecentN

df_out = pd.DataFrame.from_dict(ngram_dict, orient='index') 
df_out.to_excel('/home/songkim/Documents/verb_transitivity/Transitivity_from_GoogleNgram.xlsx')            