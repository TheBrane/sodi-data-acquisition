# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:17:26 2020

@author: rish-r
"""

from config import *
from initialize_arango import *
from ontology_mapper import *

from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json
import requests
import time
import gzip
from pathlib import Path


def create_person_node(author):
    """
    Parameters
    ----------
    author : dict
        author field of JSON file.
    Returns
    -------
    ID : str
        Document _id from 'Person' collection.
    """
    given = author.get('given', '')
    family = author.get('family', '')
    ID = search_person(given, family)
    if ID == 0:
        collec = db.collection('Person')
        para = {'URI': given+'_'+family, 'type': subject_type_author, 'sameas': '', 'given': given, 'family': family}
        metadata = collec.insert(para)
        ID = metadata['_id']
        memo_name_ID.update({str((given, family)): ID})
        print(ID, "created")
        return ID
    else:
        return ID
    

def create_author_edge(DOI_ID, person_ID):
    """
    Parameters
    ----------
    DOI_ID : str
        Document _id from 'Works' collection.
    person_ID : str
        Document _id from 'Person' collection.
    Returns
    -------
    edge_id : str
        Document _id of edge from 'Author' collection.
    """
    edge_id = search_author_edge(DOI_ID, person_ID)
    if edge_id == 0:
        edg = db.collection('Author')
        para = {'_from': DOI_ID, '_to': person_ID, 'RDF': predicate_author}
        metadata = edg.insert(para)
        ID = metadata['_id']
        print(ID, "created")
        return ID
    else:
        return edge_id
    
def create_collaborator_edge(authors):
    """
    Parameters
    ----------
    authors : list of dicts
        list of author fields of JSON file.
    Returns
    -------
    collab_ID : str
        Document _id of edge from 'Collaborator' collection.
    """
    collab_ID = 0
    if len(authors) in [0,1]:
        print('Single or NO author')
        return collab_ID
    for i in range(len(authors)):
        for collab in authors[i+1:]:
            name1 = (authors[i].get('given', ''), authors[i].get('family', ''))

            name2 = (collab.get('given', ''), collab.get('family', ''))
            ID1, ID2, collab_ID = search_collab(name1, name2)
            if ID1 and ID2 and (not collab_ID):
                edg = db.collection('Collaborator')
                para = {'_from': ID1, '_to': ID2, 'RDF': predicate_collaborator}
                metadata = edg.insert(para)
                ID = metadata['_id']
                print(ID, "created")
            elif collab_ID:
                return collab_ID
            else:
                print('Invalid IDs')
                return 0
    return collab_ID


def search_person(given, family, uri=None):
    """
    Parameters
    ----------
    given : str
        Given name of Person.
    family : str
        Family name of Person.
    uri : str, optional
        identifier ID or URI of person. The default is None.
    Returns
    -------
    ID : str
        Document _id from 'Person' collection.
    """
    if str((given, family)) in memo_name_ID:
        return memo_name_ID[str((given, family))]
    else:
        edg = db.collection('Person')
        aq='FOR doc IN Person FILTER doc.given=="'+str(given)+'" AND doc.family=="'+str(family)+'" RETURN doc._id'
        # Execute AQL query to match existing records in DB
        cursor = list(db.aql.execute(aq))
        if len(cursor) == 0:
            return 0
        else:
            return cursor[0]

def search_author_edge(DOI_ID, person_ID):
    """
    Parameters
    ----------
    DOI_ID : str
        Document _id from 'Works' collection.
    person_ID : str
        Document _id from 'Person' collection.
    Returns
    -------
    ID : str
        Document _id of edge from 'Author' collection.
    """
    ed = db.collection('Author')
    aq='FOR doc IN Author FILTER doc._from=="'+str(DOI_ID)+'" AND doc._to=="'+str(person_ID)+'" RETURN doc._id'
    cursor = list(db.aql.execute(aq))
    if len(cursor) == 0:
        return 0
    else:
        return cursor[0]
    
def search_collab(name1, name2):
    """
    Parameters
    ----------
    name1 : tuple of given name, family name
        name of author.
    name2 : tuple of given name, family name
        name of collaborator.
    Returns
    -------
    ID1 : str
        Document _id of author from 'Person' collection.
    ID2 : str
        Document _id of collaborator from 'Person' collection.
    ID : str
        Document _id of edge from 'Collaborator' collection.
    """
    ID1 = search_person(name1[0], name1[1])
    ID2 = search_person(name2[0], name2[1])
    edg = db.collection('Collaborator')
    aq='FOR doc IN Collaborator FILTER doc._from=="'+str(ID1)+'" AND doc._to=="'+str(ID2)+'" RETURN doc._id'
    cursor = list(db.aql.execute(aq))
    if len(cursor) == 0:
        return ID1, ID2, 0
    else:
        return ID1, ID2, cursor[0]
    
def main():
# =============================================================================
#     #load from crossref JSON files
#     file_num = 0
#     for files in json_folder.iterdir():
#         with open(files) as f:
#             data = json.load(f)
#         DOI = data.get('message').get('DOI', '').upper()
#         if DOI == '':
#             continue
#         DOI_ID = search_works(DOI)
#         authors = data.get('message').get('author', '')
#         
#         for author in authors:
#             print('DOI', DOI_ID, 'Author',author)
#             person_ID = create_person_node(author)
#             aid = create_author_edge(DOI_ID, person_ID)
#         cid = create_collaborator_edge(authors)
# 
#         file_num += 1
#         # print("created #", file_num)
#     print("Total number of files:", file_num)
#     json.dump(memo_name_ID, open("memo_name_ID.json", 'w'))
# 
# =============================================================================
    
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
            DOI = data.get('DOI', '').upper()
            if DOI == '':
                continue
            DOI_ID = search_works(DOI)
            authors = data.get('author', '')
        
            for author in authors:
                person_ID = create_person_node(author)
                aid = create_author_edge(DOI_ID, person_ID)
            cid = create_collaborator_edge(authors)

    json.dump(memo_name_ID, open("memo_name_ID.json", 'w'))
if __name__ == "__main__":
    main()
