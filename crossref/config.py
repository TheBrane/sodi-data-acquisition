# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:08:56 2020

@author: rish-r
"""
from pathlib import Path
import json


db_name = 'SODI_TEST'
user = 'root'
password = 'Cro$$refkg'

crossref_url = 'https://api.crossref.org/works'
subject_type_work = 'http://schema.org/CreativeWork'
subject_type_author = 'http://schema.org/Person'
predicate_author = 'https://schema.org/author'
predicate_citation = 'https://schema.org/citation'
predicate_collaborator = 'https://schema.org/colleague'
json_folder = Path("D:/SODI/Proj/AlphaGO_graph")
nature_folder = Path("D:/CrossRef/fl")


# memoization of DOI and Arango ID, to avoid executing AQL search
memo_DOI_ID = json.load(open("memo_DOI_ID.json", 'r'))
# memoization of DOI and references DOI
memo_ref_DOI = json.load(open("memo_ref_DOI.json", 'r'))
# memoization of ID and reference IDs
memo_ref_ID = json.load(open("memo_ref_ID.json", 'r'))
# List of DOI not yet loaded, to be done, fetched and loaded
memo_TBD_DOI = json.load(open("memo_TBD_DOI.json", 'r'))
# memoization of Person names and ID 
memo_name_ID = json.load(open("memo_name_ID.json", 'r'))
