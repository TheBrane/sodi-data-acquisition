# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

def find_bigrams(input_list):
    ngram = []
    for i in range(len(input_list)-1):
        if input_list[i] == input_list[i+1]:
            continue
        ngram.append((input_list[i],input_list[i+1], 'hierarchical'))
    return ngram

def get_links(id, title):
    url = 'http://www.eol.org/pages/' + id
    r = requests.get(url)
    response = BeautifulSoup(r.text, "lxml")
    branches = response.findAll("ul", { "class" : "branch" })
    links = []
    for i in branches:
        if i.find("a"):
            links.append(i.find("a").contents[0])

    hierarchyLinks = [l for l in links if isinstance(l, str)]
    finalLinks = []
    finalLinks = finalLinks + find_bigrams(hierarchyLinks[:-1] + [title])
    #print(links)
    return finalLinks

def get_traits(id):
    url = 'http://www.eol.org/pages/' + id
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    traits = {}
    trait_box = soup.find("table", { "class" : "standard data" })
    if trait_box:
        for entry in trait_box.find_all('tr'):
            contents = tuple(entry.stripped_strings)
            if len(contents) > 1:
                traits[contents[0]] = [content for content in contents[1:] if content != 'more']
    return traits

def get_node_data(id):
    url = "https://eol.org/pages/%s/details" %id
    r  = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.title.text.split(' - ')[-3]
    description_data = soup.find("div", { "class" : "copy" }).get_text()
    node = {'eol_id': id, 'title': title}
    node['links'] = get_links(str(id), title)
    node['description'] = description_data
    node['traits'] = get_traits(str(id))
    return node

### Generator driven approach to iterate over every page/taxon
def scrape_eol(start=1, entries=100):
    index = {}
    for taxon in range(start, start+entries):
        node = get_node_data(taxon)
        index[node['title']] = node
        if taxon % 5 == 0:
            print('%s pages scraped.' %taxon)
    return index

### Generating CSV from nodes
def generate_csv(index):
    counter = 0
    with open('import_sample_%s.csv' % len(index), 'w') as f:
        # First write data to create nodes with description for each taxon
        for key in index:
            f.write('CN;%s;%s;description;%s\n' %(counter, key, index[key]['description'].strip()))
            counter += 1
            index[key]['node_id'] = counter

        # With nodes created, next write edges linkking each node to parent and vice versa
        for key in index:
            links = [l for l in index[key]['links'] if l[0] in index and l[1] in index]
            for link in links:
                f.write('CL;%s;%s;is contained with;contains\n' %(index[link[0]]['node_id'], index[link[1]]['node_id']))

        # Updating trait info to node; if lateral dependencies exist, creating links
        for key in index:
            traits = index[key]['traits']
            for trait in traits:
                for item in traits[trait]:
                    if item in index:
                        f.write('CL;%s;%s;passive object;%s\n' %(index[key]['node_id'], index[item]['node_id'], trait))
                    else:
                        f.write('UN;%s;%s;%s;%s\n' %(index[key]['node_id'], key, trait, item.encode('utf-8')))

index = scrape_eol()
generate_csv(index)
