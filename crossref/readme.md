# Crossref Project
This is a repository for the Crossref ETL pipeline, to load SODI-Graph using Crossref metadata, https://www.crossref.org/

The goal is to create a science knowledge graph, a database of scientific works, books, journals, datasets, and its authors, collaborators, publishers, institutions, funders. 
___
## Prerequisites
1. ArangoDB 3.7.2
    * Arango Server
    * Arango Shell
2. Python 3.8 or higher

## Installation, Initial Setup
1. Modify **config.py** with credentials, folder path, etc.
2. Execute **initialize_arango.py** to create an Arango database instance - Node collections, Edge collections and Graph

## Scripts
1. Execute **crossref_load.py** to create nodes - for scientific works, papers, journal articles, etc.
2. Execute **crossref_references.py** to create edges - for references and citations
3. Execute **crossref_authors.py** to create nodes - for authors and edges - for collaborators

## TBD
1. Separate modes to differentiate 
    * loading from .gz file
    * loading from Crossref API

