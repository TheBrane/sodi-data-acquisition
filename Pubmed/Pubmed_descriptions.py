# -*- coding: utf-8 -*-
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import sys

def get_info(url):

    info = {}
    browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string

    soup = BeautifulSoup(innerHTML)
    items = soup.find_all('dd', attrs={'class': 'ng-binding'})


    scope = soup.find_all('span', attrs={'id': 'scopeNote'})
    info['Scope'] = scope[0].text


    browser.quit()
    return info

f = open('done.txt', 'r')
done = f.readlines()
done = [i.strip() for i in done]
data = pd.read_csv('pubmed.csv', sep = ';')
data.drop_duplicates(subset=['Title'], inplace = True)

for entry in data.Title[int(sys.argv[1]) : min(int(sys.argv[2]), len(data.Title))]:
    if entry not in done:
        try:
            url = 'https://meshb.nlm.nih.gov/search?searchInField=termDescriptor&sort=&size=20&searchType=exactMatch&searchMethod=FullWord&q=' + entry.replace(' ', '%20')
            info = get_info(url)
            #for r in info['related']:
                #with open('lateral_links.txt', 'a') as the_file:
                    #the_file.write((entry + ';' + r + '\n').encode('utf8'))
            with open('descriptions.txt', 'a') as the_file:
                    the_file.write((entry + ';' + info['Scope'].replace('\n', ' ').replace('Scope Note','').strip() + '\n').encode('utf8'))
            with open('done.txt', 'a') as the_file:
                the_file.write((entry + '\n').encode('utf8'))
        except:
            pass
