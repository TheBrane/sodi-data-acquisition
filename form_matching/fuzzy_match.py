'''
	Tashlin Reddy
	August 2020
	Fuzzy Match strings in Columns of CSV file 
'''


#read in dependencies

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz


#read in csv form

form = pd.read_csv('form.csv')
#form = pd.read_csv('https...')


#iterate over each column and check if there is a list to fuzzy match
df_new = pd.DataFrame()
for col_num in range(0,form.shape[1]):
    title = form.columns[col_num]
    try:
        if form.iloc[:,col_num].str.contains(',').any() == True:
            matched_series = fuzzy_match_col(col_num)
            df_new[title] = matched_series
        else: 

            df_new[title] = form.iloc[:,col_num]
    except:
        df_new[title] = form.iloc[:,col_num]

#export new matched csv file
df_new.to_csv("fuzz_matched.csv")


#fuzzy match function 

def fuzzy_match_col(col_num):
    keyword_col = form.iloc[:,col_num]
    keywords_lst = keyword_col[0].split(',')

    new_lst = []
    for keyword_lst in keyword_col:
        new_wrds = []
        try:
            keywords = keyword_lst.split(',')
            for word in keywords:
                word = word.strip()
                word = word.replace(" ", "_")
                word = word.lower().capitalize()
                if word != '':
                    new_wrds.append(word)

        except:
            new_wrds.append('NAN')
            
        new_lst.append(new_wrds)
        
    for i in range(1, len(new_lst)):
        for word_list in new_lst[:i]:
            for word in word_list:
                for match in new_lst[i]:
                    score = fuzz.ratio(word, match)
                    if score > 70 and score !=100:
                        #print(word,'=', match, " score:", score)
                        new_lst[i] = [w.replace(match, word) for w in new_lst[i]]

    matched_words = [', '.join(element) for element in new_lst]
    cleaned_words = [w.replace('_', ' ') for w in matched_words]
    return cleaned_words
