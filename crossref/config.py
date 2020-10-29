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
predicate_author = 'https://schema.org/author'
predicate_citation = 'https://schema.org/citation'
json_folder = Path("D:\SODI\Proj\AlphaGO_graph")

# =============================================================================
# memo_DOI_ID = {}
# memo_ref_DOI = {}
# memo_ref_ID = {}
# memo_TBD_DOI = {}
# json.dump(memo_DOI_ID, open("memo_DOI_ID.json", 'w'))
# json.dump(memo_ref_DOI, open("memo_ref_DOI.json", 'w'))
# json.dump(memo_ref_ID, open("memo_ref_ID.json", 'w'))
# json.dump(memo_TBD_DOI, open("memo_TBD_DOI.json", 'w'))
# =============================================================================

# memoization of DOI and Arango ID, to avoid executing AQL search
memo_DOI_ID = json.load(open("memo_DOI_ID.json", 'r'))
# memoization of DOI and references DOI
memo_ref_DOI = json.load(open("memo_ref_DOI.json", 'r'))
# memoization of ID and reference IDs
memo_ref_ID = json.load(open("memo_ref_ID.json", 'r'))
# List of DOI not yet loaded, to be done, fetched and loaded
memo_TBD_DOI = json.load(open("memo_TBD_DOI.json", 'r'))

