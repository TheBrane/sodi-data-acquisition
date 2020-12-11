"""
  Tashlin Reddy
  November 2020
  Standardize Topic Json Column 
"""

import sys
import pandas as pd
import json


def brane_standardize(some_string):
    """
    Parameters
    ----------
    some_string : str
        Column of Strings to be standardized

    Returns
    -------
    word : str
        Standardized String
    """
    word = some_string.strip()
    word = word.replace(" ", "_")
    word = word.lower().capitalize()
    word = word.replace("_", " ")
    return word

def main(argv):
    """
    Parameters
    ----------
    Argv1 : str
        Topics Json file path.
    Argv2 : str
        Title of Column to be Standardized
    Argv3 : str
        Output File Name
    Returns
    -------
    Output : Topic Json
        Input File with standardized column as Output Name.
    """

    if len(sys.argv) < 4:
        sys.exit("Enter: <Input File Path> <Column Title> <Output File Name>")

    # Print total number of arguments
    print ('Total number of arguments:', format(len(sys.argv)))

    print('Topic json file path:',  str(argv[0]))
    print('Column name to standardize:',  str(argv[1]))
    print('Output file name:',str(argv[2]))

    json_file = str(argv[0])
    title_col = str(argv[1])
    output_file = str(argv[2])
    df_topics = pd.read_json(json_file)

    title_series = df_topics['title']
    standardize_series = title_series.apply(brane_standardize)
    df1 = standardize_series.to_frame(name='title')
    df_topics = df_topics.assign(title=df1['title'])
    text_json = json.dumps([row.dropna().to_dict() for index,row in df_topics.iterrows()])
    cleaned_json = eval(text_json)
    with open(output_file, 'w') as json_file:
        json.dump(cleaned_json, json_file)

if __name__ == "__main__":
   main(sys.argv[1:])