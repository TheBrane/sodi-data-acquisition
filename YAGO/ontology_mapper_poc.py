# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 07:37:02 2020

@author: rish-r
"""

# Proof-of-concept for a general purpose ontology mapper
# Extract from YAGO and DBpedia and load into ArangoDB KG


# Query SPARQL databases, return formatted RDF triples 
def triples_generator(endpoint_url,sparql_query,result_format='json'):
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
        Note:From the SPARQL specification-https://www.w3.org/TR/sparql11-protocol/#query-success        
        SELECT and ASK: a SPARQL Results Document in XML, JSON, or CSV/TSV format.
        DESCRIBE and CONSTRUCT: an RDF graph serialized, for example, in the RDF/XML syntax, 
        or an equivalent RDF graph serialization.

    """
    from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDFXML, N3
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(result_format)
    results = sparql.query().convert()
    print(results)
    if result_format=='json':
        return results
    elif result_format=='xml':
        return results.toxml()
    elif result_format=='rdf+xml':
        return results.serialize(format='xml')
    elif result_format=='n3':
        return results.serialize(format='n3')
    else:
        return print("Invalid result format")

    
# Convert to standardized RDF vocabulary
#def vocab_mapper():

# Convert to custom ontology by lookup on file or table    
#def ontology_mapper():
    
# Create nodes in ArangoDB
#def create_nodes():    

# Create edges in ArangoDB
#def create_edges():

    