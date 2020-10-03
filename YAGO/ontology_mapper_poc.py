# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 07:37:02 2020

@author: rish-r
"""

# Proof-of-concept for a general purpose ontology mapper
# Extract from YAGO and DBpedia and load into ArangoDB KG

from arango import ArangoClient, ArangoServerError, DocumentInsertError


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
    # sys_db.create_database(db_name)

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

    # Create a new graph named "Music".
    graph = db.create_graph('Music')

    # Create vertex collections for the graph.
    Person = graph.create_vertex_collection('Person')

    # Create vertex collections for the graph.
    Works = graph.create_vertex_collection('Works')

    # Create an edge definition for works to person.
    creator = graph.create_edge_definition(
        edge_collection='creator',
        from_vertex_collections=['Works'],
        to_vertex_collections=['Person']
    )

    # Create an edge definition relation between persons.
    relation = graph.create_edge_definition(
        edge_collection='relation',
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
    return client.db('SODI_DEV', 'root', 'Cro$$refkg')


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


def create_nodes(uri, typ, data=None):
    """
    Parameters
    ----------
    uri : str
        Resource identifier for RDF subject or object, typically URL.
    typ : str
        Resource type as defined by the schema, ontology.
    data : dict, default is None
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
        if len(cursor) == 0:
            metadata = collec.insert({'URI': uri, 'type': typ, 'sameas': ''})
            ID = metadata['_id']
            print(ID, "created")
        else:
            # update node with additional data
            collec.update_match({'_id': cursor[0]}, {'data': data})
            ID = str(cursor[0])
            print(ID, "updated")

    except (DocumentInsertError):
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
    db = intialize_client()
    # Get the AQL API wrapper.
    aql = db.aql    
    if triple[1] == 'http://schema.org/lyricist':
        # Get the API wrapper for a collection.
        edg = db.collection('creator')
        aq='FOR doc IN creator FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
    elif triple[1] == 'http://dbpedia.org/ontology/associatedMusicalArtist':
        edg = db.collection('relation')
        aq='FOR doc IN relation FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
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


def main():
    intialize_database('SODI_DEV', 'root', 'xxxxxx')
    # define ontology lookup mapping sheet
    ontology_lookup = {'predicate':
                       ['subject_type', 'predicate_alt', 'object_type'],
    'http://schema.org/lyricist':
        ['http://schema.org/CreativeWork', 'http://schema.org/lyricist',
         'http://schema.org/Person'],
    'http://dbpedia.org/ontology/associatedMusicalArtist':
        ['http://schema.org/Person',
         'http://dbpedia.org/ontology/associatedMusicalArtist',
         'http://schema.org/Person']}

    yago_url = 'https://yago-knowledge.org/sparql/query'
    dbp_url = 'http://dbpedia.org/sparql'

    # Construct a graph of Tupac Shakur songs (lyricist of) from YAGO
    yago_qry = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <http://schema.org/>
    CONSTRUCT { ?songs schema:lyricist  ?person. }
      WHERE {
      ?person rdfs:label "Tupac Shakur"@en .
      ?songs schema:lyricist  ?person.
    }
    LIMIT 5"""

    result1 = triples_generator(yago_url, yago_qry)

    # Call ontology mapper to create nodes and edges
    edges = ontology_mapper(result1, ontology_lookup)
    print(edges)
    print()

    # Construct a graph of MC Hammer songs (lyricist of) from YAGO
    yago_qry2 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <http://schema.org/>
    CONSTRUCT { ?songs schema:lyricist  ?person. }
          WHERE {
          ?person rdfs:label "MC Hammer"@en .
          ?songs schema:lyricist  ?person.
        }
    LIMIT 5"""

    result3 = triples_generator(yago_url, yago_qry2)
    edges3 = ontology_mapper(result3, ontology_lookup)
    print(edges3)
    print()

    # Construct a graph of Tupac Shakur and associated artists from DBpedia
    dbp_qry = """CONSTRUCT {?value
    <http://dbpedia.org/ontology/associatedMusicalArtist> ?resource}
    WHERE {
    ?value rdfs:label "Tupac Shakur"@en .
    ?resource <http://dbpedia.org/ontology/associatedMusicalArtist> ?value }
    LIMIT 10"""

    namespace_sameas('http://yago-knowledge.org/resource/Tupac_Shakur',
                     'http://dbpedia.org/resource/Tupac_Shakur')
    namespace_sameas('http://yago-knowledge.org/resource/MC_Hammer',
                     'http://dbpedia.org/resource/MC_Hammer')
    result2 = triples_generator(dbp_url, dbp_qry)
    # cleanse labels, 's' to 'subject'
    for triple in result2:
        triple['subject'] = triple.pop('s')
        triple['predicate'] = triple.pop('p')
        triple['object'] = triple.pop('o')

    edges2 = ontology_mapper(result2, ontology_lookup)
    print(edges2)
    print()

if __name__ == "__main__":
    main()
