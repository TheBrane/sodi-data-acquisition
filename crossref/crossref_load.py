# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 2020

@author: rish-r
"""
# Extract from ma-graph and OpenCitations, load into ArangoDB KG
from initialize_arango import *
from ontology_mapper import *
from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json
from pathlib import Path



def search_work(DOI, uri=None):
    """
    Parameters
    ----------
    DOI : str
        Digital Object Identifier, is a string of numbers, letters and symbols
        used to permanently identify an article or document and link to it on the web.
    uri :  str, optional
        Resource identifier for RDF subject or object, typically URL.
        The default is None.
    Returns
    -------
    ID : str
        Document _id from 'Work' collection.
    """
    try:
        DOI_upper = str(DOI).upper()
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql
        collec = db.collection('Works')
        aq='FOR doc IN Works FILTER doc.DOI=="'+str(DOI_upper)+'" OR doc.URI=="'+str(uri)+'" RETURN doc._id'
        # Execute AQL query to match existing records in DB
        ID = list(db.aql.execute(aq))
        if ID:
            return ID[0]
        else:
            print("Document not found")
            return 0
    except IndexError as e:
        print(e)
        return 0

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
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql
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
        JSON file format.
    Returns
    -------
    ID : str
        ArangoDB document _id(also called handle), which uniquely identifies
        the document across all collections within a DB.
    """
    # DOI is case insensitive, default to UPPER
    DOI = data.get('message').get('DOI').upper()
    URL = data.get('message').get('URL')
    title = str(data.get('message').get('title'))[1:-1]
    subject = data.get('message').get('subject')
    work_type = data.get('message').get('type')
    # additional data passed as fields dict
    fields = {'DOI': DOI, 'title': title, 'subject': subject,
              'work_type': work_type, 'data': data.get('message')}
    ID = create_nodes(URL, 'http://schema.org/CreativeWork', fields)
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
    response = requests.get(crossref_url, params=parameters)
    for record in response:
        ID = load_crossref_data(record)
        print(record, 'ID :', ID)
        record_num += 1
    return record_num

    
def main():
    #intialize_database(db_name, user, password)

    predicate_citation = 'https://schema.org/citation'
    predicate_author = 'https://schema.org/author'

    json_folder = Path("D:\SODI\Proj\AlphaGO_graph")
    crossref_url = 'https://api.crossref.org/works'

    file_num = 0
    for files in json_folder.iterdir():
        with open(files) as f:
            data = json.load(f)
        ID = load_crossref_data(data)
        file_num += 1
        # print("created #", file_num)
    print("Total files:", file_num)

if __name__ == "__main__":
    main()
