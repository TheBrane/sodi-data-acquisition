from bs4 import BeautifulSoup
import requests

def find_bigrams(input_list):
  ngram = []
  for i in range(len(input_list)):
      try:
          ngram.append((input_list[i],input_list[i+1], 'hierarchical'))
      except:
         pass
  return ngram

def getLinks(id, title):
    url = 'http://www.eol.org/pages/' + id
    r = requests.get(url)
    response = BeautifulSoup(r.text)
    branches = response.findAll("ul", { "class" : "branch" })
    links = []
    for i in branches:
        links.append(i.find("a").contents[0])

    lateralLinks = [l for l in links if isinstance(l, str) == False]
    hierarchyLinks = [l for l in links if isinstance(l, str)]

    finalLinks = []

    for l in lateralLinks:
        finalLinks.append((title,l.text, 'lateral'))

    finalLinks =finalLinks + find_bigrams(hierarchyLinks[:-1] + [title])
    print(finalLinks)
    return links


a = getLinks('94313', 'foo')
