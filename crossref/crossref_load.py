# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 2020

@author: rish-r
"""
# Extract from Crossref JSON files, Crossref API, load into ArangoDB KG
from config import *
from initialize_arango import *
from ontology_mapper import *

from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json
import requests
import time
import gzip
from pathlib import Path


def search_doc(uri, collection_name, label=None):
    """
    Parameters
    ----------
    uri :str
        Resource identifier for RDF subject or object, typically URL.
    collection_name : str
        ArangoDB collection name.
    label : str, optional
        label of the node document. The default is None.

    Returns
    -------
    ID : str
        Document _id from a collection.
    """
    try:
        collec = db.collection(collection_name)
        aq='FOR doc IN '+str(collection_name)+' FILTER doc.label=="'+str(label)+'" OR doc.URI=="'+str(uri)+'" RETURN doc._id'
        # Execute AQL query to match existing records in DB
        ID = list(db.aql.execute(aq))
        if ID:
            return ID
        else:
            print("Document not found")
            return 0
    except IndexError as e:
        print(e)
        return 0


def load_crossref_data(data):
    """
    Parameters
    ----------
    data : JSON
        A single corssref JSON file, containing a work.
    Returns
    -------
    ID : str
        ArangoDB document _id(also called handle), which uniquely identifies
        the document across all collections within a DB.
    """
    ### standardize DOI to uppercase, it is case-insensitive
    DOI = data.get('DOI').upper()
    URL = data.get('URL')
    title = str(data.get('title'))[1:-1]
    subject = data.get('subject')
    work_type = data.get('type')
    # additional data passed as fields dict
    fields = {'DOI': DOI, 'title': title, 'subject': subject,
              'work_type': work_type, 'data': data}
    #print(fields)
    ID = create_works(DOI, subject_type_work, fields)
    memo_DOI_ID.update({DOI: ID})
    return ID


def load_crossref_resp(crossref_url, parameters=None):
    """
    Parameters
    ----------
    fetch_url : str
        Crossref API URL.
    parameters : dict, optional
        dict containing URL parameters. The default is None.
    Returns
    -------
    record_num : int
        number of records loaded.
    """
    record_num = 0
    ID = ""
    response = requests.get(crossref_url, params=parameters)
    response = response.json().get('message').get('items')
    #print(response.json().get('message').get('items'))
    for record in response:
        ### standardize DOI to uppercase, it is case-insensitive
        DOI = record.get('DOI').upper()
        title = str(record.get('title'))[1:-1]
        fields = {'DOI': DOI, 'title': title, 'data': record}
        #print(DOI, subject_type, fields)
        ID = create_works(DOI, subject_type, fields)
        memo_DOI_ID.update({DOI: ID})
        record_num += 1
    return record_num

    
def main():
    start = time.time()
    #initialize_database(db_name, user, password)
    #initialize_memos()

    #load from crossref gz files
    i = 0
    for file in nature_folder.iterdir():
        print(i)
        i += 1
        with gzip.open(file, 'rb') as f:
            lines = json.load(f)
        lines = lines.get('items')
        line_num = 0
        for data in lines:
            #print(data)
            if data:
                ID = load_crossref_data(data)
                line_num += 1
                print("created #", line_num)        
            else:
                continue
    
    print("Total number of files:", i)
    json.dump(memo_DOI_ID, open("memo_DOI_ID.json", 'w'))
    json.dump(memo_TBD_DOI, open("memo_TBD_DOI.json", 'w'))
    end = time.time()
    print('crossref load, create works',end - start)


# =============================================================================
#     #load from crossref JSON files
#     file_num = 0
#     for files in json_folder.iterdir():
#         with open(files) as f:
#             data = json.load(f)
#         data = data.get('message')
#         ID = load_crossref_data(data)
#         file_num += 1
#         # print("created #", file_num)
# =============================================================================

# =============================================================================
# url = 'https://api.crossref.org/works'
# 
# parameters = {'query.author' : 'demis+hassabis',
#               'rows' : 2
#                           }
# =============================================================================

# =============================================================================
#     #load from crossref API, random sample of 10 records
#     crossref_url ='http://api.crossref.org/works?sample=10'
#     parameters = {"select":"DOI,title"}
#     
#     rec_count = load_crossref_resp(crossref_url, parameters)
#     print('Total number of records:', rec_count)
# 
# =============================================================================



if __name__ == "__main__":
    main()
