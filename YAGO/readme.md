# YAGO ETL Pipeline
This is a repository for the YAGO ETL pipeline and more generally any SPARQL endpoint.

The goal is to execute SPARQL queries, fetch RDF JSON and load into Arango DB Graph using Ontology mapper to transform to custom ontology 
___
## Prerequisites
1. ArangoDB 3.7.2
    * Arango Server
    * Arango Shell
2. Python 3.8 or higher
3. Python-Arango driver https://github.com/Joowani/python-arango 

## Initial Setup
1. Execute **arangodb_setup.py** to create an Arango database instance - Node collections, Edge collections and Graph

## Scripts
1. **ontology_mapper_poc.py** proof-of-concept to demonstrate ontology mapper, creates a graph of Tupac, songs he wrote and his associated acts.
2. **science_ontology_mapper.py** implements universal ontology mapper, pulls RDF JSON from multiple sources 
    * ma-graph.org
    * opencitations.net

