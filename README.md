# sodi-data-acquisition

*1. Select DB*
- 1.1.   Pick a structured or unstructured Open Access DB (Data usable for any purpose)
  - 1.2    Validate with team
    
*2.Select target data*
- 2.1. Select data and supporting citation data to be scraped
    
*3. Identify Ontology tags applicable to target data for classification*
- 3.1. Define mapping of target DB ontology onto SODI's ontology - see KCS mapping examples in [SODI ontology doc](https://docs.google.com/spreadsheets/d/1DkbxDBdbYkVYgzq5rciWsLBGdYJnBjKu284Wf8BeTc0/edit#gid=570911882)
   - 3.1.1 Define rules - [see KCS-mapping examples](https://docs.google.com/spreadsheets/d/1DkbxDBdbYkVYgzq5rciWsLBGdYJnBjKu284Wf8BeTc0/edit#gid=1531718387)
    
- 3.2. If no tags in [SODI ontology doc](https://docs.google.com/spreadsheets/d/1DkbxDBdbYkVYgzq5rciWsLBGdYJnBjKu284Wf8BeTc0/edit#gid=570911882) are applicable, use tags of your choosing
    - 3.2.1 Properly define and reference the new tag(s) you use in the [SODI ontology doc](https://docs.google.com/spreadsheets/d/1DkbxDBdbYkVYgzq5rciWsLBGdYJnBjKu284Wf8BeTc0/edit#gid=570911882)
      
 - 3.3 Scrape sample set of data (Max 1000 terms and/or relationships, whichever comes first) and upload for review
     - 3.3.1 if sample false positive (FP) rate > 1%, adjust and return to 3.3
     - 3.3.2 if sample false positive (FP) rate < 1%, upload JSON to the project Database
       
Rinse and repeat
