# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 2020

@author: rish-r
"""
# Extract from ma-graph and OpenCitations, load into ArangoDB KG

from arango import ArangoClient, ArangoServerError, DocumentInsertError
import json
from pathlib import Path


json_folder = Path("D:\SODI\Proj\AlphaGO_graph")
db_name = 'SODI_TEST'
user = 'root'
password = 'xxxxxx'


def intialize_database(db_name, user, password):
    """
    Parameters
    ----------
    db_name : str
        Name of the ArangoDB instance.
    user : str
        Username.
    password : str
        Password.

    Returns
    -------
    None.
    """

    # Initialize the client for ArangoDB.
    client = ArangoClient(hosts='http://localhost:8529')

    # Connect to "_system" database as root user.
    sys_db = client.db('_system', username=user, password=password)

    # Create a new database named "test".
    #sys_db.create_database(db_name)

    # Connect to "test" database as root user.
    db = client.db(db_name, username=user, password=password)

    # Create a new collection named "Person".
    Person = db.create_collection('Person')

    # Create a new collection named "Works".
    Works = db.create_collection('Works')
    
    # Add a hash index to the collection.
    Person.add_hash_index(fields=['URI'], unique=True)

    # Add a hash index to the collection.
    Works.add_hash_index(fields=['URI'], unique=True)

    # Add a hash index to the collection.
    Works.add_hash_index(fields=['DOI'], unique=True)

    # Create a new graph named "Publications".
    graph = db.create_graph('Publications')

    # Create vertex collections for the graph.
    Person = graph.create_vertex_collection('Person')

    # Create vertex collections for the graph.
    Works = graph.create_vertex_collection('Works')
    
    # Create an edge definition for works to works.
    References = graph.create_edge_definition(
        edge_collection='References',
        from_vertex_collections=['Works'],
        to_vertex_collections=['Works']
    )

    # Create an edge definition for works to person.
    Author = graph.create_edge_definition(
        edge_collection='Author',
        from_vertex_collections=['Works'],
        to_vertex_collections=['Person']
    )

    # Create an edge definition relation between persons.
    Collaborator = graph.create_edge_definition(
        edge_collection='Collaborator',
        from_vertex_collections=['Person'],
        to_vertex_collections=['Person']
    )


def intialize_client():
    """
    Returns
    -------
    database object
        db object for python-arango driver functions.
    """
    # Initialize the client for ArangoDB.
    client = ArangoClient(hosts='http://localhost:8529')
    # Connect to "test" database as root user.
    return client.db(db_name, user, password)


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


# Convert to standardized RDF vocabulary
# def vocab_mapper():


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
        # Initialize the client for ArangoDB.
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql
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
            #print('para', para)
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
        ID='error'
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
    e=[]
    if from_id != to_id:
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql    
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
        #else update triple data
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
    # Initialize the client for ArangoDB.
    db = intialize_client()
    # Get the AQL API wrapper.
    aql = db.aql
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
    TYPE
        DESCRIPTION.

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
    
def main():
    #intialize_database(db_name, user, password)
    # define ontology lookup mapping logic
    ontology_lookup = {'predicate':
                       ['subject_type', 'predicate_alt', 'object_type'],
    'http://schema.org/lyricist':
        ['http://schema.org/CreativeWork', 'http://schema.org/lyricist',
         'http://schema.org/Person'],
    'http://purl.org/dc/terms/creator':
        ['http://schema.org/CreativeWork', 'http://purl.org/dc/terms/creator',
         'http://schema.org/Person'],        
    'http://dbpedia.org/ontology/associatedMusicalArtist':
        ['http://schema.org/Person',
         'http://dbpedia.org/ontology/associatedMusicalArtist',
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
    predicate_citation = 'https://schema.org/citation'
    predicate_author = 'https://schema.org/author'
    for files in json_folder.iterdir(): 

        with open(files) as f:
             data = json.load(f)
        #DOI is case insensitive, default to UPPER
        DOI = data.get('message').get('DOI').upper()
        URL = data.get('message').get('URL')
        title = str(data.get('message').get('title'))[1:-1]
        subject = data.get('message').get('subject')
        work_type = data.get('message').get('type')
        #additional data passed as fields dict
        fields = {'DOI':DOI,'title':title, 'subject':subject, 
                  'work_type':work_type, 'data':data.get('message')}
        create_nodes(URL, 'http://schema.org/CreativeWork',fields)
    #try:
# =============================================================================
#     file_num = 1    
#     for files in json_folder.iterdir():         
#         with open(files) as f:
#              data = json.load(f)
#         
#         from_DOI = data.get('message').get('DOI')
#         from_id = search_work(from_DOI)
#         if from_id !=0:
#             references = data.get('message').get('reference')
#             if references is not None:
#                 ref_num = 1
#                 for ref in references:                   
#                     to_DOI = ref.get('DOI',0)
#                     to_id = search_work(to_DOI)
#                     print(from_id, '--->', to_id, 'ref#',ref_num)
#                     if to_id !=0:
#                         trip = [from_DOI, predicate_citation, to_DOI]
#                         print('File #',file_num, trip)
#                         e = create_edges(from_id, to_id, trip)
#                         print(e)
#                     ref_num += 1
#             else:
#                 print('No references. File #',file_num)
#         print('File name:',files,'#',file_num, '============================================')
#         file_num += 1
# =============================================================================
# =============================================================================
#     except (TypeError, AttributeError):
#         print('None found')
#         pass
#         
# =============================================================================
    
# =============================================================================
#         URL = data.get('message').get('URL')
#         title = str(data.get('message').get('title'))[1:-1]
#
#         
#         #print(URL, title) 
#         fields = {'DOI':DOI,'title':title,'data':data.get('message')}
#         create_nodes(URL, 'http://schema.org/CreativeWork',fields)
#         
# =============================================================================
        
if __name__ == "__main__":
    main()
