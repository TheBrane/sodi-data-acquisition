# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:34:14 2020

@author: Rishabh Rajiv
"""
# Initial setup: connecting to ArangoDB using python-arango driver
# https://www.arangodb.com/docs/stable/drivers/
# Creating a graph using YAGO - WordnetDomainHierarchy

from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://localhost:8529')

# Connect to "_system" database as root user.
sys_db = client.db('_system', username='root', password='')

# Create a new database named "SODI_test".
sys_db.create_database('SODI_test')

# Connect to "SODI_test" database as root user.
db = client.db('SODI_test', username='root', password='')

# Create a new collection named "WordnetDomain".
WordnetDomain = db.create_collection('WordnetDomain')

# Add a hash index to the collection.
WordnetDomain.add_hash_index(fields=['Domain'], unique=True)

# Insert new documents into the collection.
WordnetDomain.insert({'_key': '01','Domain': 'wordnetDomain_top', 'label': 'Top'})
WordnetDomain.insert({'_key': '02','Domain': 'wordnetDomain_doctrines', 'label': 'Doctrines'})
WordnetDomain.insert({'_key': '03','Domain': 'wordnetDomain_free_time', 'label': 'Free Time'})
WordnetDomain.insert({'_key': '04','Domain': 'wordnetDomain_applied_science', 'label': 'Applied Science'})
WordnetDomain.insert({'_key': '05','Domain': 'wordnetDomain_pure_science', 'label': 'Pure Science'})
WordnetDomain.insert({'_key': '06','Domain': 'wordnetDomain_social_science', 'label': 'Social Science'})
WordnetDomain.insert({'_key': '07','Domain': 'wordnetDomain_factotum', 'label': 'Factotum'})
WordnetDomain.insert({'_key': '08','Domain': 'wordnetDomain_mathematics', 'label': 'Mathematics'})
WordnetDomain.insert({'_key': '09','Domain': 'wordnetDomain_physics', 'label': 'Physics'})
WordnetDomain.insert({'_key': '10','Domain': 'wordnetDomain_computer_science', 'label': 'Computer Science'})
WordnetDomain.insert({'_key': '11','Domain': 'wordnetDomain_engineering', 'label': 'Engineering'})

# Execute an AQL query and iterate through the result cursor.
cursor = db.aql.execute('FOR doc IN WordnetDomain RETURN doc')
domain_names = [document['Domain'] for document in cursor]

# Create a new graph named "DomainHierarchy".
graph = db.create_graph('DomainHierarchy')

# Create vertex collections for the graph.
WordnetDomain = graph.create_vertex_collection('WordnetDomain')

# Create an edge definition (relation) for the graph.
narrower = graph.create_edge_definition(
    edge_collection='narrower',
    from_vertex_collections=['WordnetDomain'],
    to_vertex_collections=['WordnetDomain']
)

# Create edge label 'RDF' to save RDF triples TSV.
# Insert edge documents into "narrower" edge collection.
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/02', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_doctrines>'})
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/03', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_free_time>'})
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/04', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_applied_science>'})
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/05', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_pure_science>'})
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/06', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_social_science>'})
narrower.insert({'_from': 'WordnetDomain/01', '_to': 'WordnetDomain/07', 'RDF': '<wordnetDomain_top>	skos:narrower	<wordnetDomain_factotum>'})
narrower.insert({'_from': 'WordnetDomain/05', '_to': 'WordnetDomain/08', 'RDF': '<wordnetDomain_pure_science>	skos:narrower	<wordnetDomain_mathematics>'})
narrower.insert({'_from': 'WordnetDomain/05', '_to': 'WordnetDomain/09', 'RDF': '<wordnetDomain_pure_science>	skos:narrower	<wordnetDomain_physics>'})
narrower.insert({'_from': 'WordnetDomain/04', '_to': 'WordnetDomain/10', 'RDF': '<wordnetDomain_applied_science>	skos:narrower	<wordnetDomain_computer_science>'})
narrower.insert({'_from': 'WordnetDomain/04', '_to': 'WordnetDomain/11', 'RDF': '<wordnetDomain_applied_science>	skos:narrower	<wordnetDomain_engineering>'})

# Traverse the graph in outbound direction, breadth-first.
result = graph.traverse(
    start_vertex='WordnetDomain/01',
    direction='outbound',
    strategy='breadthfirst'
)
