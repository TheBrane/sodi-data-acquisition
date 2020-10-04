# -*- coding: utf-8 -*-
"""
Created on Fri Oct 2 2020

@author: rish-r
"""
# Extract from ma-graph and OpenCitations, load into ArangoDB KG

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

    # Create a new graph named "Publications".
    graph = db.create_graph('Publications')

    # Create vertex collections for the graph.
    Person = graph.create_vertex_collection('Person')

    # Create vertex collections for the graph.
    Works = graph.create_vertex_collection('Works')

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


def intialize_client(db_name = 'SODI_TEST', user = 'root', password = 'xxxxxx'):
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


def create_nodes(uri, typ, data=['','']):
    """
    Parameters
    ----------
    uri : str
        Resource identifier for RDF subject or object, typically URL.
    typ : str
        Resource type as defined by the schema, ontology.
    data : list, default is None
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
            metadata = collec.insert({'URI': uri, 'type': typ, 'sameas': '', data[0]:data[1]})
            ID = metadata['_id']
            print(ID, "created")
        else:
            # update node with additional data
            collec.update_match({'_id': cursor[0]}, {data[0]:data[1]})
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
    e=[]
    if from_id != to_id:
        db = intialize_client()
        # Get the AQL API wrapper.
        aql = db.aql    
        if triple[1] in ['http://schema.org/lyricist','http://purl.org/dc/terms/creator']:
            # Get the API wrapper for a collection.
            edg = db.collection('Author')
            aq='FOR doc IN Author FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
        elif triple[1] == 'http://dbpedia.org/ontology/associatedMusicalArtist':
            edg = db.collection('Collaborator')
            aq='FOR doc IN Collaborator FILTER doc._from=="'+str(from_id)+'" AND doc._to=="'+str(to_id)+'" RETURN doc._id'
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
                    ontology_lookup[row['predicate']['value']][0],[ 
                    ontology_lookup[row['predicate']['value']][1],
                    row['object']['value'],row['predicate']['value']])
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
    
def main():
    intialize_database('SODI_TEST', 'root', 'xxxxxx')
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
         'literal']       }

    ma_url = 'http://ma-graph.org/sparql'
    ma_qry1 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX magp: <http://ma-graph.org/property/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX fabio: <http://purl.org/spar/fabio/>
            PREFIX org: <http://www.w3.org/ns/org#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            CONSTRUCT {?author foaf:name ?authorName}
            WHERE {
            ?field rdf:type <http://ma-graph.org/class/FieldOfStudy> .
            ?field foaf:name "Machine learning"^^xsd:string .
            ?paper fabio:hasDiscipline ?field .
            ?paper dcterms:creator ?author .
            ?author foaf:name ?authorName .
            }
            LIMIT 10"""
    ma_qry2 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX magp: <http://ma-graph.org/property/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX fabio: <http://purl.org/spar/fabio/>
            PREFIX org: <http://www.w3.org/ns/org#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            CONSTRUCT { ?paper dcterms:creator ?author}
            WHERE {
            ?field rdf:type <http://ma-graph.org/class/FieldOfStudy> .
            ?field foaf:name "Machine learning"^^xsd:string .
            ?paper fabio:hasDiscipline ?field .
            ?paper dcterms:creator ?author .
            ?author foaf:name ?authorName .
            ?paper dcterms:title ?title 
            }
            LIMIT 10"""
    ma_qry3 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX magp: <http://ma-graph.org/property/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX fabio: <http://purl.org/spar/fabio/>
            PREFIX org: <http://www.w3.org/ns/org#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            CONSTRUCT {?paper dcterms:title ?title}
            WHERE {
            ?field rdf:type <http://ma-graph.org/class/FieldOfStudy> .
            ?field foaf:name "Machine learning"^^xsd:string .
            ?paper fabio:hasDiscipline ?field .
            ?paper dcterms:creator ?author .
            ?author foaf:name ?authorName .
            ?paper dcterms:title ?title 
            }
            LIMIT 10"""
    ma_qry4 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX magp: <http://ma-graph.org/property/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX fabio: <http://purl.org/spar/fabio/>
            PREFIX org: <http://www.w3.org/ns/org#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX datacite: <http://purl.org/spar/datacite>
            
            CONSTRUCT {?paper dcterms:creator ?author}
            WHERE {
            ?paper dcterms:creator ?author .
            ?author foaf:name ?name .
            ?paper dcterms:title "MACHINE LEARNING AND CASE-BASED REASONING: THEIR POTENTIAL ROLE IN PREVENTING THE OUTBREAK OF WARS OR IN ENDING THEM"^^xsd:string .
            OPTIONAL{?paper datacite:doi ?doi} .
            }
            
            LIMIT 10"""
    oc_url = 'http://opencitations.net/sparql'
    oc_qry1 = """PREFIX cito: <http://purl.org/spar/cito/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX datacite: <http://purl.org/spar/datacite/>
            PREFIX literal: <http://www.essepuntato.it/2010/06/literalreification/>
            PREFIX biro: <http://purl.org/spar/biro/>
            PREFIX frbr: <http://purl.org/vocab/frbr/core#>
            PREFIX c4o: <http://purl.org/spar/c4o/>
            CONSTRUCT {
              ?cited dcterms:title ?title}
            WHERE {
            	<https://w3id.org/oc/corpus/br/1> cito:cites ?cited .
            	OPTIONAL { 
            		<https://w3id.org/oc/corpus/br/1> frbr:part ?ref .
            		?ref biro:references ?cited ;
            			c4o:hasContent ?cited_ref 
            	}
            	OPTIONAL { ?cited dcterms:title ?title }
            	OPTIONAL {
            		?cited datacite:hasIdentifier [
            			datacite:usesIdentifierScheme datacite:url ;
            			literal:hasLiteralValue ?url
            		]
            	}
            }LIMIT 10"""
            
    res1 = triples_generator(ma_url,ma_qry1) 
    # cleanse labels, 's' to 'subject'
    res1 = cleanse_triples(res1)    
    g1 = ontology_mapper(res1, ontology_lookup)
    
    res2 = triples_generator(ma_url,ma_qry2)
    res2 = cleanse_triples(res2)
    g2 = ontology_mapper(res2, ontology_lookup)    

    res3 = triples_generator(oc_url,oc_qry1)
    g3 = ontology_mapper(res3, ontology_lookup)
    
    res4 = triples_generator(ma_url,ma_qry3)
    res4 = cleanse_triples(res4)
    g4 = ontology_mapper(res4, ontology_lookup)
    
        
    res5 = triples_generator(ma_url,ma_qry4)
    res5 = cleanse_triples(res5)
    g5 = ontology_mapper(res5, ontology_lookup)


if __name__ == "__main__":
    main()
