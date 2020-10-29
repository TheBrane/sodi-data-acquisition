# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:27:30 2020

@author: rish-r
"""
from config import *
from initialize_arango import *
from ontology_mapper import *

from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json
import requests
import time
from pathlib import Path


def create_references(from_id, to_id, triple):
    try:
        e = {}
        if from_id != to_id:
            db = intialize_client()
            # Get the AQL API wrapper.
            aql = db.aql
            if triple[1] == 'https://schema.org/citation':
                edg = db.collection('References')
            e['_id'] = search_references(from_id, to_id)
            if e['_id'] == 0:
                e = edg.insert({'_from': from_id, '_to': to_id, 'RDF': triple})
                print(e['_id'], "edge created")
            else:
                print('edge already exists', e['_id'])
    except (DocumentInsertError):
        print('DocumentInsertError')
        pass
    return e


def search_references(from_id, to_id):
    """
    Parameters
    ----------
    from_id : str
        Document _id of 'from' vertex.
    to_id : str
        Document _id of 'to' vertex.
    Returns
    -------
    ID : str
        Document _id of edge.
    """
    # search if DOI exists in memo
    if str((from_id, to_id)) in memo_ref_ID:
        return memo_ref_ID[str((from_id, to_id))]
    else:
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql
        edg = db.collection('References')
        aq='FOR doc IN References FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
        # Execute AQL query to match existing records in DB
        cursor = list(db.aql.execute(aq))
        if len(cursor) == 0:
            return 0
        else:
            return cursor[0]


# Create references/citations edges from crossref works
def create_edges_reference(data):
    """
    Parameters
    ----------
    data : JSON dict
        A single corssref JSON file, containing a work.
    Returns
    -------
    tot_ref, cre_ref : total number of references, 
                        number of references created.
    """
    e = []
    #ref_DOI_list = []
    tot_ref = cre_ref = 0
    try:
        from_DOI = data.get('message').get('DOI', 0)
        from_ID = search_works(from_DOI)
        if from_ID != 0:
            references = data.get('message').get('reference')
            if references is not None:
                for ref in references:
                    to_DOI = ref.get('DOI', 0)
                    to_ID = search_works(to_DOI)
                    print(from_ID, from_DOI, '--->', to_ID, to_DOI, 'ref#', tot_ref)
                    if to_ID != 0:
                        #ref_DOI_list.append(to_DOI)
                        trip = [from_DOI, predicate_citation, to_DOI]
                        e = create_references(from_ID, to_ID, trip)
                        memo_ref_ID[str((from_ID, to_ID))] = e['_id']
                        cre_ref += 1
                    else:
                        memo_TBD_DOI[to_DOI] = 'NA'
                    tot_ref += 1
                #memo_ref_DOI[from_DOI] = ref_DOI_list
            else:
                print('No references in file. DOI #', from_DOI)
    except (TypeError, AttributeError):
        print('Exception : None found')
        pass
    return tot_ref, cre_ref


def main():
    # create references edges from crossref JSON files
    start = time.time()
    file_num = 0
    for files in json_folder.iterdir():
        with open(files) as f:
            data = json.load(f)
        tot_ref, cre_ref = create_edges_reference(data)
        print('#', file_num, ', File name:', files)
        print('Total refs', tot_ref, ', Created refs', cre_ref)
        print('============================================')
        file_num += 1

    json.dump(memo_ref_DOI, open("memo_ref_DOI.json", 'w'))
    json.dump(memo_ref_ID, open("memo_ref_ID.json", 'w'))
    json.dump(memo_TBD_DOI, open("memo_TBD_DOI.json", 'w'))
    
    end = time.time()
    print('crossref references load, create references',end - start)

if __name__ == "__main__":
    main()
