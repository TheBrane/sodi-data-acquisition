import requests     # how python goes onto the internet!
import re           # regex
from bs4 import BeautifulSoup # a python HTML parser (version 3)
import pandas as pd


from sklearn.feature_extraction.text import  TfidfVectorizer




from time import sleep




class compound ():
    def __init__(self, id_or_formula):
        self.flag_iupac = 0
        self.flag_smiles = 0
        self.flag_inchi = 0
        self.id = self.get_id(id_or_formula)
        self.json = self.get_json(self.id)
        self.url = 'https://pubchem.ncbi.nlm.nih.gov/compound/' + str(self.id) 
        self.text = []
        
        self.properties_dic = {}
        
        if self.id != 0 and self.json !=0:
            self.References = {} 
            for i in self.json['Record']['Reference']:
                self.References[i['ReferenceNumber']] = i['SourceName'] 
                self.get_keys(self.json, [])     
                self.components = self.decompose(self.formula)
            titles = [self.formula]
            titles= []
            if self.flag_iupac == 1 :
                titles.append(self.Iupac)
            if self.flag_smiles == 1:
                titles.append(self.SMILES)
            if self.flag_inchi == 1:
                titles.append(self.InCHI)
            
            self.titles = ', '.join(titles)
            self.create_db_entry()
            #self.inovators = self.get_innovators(self.id)
            
    def create_db_entry(self):
        self.entry = {
            'ID': 'pubchem' + str(self.id).zfill(9),
            'Family': 'Technology',
            'Group': 'Body',
            'Type': 'Molecule',
            'Entity': 'Entity',
            'Formula': self.formula
            }
        
        titles = self.titles.split(', ')
        for i in range(len(titles)):
            self.entry['Title' + str(i+1)] = titles[i]
        self.entry['Title'] = self.name.capitalize()
        if hasattr(self, 'description'):
            self.entry['Description'] = self.description
            self.entry['Description_ref'] = self.References[self.description_ref]                  
        #self.entry = dict(self.entry.items() + self.properties_dic.items())
            
    def get_json(self, comp_id):
        id = str(comp_id).zfill(9)
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/'+ id + '/JSON/?response_type=display'
        r = requests.get(url,verify=False).json()
        try:
            return r
        except:
            return 0
        
    def get_id (self, id_or_formula):
        url = 'https://pubchem.ncbi.nlm.nih.gov/compound/' + str(id_or_formula)
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.text,'html.parser')
        meta = soup.findAll("meta", { "name" : "pubchem_uid_value" })
        try:
            return str(meta[0].get('content')).zfill(9)
        except:
            return 0   
        
    def decompose (self, formula):
        sub = re.findall('[A-Z][^A-Z]*', formula)
        l=[]
        for i in range(len(sub)):
            for j in range(len(sub)):
                if len(sub[i:j+1]) > 0 and j>i:
                    l.append(sub[i:j+1])
                    if len(sub[i:j+1]) == 1:
                        #get the element withou number(eg. H2 becomes H)
                        l.append(''.join([k for k in sub[i:j+1][0] if not k.isdigit()]))
        
        result = list(set([''.join(i) for i in l] ))
        return [r for r in result if r != formula]
    
    def get_innovators(self, comp_id):
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/categories/compound/' + comp_id +'/JSON/?response_type=display'
        r = requests.get(url,verify=False).json()
        return r['SourceCategories']['Categories']
    
    def get_related(self, related):
        related_compounds = {}
        id_list = []
        k=0
        for i in related:
            if (k+1)%10 != 0:
                r = requests.get(i['URL'], verify=False)
                soup = BeautifulSoup(r.text,'html.parser')
                dl = soup.findAll("dl", {'class': 'rprtid'})
                for tag in dl:
                    id_list.append(tag.findAll('dd')[0].text)
                related_compounds[i['Name']] = id_list 
            else:
                pass
            k += 1
        return related_compounds
        
    def get_keys(self, d_or_l, keys_list):
        if isinstance(d_or_l, dict):
            for k, v in iter(sorted(d_or_l.iteritems())):
                if isinstance(v, list):
                    self.get_keys(v, keys_list)
                elif isinstance(v, dict):
                    self.get_keys(v, keys_list)
                keys_list.append(k)   
                
                if k == 'StringValue':
                    if 'ReferenceNumber' in d_or_l.keys():
                        self.text.append((d_or_l[k], d_or_l['ReferenceNumber']))
                if k == 'TOCHeading':
                    if v == 'Molecular Formula':
                        formula = d_or_l['Information'][0]['StringValue']
                        self.formula = formula
                    if v =='Record Title':
                        name = d_or_l['Information'][0]['StringValue']
                        if not ' ' in name:
                            self.name = name[0].upper() + name[1:]
                        else:
                            self.name = name[0].upper() + name[1:].lower()

                    if v == 'Record Description':
                        self.description = d_or_l['Information'][0]['StringValue']
                        self.description_ref = d_or_l['Information'][0]['ReferenceNumber']
                    if v == 'Related Compounds':
                        related = d_or_l['Information']
                        self.related_reference = d_or_l['Information'][0]['ReferenceNumber']
                        self.related = related
                       

                    if v == 'IUPAC Name':
                        self.flag_iupac = 1
                        self.Iupac = d_or_l['Information'][0]['StringValue']
                    if v == 'InChI':
                        self.flag_inchi = 1
                        self.InCHI = d_or_l['Information'][0]['StringValue']
                    if v == 'Canonical SMILES':
                        self.flag_smiles = 1
                        self.SMILES = d_or_l['Information'][0]['StringValue']  

              

#                    if v == 'Computed Properties':
#                        reference_number = d_or_l['Information'][0]['ReferenceNumber']
#                        self.computed_proprerties = d_or_l['Information'][0]['Table']['Row']
#                        for i in self.computed_proprerties:
#                            try:
#                                ref =  self.References[reference_number]
#                            except:
#                                ref = 'PubChem'
#                                
#                            self.properties_dic[i['Cell'][0]['StringValue']+'_ref'] = ref
#                            self.properties_dic[i['Cell'][0]['StringValue']] = ' '.join([str(i['Cell'][1][k]) for k in i['Cell'][1].keys()])
#                    if v == 'Experimental Properties':
#                        self.exp_prop = d_or_l['Section']
#                        for i in self.exp_prop:
#                            try:
#                                    ref =  self.References[i['Information'][0]['ReferenceNumber']]
#                            except:
#                                    ref = 'PubChem'
#                                    
#                            if 'StringValue' in i['Information'][0].keys():
#                                
#                                self.properties_dic[i['Information'][0]['Name']+'_ref'] = ref
#                                self.properties_dic[i['Information'][0]['Name']] = i['Information'][0]['StringValue']
#                            elif 'NumValue' in i['Information'][0].keys() and 'ValueUnit' in i['Information'][0].keys():
#                                try:
#                                    self.properties_dic[i['Information'][0]['Name']+'_ref'] = i['Information'][0]['Reference'][0]
#                                except:
#                                    self.properties_dic[i['Information'][0]['Name']+'_ref'] = 'PubChem'
#                                    
#                                self.properties_dic[i['Information'][0]['Name']] = str(i['Information'][0]['NumValue']) + ' ' + i['Information'][0]['ValueUnit']
#                            elif  'NumValue' in i['Information'][0].keys() and 'ValueUnit' not in i['Information'][0].keys():
#                                try:
#                                    self.properties_dic[i['Information'][0]['Name']+'_ref'] = i['Information'][0]['Reference'][0]
#                                except:
#                                    self.properties_dic[i['Information'][0]['Name']+'_ref'] = 'PubChem'
#                                self.properties_dic[i['Information'][0]['Name']] = str(i['Information'][0]['NumValue'])
#                            else:
#                                pass
                   
        elif isinstance(d_or_l, list):
            for i in d_or_l:
                if isinstance(i, list):
                    self.get_keys(i, keys_list)
                elif isinstance(i, dict):
                    self.get_keys(i, keys_list)

        else:
            print "** Skipping item of type: {}".format(type(d_or_l))
    
        return keys_list

def create_entry(db_id, title, title2, family, entity, prop, group = 'Body', typ = 'Molecule'):
    dic = {
        'ID': str(db_id).zfill(9),
        'Title': title,
        'Title2': '',
        'Family': family,
        'Group': group,
        'Type': typ,
        'Entity': entity,
        'Property': prop
        }
    
    titles = title2.split(', ')
    for i in range(len(titles)):
        dic['Title' + str(i+2)] = titles[i]
    
    #dataset = pd.DataFrame(dic)
    return dic#dataset[['ID', 'Title', 'Title2 (fuzzy)','Family','Group','Type','Entity','Property']]

def create_link(rel_id, parent_id, child_id, link, reference):
    dic = {
        'REL ID': str(rel_id).zfill(9),
        'PARENT ID': str(parent_id).zfill(9),
        'CHILD ID': str(child_id).zfill(9),
        'LINK': link,
        'REFERENCE': str(reference)
        }
   # dataset = pd.DataFrame(dic)
    return dic#dataset[['REL ID', 'PARENT ID', 'CHILD ID', 'LINK']]



def create_db(entry, index, db = pd.DataFrame()):
    db = db.append(entry, ignore_index=True)
    db.to_csv('db.csv', sep=';', index = False, encoding='utf-8')
    return db



        

def create_inovators(comp, links = pd.DataFrame(), db = pd.DataFrame()):  
        ids = comp.id
        inov = comp.get_innovators(ids)
        
        try:
            rel_id = int(links['REL ID'].max())+1
        except:
            rel_id = 1
            
        for i in inov:
            if i['Category'] == 'Chemical Vendors':
                group = 'Enterprise'
                typ = 'Company'
                entity = ''
            elif i['Category'] == 'Governmental Organization':
                group = 'Public institution'
                typ = 'Government agency'
                entity = ''
            elif i['Category'] == 'Journal Publisher':
                entity = 'Journal Publisher'
                group = 'Enterprise'
                typ = 'Company'
            elif i['Category'] == 'Research and Development':
                group = 'Enterprise'
                typ = 'Research Center'
                entity = ''
            else:
                pass
            
            for s in i['Sources']:
                try:
                    link = create_link(rel_id,'pubchem' + ids, 'pubchem' +  s['SourceName'], 'Is a molecule of', s['SourceURL'])
                except:
                    link = create_link(rel_id,'pubchem' + ids, 'pubchem' +  s['SourceName'], 'Is a molecule of',  'PubChem')
                links = links.append(link, ignore_index=True)
                rel_id +=1
                
                if 'pubchem' + s['SourceName'] not in db.ID.values:
                    entry = {'ID': 'pubchem' + s['SourceName'],
                                 'Title': s['SourceName'],
                                 'Group': group,
                                 'Type': typ,
                                 'Entity': entity
                                
                                }
                    db = create_db(entry, 'pubchem' + s['SourceName'], db)
                 
                links.to_csv('links.csv', sep=';',index = False)

 
            
        return db, links
    
def create_related(comp, links = pd.DataFrame(), db = pd.DataFrame()):
        related = comp.get_related(comp.related)
        ids = comp.id
        try:
            rel_id = int(links['REL ID'].max())+1
        except:
            rel_id = 1
    
        try:
            reference = comp.References['comp.related_reference']
        except:
            reference = 'PubChem'
    
        for key in related.keys():
            for child_id in related[key][5:20]:
                child = compound(child_id)
                entry = child.entry
                
                if not 'Cid' in child.name and not set('[~!@#$%^&*()_+{}"\']+$').intersection(child.name):
                    link = create_link(rel_id,'pubchem' + ids, 'pubchem' + child_id, 'Has the ' + key + ' as' , reference)
                    links = links.append(link, ignore_index=True)
                    rel_id += 1
                    db = create_db(entry, 'pubchem' + child_id, db)
                    links.to_csv('links.csv', sep=';',index = False)
        return db, links
                  
def create_components(comp, links = pd.DataFrame(), db = pd.DataFrame()):  
        components = comp.components
        ids = comp.id
        
        try:
            rel_id = int(links['REL ID'].max())+1
        except:
            rel_id = 1
            
        for c in components:
            if c != comp.formula:
                child_comp = compound(c)
                if child_comp.id != 0:
                    if not child_comp.json == ['Fault']:
                        if not 'Cid' in child_comp.name and not set('[~!@#$%^&*()_+{}"\']+$').intersection(child_comp.name):
                            link = create_link(rel_id, 'pubchem' + ids, 'pubchem' + child_comp.id, 'Is a molecule of', 'PubChem')
                            links = links.append(link, ignore_index=True)
                            rel_id += 1
                         
                            sleep(0.5)
                            entry = child_comp.entry
                            if 'pubchem' + child_comp.id not in db.ID.values:
                                db =    create_db(entry, 'pubchem' + child_comp.id, db)
                            links.to_csv('links.csv', sep=';',index = False)
        return db, links
    
def create_matches(comp, links = pd.DataFrame(), db = pd.DataFrame()):
        text = [i[0] for i in comp.text]
        ids = comp.id
        
        try:
            rel_id = int(links['REL ID'].max())+1
        except:
            rel_id = 1
            
        matches = match_titles(text, db)
        comp_index = 0
        for m in matches:
            for i in m:
                link = create_link(rel_id, ids, db.ID[db.Title.apply(lambda x: x.lower()) == i].index.tolist()[0] ,'Is a molecule of', 'PubChem')
                links = links.append(link, ignore_index=True)
                links.to_csv('links.csv', sep=';',index = False)
                rel_id += 1
            comp_index += 1
#   
        return db, links




def match_titles(text, db):
    titles = db[(db.Tag == 'Discipline') | (db.Tag == 'Biological phenomenon') | (db.Type == 'Body')].Title
    vect = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    matrix = pd.DataFrame(vect.fit_transform(text).toarray(), columns = vect.get_feature_names())
    
    cols = matrix.columns
    bt = matrix.apply(lambda x: x > 0)
    bt = bt.apply(lambda x: list(cols[x.values]), axis=1)
    titles = pd.Series(titles).apply(lambda x: x.lower())
    
    
    matches = bt.apply(lambda x: list(set(x).intersection(set(titles))))
    
    return matches
    
    


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def GetReference(keyword, l):
    try:
        reference = [x[1] for x in l if keyword in x[0]][0]
    except:
        reference = 'N/A'
    return reference

db = pd.read_csv('db.csv', sep = ';')
links = pd.read_csv('links.csv', sep = ';')

with open('todo.txt') as f:
    id_list = [line.strip() for line in f.read().splitlines()]

with open('done.txt') as f:
    done = [line.strip() for line in f.read().splitlines()]
    
import time
start = time.time()

for i in id_list:
    if i not in done:
        try:
            comp = compound(i)
            if str('pubchem' + comp.id) not in db.ID.values:
                db = create_db(comp.entry, comp.id, db)
            db, links = create_components(comp, links, db)
            db, links = create_inovators(comp, links, db)
            db, links = create_related(comp, links, db)
           # db, links = create_matches(comp, links, db) 
            with open("done.txt", "a") as myfile:
                myfile.write('\n' + str(i) )
        except:
            pass

end = time.time()
elapsed = end - start

db = db.drop_duplicates()
links = links.drop_duplicates(subset =  ['CHILD ID','LINK','PARENT ID'])


### Adjusts scrape to be imported into DB 
for i in ['ID', 'Title', 'Formula']:
    temp = db[db.Group != 'Enterprise'].drop_duplicates(subset =  [i])

db= pd.merge(temp, db[db.Group == 'Enterprise'], how='outer')
    
    
def inov(title):
    KeywordsToCheck = ['university', 'database', 'consortium', 'repository', 'nih']
    if any(kwd in title for kwd in KeywordsToCheck):
        return 'Public institutions'
    else:
        return 'Enterprises'
  

    
temp = db[db.Group == 'Enterprise']
temp['Family'] = 'Innovator'
temp.Group = temp.Title.apply(lambda x: inov(x.lower()))
db= pd.merge(temp, db[db.Group != 'Enterprise'], how='outer')

db['IsCluster'] = pd.Series([False]*db.shape[0])

def link_title(group_child):
    if group_child == 'Enterprises':
        return ('manufactures', 'is manufactured by')
    elif group_child == 'Public institutions':
        return ('researches', 'is researched by')
    elif group_child == 'Body':
        return ('is related to', 'is related to')
    else: 
        return (0,0)


id_dic = {}
ids = 0
for i in db.ID:
    id_dic[i] = int(ids)
    ids += 1

def convert_id(ids, dic):
    try:
        return int(dic[ids])
    except:
        return float('NaN')

db['ID']  = db.ID.apply(lambda x: convert_id(x,id_dic))
links['PARENT ID'] = links['PARENT ID'].apply(lambda x: convert_id(x,id_dic))
links['CHILD ID'] = links['CHILD ID'].apply(lambda x: convert_id(x,id_dic))
links.dropna(inplace = True)
links['Title_active'] = links['CHILD ID'].apply(lambda x: link_title(db.Group[x])[0])
links['Title_passive'] = links['CHILD ID'].apply(lambda x: link_title(db.Group[x])[1])

links['CHILD ID'] = (links['CHILD ID'] + 1).astype(int)
links['PARENT ID'] = (links['PARENT ID']+1).astype(int)
db.ID = db.ID + 1

def Adjust_body(group):
    if group == 'Body':
        return 'Manufactured chemicals'
    else:
        return group

db.Group = db.Group.apply(lambda x: Adjust_body(x))
db = db[['ID','Title','Family','Group','Type','IsCluster']]
links = links[['PARENT ID', 'CHILD ID', 'Title_active','Title_passive']]

db.to_csv('export_db.csv', sep=';', index = False)
links.to_csv('export_links.csv', sep=';', index = False, header = False)


