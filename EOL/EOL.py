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

    lateralLinks = [l for l in links if isinstance(l, str) == False]
    hierarchyLinks = [l for l in links if isinstance(l, str)]

    finalLinks = []

    for l in set(lateralLinks):
        finalLinks.append((title, l.text, 'lateral'))

    finalLinks = finalLinks + find_bigrams(hierarchyLinks[:-1] + [title])
    #print(links)
    return finalLinks


def get_node_data(id):
    url = "https://eol.org/pages/%s/details" %id
    r  = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.title.text.split(' - ')[-3]
    description_data = soup.find("div", { "class" : "copy" }).get_text()
    node = {'eol_id': id, 'title': title}
    node['links'] = get_links(str(id), title)
    node['description'] = description_data
    return node


get_node_data(94313)
