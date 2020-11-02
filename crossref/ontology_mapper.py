# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 19:22:02 2020

@author: rish-r
"""
from config import *
from initialize_arango import *
from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json


def triples_generator(endpoint_url, sparql_query, result_format='json'):
    """
    Parameters
    ----------
    endpoint_url : str
        The SPARQL endpoint URL of the database you want to query
    sparql_query : str
    result_format : str, optional
        The default is 'json'. Can take 'xml','rdf+xml','n3'.

    Returns
    -------
    Depends on result_format.
    Note:From the SPARQL specification-
    https://www.w3.org/TR/sparql11-protocol/#query-success
    SELECT and ASK: a SPARQL Results Document in XML, JSON, or CSV/TSV format.
    DESCRIBE and CONSTRUCT: an RDF graph serialized, for example,
    in the RDF/XML syntax, or an equivalent RDF graph serialization.
    """
    from SPARQLWrapper import SPARQLWrapper
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(result_format)
    results = sparql.query().convert()
    if result_format == 'json':
        # cleanse, extract triples from JSON response
        results = results.get('results').get('bindings')
        return results
    elif result_format == 'xml':
        return results.toxml()
    elif result_format == 'rdf+xml':
        return results.serialize(format='xml')
    elif result_format == 'n3':
        return results.serialize(format='n3')
    else:
        return print("Invalid result format")


def create_nodes(uri, typ, fields={}):
    """
    Parameters
    ----------
    uri : str
        Resource identifier for RDF subject or object, typically URL.
    typ : str
        Resource type as defined by the schema, ontology.
    fields : dict, default is None
        Additional data to enrich the node, like label, sameas, text, etc.

    Returns
    -------
    ID : str
        ArangoDB document _id(also called handle), which uniquely identifies
        the document across all collections within a DB.
    """
    try:
        if typ == 'http://schema.org/Person':
            # Get the API wrapper for a collection.
            collec = db.collection('Person')
            aq='FOR doc IN Person FILTER doc.URI=="'+str(uri)+'" OR doc.sameas=="'+str(uri)+'" RETURN doc._id'
        elif typ == 'http://schema.org/CreativeWork':
            collec = db.collection('Works')
            aq='FOR doc IN Works FILTER doc.URI=="'+str(uri)+'" OR doc.sameas=="'+str(uri)+'" RETURN doc._id'
        # Execute AQL query to match existing records in DB
        cursor = list(db.aql.execute(aq))
        # If URI not found in DB, create
        para = {'URI': uri, 'type': typ, 'sameas': ''}
        para.update(fields)
        if len(cursor) == 0:
            metadata = collec.insert(para)
            ID = metadata['_id']
            print(ID, "created")
        else:
            record = {'_id': cursor[0]}
            # update node with additional data
            collec.update_match(record, fields)
            ID = str(cursor[0])
            print(ID, "updated")

    except (DocumentInsertError):
        print('DocumentInsertError')
        ID = 'error'
        pass

    return ID

def create_works(uri, typ, fields={}):
    try:
        if typ == 'http://schema.org/CreativeWork':
            collec = db.collection('Works')
        ID = search_works(uri)
        para = {'URI': uri, 'type': typ, 'sameas': ''}
        para.update(fields)
        if ID == 0:
            metadata = collec.insert(para)
            ID = metadata['_id']
            print(ID, "created")
        else:
            return ID
    except (DocumentInsertError):
        print('DocumentInsertError')
        ID = 'error'
        pass
    return ID


def create_edges(from_id, to_id, triple):
    """
    Parameters
    ----------
    from_id : str
        Document _id of 'from' vertex.
    to_id : str
        Document _id of 'to' vertex.
    triple : list
        RDF triple stored as list in edge property.

    Returns
    -------
    from_id : str
        Document _id of 'from' vertex.
    to_id : str
        Document _id of 'to' vertex.
    e : dict
        server response from creation of edge, contains _key, _id, etc.
    """
    e = []
    if from_id != to_id:
        if triple[1] in ['http://schema.org/lyricist','http://purl.org/dc/terms/creator',
                         'https://schema.org/author']:
            # Get the API wrapper for a collection.
            edg = db.collection('Author')
            aq='FOR doc IN Author FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
        elif triple[1] == 'http://dbpedia.org/ontology/associatedMusicalArtist':
            edg = db.collection('Collaborator')
            aq='FOR doc IN Collaborator FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
        elif triple[1] == 'https://schema.org/citation':
            edg = db.collection('References')
            aq='FOR doc IN References FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'

        # Execute AQL query to match existing records in DB
        cursor = list(db.aql.execute(aq))
        # If _from and _to not found in DB, create new
        if len(cursor) == 0:
            e = edg.insert({'_from': from_id, '_to': to_id, 'RDF': triple})
            print(e['_id'], "edge created")
        # else update triple data
        else:
            e = edg.update_match({'_id': cursor[0]}, {'RDF': triple})
            print(e, "edge updated")

    return (from_id, to_id, e)

    
def ontology_mapper(triples, ontology_lookup):
    """
    Parameters
    ----------
    triples : list
        RDF triple from SPARQL endpoint.
    ontology_lookup : dict
        Ontology mapping logic can be dict, xls, csv or user input. Is used to
        lookup and translate from source ontology to custom defined ontology.

    Returns
    -------
    edges : list
        List of all edge definitions created.
    """
    edges = []
    for row in triples:
        # lookup predicate in ontology_lookup mapping sheet
        if (row['predicate']['value'] in ontology_lookup.keys()):
            # Create subject nodes after looking-up subject type
            ID_s = create_nodes(row['subject']['value'],
                                ontology_lookup[row['predicate']['value']][0])
            # Create object nodes after looking-up object type
            # If object type is literal, add property to existing node
            if ontology_lookup[row['predicate']['value']][2] == 'literal':
                ID_o = create_nodes(row['subject']['value'],
                    ontology_lookup[row['predicate']['value']][0],
                    {ontology_lookup[row['predicate']['value']][1],
                    row['object']['value'],row['predicate']['value']})
            # If object type is not literal, create new node
            else:
                ID_o = create_nodes(row['object']['value'],
                                ontology_lookup[row['predicate']['value']][2])
            triple = [row['subject']['value'], row['predicate']['value'],
                      row['object']['value']]
            # Create edge getting from_id and to_id from create_nodes function
            edges += create_edges(ID_s, ID_o, triple)
            print('------------------------------')
    print('Graph created.')
    print('============================================================')
    return edges


def namespace_sameas(uri, uri_dup):
    """
    Parameters
    ----------
    uri : str
        Resource identifier for RDF subject or object, typically URL.
    uri_dup : str
        Same resource using different namespace identifier, duplicate URI .

    Returns
    -------
    cursor : list
        List of updated node, 'sameas' field value.
    """
    for collec in ('Person', 'Works'):
        coll = db.collection(collec)
        aql='FOR doc IN '+str(collec)+' FILTER doc.URI=="'+str(uri)+'"RETURN doc._id'
        cursor = list(db.aql.execute(aql))
        if len(cursor) != 0:
            coll.update_match({'_id': cursor[0]}, {'sameas': uri_dup})
            print('updated sameas', cursor, uri, uri_dup)
    return cursor

def cleanse_triples(response):
    """
    Parameters
    ----------
    response : list of dicts
        JSON response from SPARQL query.
    Returns
    -------
    response : list of dicts
        substitute keys 's' for 'subject, 'p' for 'predicate' and 'o' for 'object'.
    """
    for triple in response:
        triple['subject'] = triple.pop('s')
        triple['predicate'] = triple.pop('p')
        triple['object'] = triple.pop('o')
    return response


def search_works(DOI, uri=None):
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
    DOI = str(DOI).upper()
    # search if DOI exists in memo
    if DOI in memo_DOI_ID:
        return memo_DOI_ID[DOI]
    # else query Arango DB
    else:
        try:
            collec = db.collection('Works')
            aq='FOR doc IN Works FILTER doc.DOI=="'+str(DOI)+'" OR doc.URI=="'+str(uri)+'" RETURN doc._id'
            # Execute AQL query to match existing records in DB
            ID = list(db.aql.execute(aq))
            if ID:
                memo_DOI_ID[DOI] = ID[0]
                return ID[0]
            else:
                print('Document', DOI, ' not found')
                memo_TBD_DOI[DOI] = 'NA'
                return 0
        except IndexError as e:
            print(e)
            return 0


# ontology mapping logic lookup file
ontology_lookup = {'predicate':
                       ['subject_type', 'predicate_alt', 'object_type'],
    'http://purl.org/dc/terms/creator':
        ['http://schema.org/CreativeWork', 'http://purl.org/dc/terms/creator',
         'http://schema.org/Person'],        
    'http://xmlns.com/foaf/0.1/name':
        ['http://schema.org/Person', 'label',
         'literal'],
    'http://purl.org/dc/terms/title':
        ['http://schema.org/CreativeWork', 'title',
         'literal'],       
    'https://schema.org/citation':
        ['http://schema.org/CreativeWork','https://schema.org/citation',
         'http://schema.org/CreativeWork'],
    'https://schema.org/author':
        ['http://schema.org/CreativeWork', 'https://schema.org/author',
         'http://schema.org/Person']
        }