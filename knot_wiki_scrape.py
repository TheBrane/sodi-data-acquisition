#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:51:31 2019

The Brane
'Knot' wikipedia scraping script version 1.0

@author: keonpark
"""

# Importing Libraries
import sys
import csv
import wikipedia
import re
import urllib.request
from bs4 import BeautifulSoup as bs4
import requests




def main_knot():

    """
    Part 1: Creating a classification structure
    - Link Knot to cluster parent ("Knot" is a kind of "Method")
    - Within the wikipedia page, go to the section Knot categories. For each category, create a cluster with the title adding "knot" and the definition.
    - Link each new cluster to Knot
    """


    """
    Part 1-1: Scraping data from 'Knot' wiki page and append in a separate list
    """
    # Get 'title' & 'summary' of Wikipedia page of 'Knot' for data entry
    knot_title = wikipedia.WikipediaPage('Knot').title
    knot_summary = wikipedia.WikipediaPage('Knot').summary

    # Get 'Knot Categories' from 'Knot' Wikipedia page
    knot_url = requests.get('https://en.wikipedia.org/wiki/Knot').text
    knot_soup = bs4(knot_url)
    knot_data = knot_soup.find('div', {'id':"mw-content-text"})
    knot_data_dt = knot_data.findAll('dt')

    # Creating Nodes for Knot categories from 'Knot' Wikipedia page
    knot_categories = []
    _dict_ = {}
    _dict_['Knot'] = 1
    _dict_['Releasing knot'] = 2
    _dict_['Binding knot'] = 3
    _dict_['Quick-release knot'] = 4
    _dict_['Jamming knot'] = 5
    _dict_['Fair knot'] = 6
    _dict_['Non-jamming knot'] = 7

    # category_id_count: starting from 'bend knot' 
    category_id_count = 8

    for category in knot_data_dt:
        category_list = category.find('a')
        knot_title = category_list.get('title')

        if 'knot' not in knot_title:
            knot_title = knot_title + ' knot'

        elif '(knot)' in knot_title:
            knot_title = knot_title.split(' ')[0] + ' knot'

        knot_categories.append(knot_title)
        _dict_[knot_title] = category_id_count
        category_id_count = category_id_count + 1

    # Get summary of each knot category & append them in a list
    category_summary = knot_soup.find('div', {'class':"mw-parser-output"})
    categories = category_summary.findAll('dl')

    # categories[10] = a 'dl' tag with Knot categories
    summaries_cat = categories[10].select('dd')

    # Using for loop to append category summaries
    knot_categories_summaries = []
    for sum_cat in summaries_cat:
        knot_categories_summaries.append(sum_cat.text)

    """
    Part 2: Treating each topic 
    - Go to https://en.wikipedia.org/wiki/List_of_knots
    - Go to first hyperlinked topic ( e.g. Adjustable bend) 
    - Scrape Title, Definition, wikipedia URL
    """
    # 2-1: Scrape title, definition, wiki URL of each knot from 'List of Knot' wiki page 
    LoK_url = requests.get('https://en.wikipedia.org/wiki/List_of_knots').text
    LoK_soup = bs4(LoK_url)
    LoK_data = LoK_soup.find('div', {'class':'mw-parser-output'})
    LoK_categories = LoK_data.findAll('div',{'class':'div-col columns column-width'})

    LoK_list = []
    for cat in LoK_categories:
        t = cat.findAll('li')
        for link in t:
            LoK_list.append(link.find('a'))

    # Get Last two sections ('Y', 'Z') of categories
    Y_section = LoK_data.find('a',{'href':'/wiki/Yosemite_bowline'})
    Z_section_1 = LoK_data.find('a',{'href':'/wiki/Zeppelin_bend'})
    Z_section_2 = LoK_data.find('a',{'href':'/wiki/Zeppelin_loop'})

    LoK_list.append(Y_section)
    LoK_list.append(Z_section_1)
    LoK_list.append(Z_section_2)

    LoK_title = []
    LoK_desc = []
    LoK_url = []
    # category_id_count: starting from 'Adjustable bend'
    category_id_count = 23

    for item in LoK_list:
        # Get titles of each knot category
        name = item.get('title')
        LoK_title.append(name)

        # Get URL
        url = 'https://en.wikipedia.org' + item['href']
        LoK_url.append(url)

        # Get description
        description = wikipedia.WikipediaPage(name).summary
        LoK_desc.append(description)

        # Chekcing redundancy 
        if name in list(_dict_.keys()):
            continue
        else:
            _dict_[name] = category_id_count
            category_id_count = category_id_count + 1

        # Progress...
        print('Scraping for {0} in progress...'.format(name))

    """
     Part 3: Property Window information (Category, Related, Releasing, Typical Use) of each Knot page
    """
    # Using loop to get Property window information of each knot
    prop_dict = {}
    for j in range(len(LoK_url)):
        prop_name = LoK_title[j]
        prop_url = requests.get(LoK_url[j]).text
        prop_soup = bs4(prop_url)

        # Creating empty dictionary for each knot for adding another dict of Property window information
        prop_dict[prop_name] = {}

        # ** Some pages does NOT have property window ** 
        # Appending information to dictionary    
        if prop_soup.find('table', {'class':'infobox'}) != None:
        # If Property Window exists,
            prop_data = prop_soup.find('table', {'class':'infobox'})
            prop_data_tr = prop_data.findAll('tr')  
            prop_data_td = prop_data.findAll('td')

            for i in range(len(prop_data_tr)):
                type_name = prop_data_tr[i].find('th', {'scope':'row'})
                contents = prop_data_tr[i].td

                if type_name and contents != None:
                    type_ = type_name.getText()
                    contents_ = contents.getText()

                    # Adding condition for class 'Typical use'      
                    if type_ == 'Typical use':
                        # If <a> tag does NOT EXIST in 'Typical use' class 
                        if prop_data_tr[i].find('a') == None:
                            continue

                        else:
                            prop_dict[prop_name][type_] = []
                            if len(prop_data_tr[i].findAll('a')) == 1:
                                # When there is only 1 'Typical use' entity
                                TU_ = prop_data_tr[i].find('a')
                                TU = TU_.get('title')
                                prop_dict[prop_name][type_].append(TU)

                            else:
                                # When there are more than 1 'Typical use' entity
                                prop_dict[prop_name][type_] = []
                                for k in range(len(prop_data_tr[i].findAll('a'))):
                                    hyperlink = prop_data_tr[i].findAll('a')
                                    _TU = hyperlink[k].get('title')
                                    prop_dict[prop_name][type_].append(_TU)

                    # Adding condition for class 'Related'      
                    elif type_ == 'Related':

                        if prop_data_tr[i].find('a') == None:
                            continue

                        else:
                            prop_dict[prop_name][type_] = []
                            if len(prop_data_tr[i].findAll('a')) == 1:       

                                # Scrape 'Related' entity with hyperlinks only
                                RE = prop_data_tr[i].find('a')
                                RE = RE.get('href')
                                RE_url = 'https://en.wikipedia.org/' + str(RE)
                                RE_url = requests.get(RE_url).text
                                RE_soup = bs4(RE_url)
                                RE_data = RE_soup.find('div', {'id':'content'})
                                RE_head =  RE_data.find('h1', {'id':'firstHeading'})
                                RE_title = RE_head.text
                                RE_sum = wikipedia.WikipediaPage(RE_title).summary 

                                prop_dict[prop_name][type_].append(RE_title)

                            else:
                                # When there are more than 1 'Related' entity
                                for j in range(len(prop_data_tr[i].findAll('a'))):
                                    RE_ = prop_data_tr[i].findAll('a')
                                    RE_ = RE_[j].get('href')
                                    RE_url_ = 'https://en.wikipedia.org/' + str(RE_)
                                    RE_url_ = requests.get(RE_url_).text
                                    RE_soup_ = bs4(RE_url_)
                                    RE_data_ = RE_soup_.find('div', {'id':'content'})
                                    RE_head_ =  RE_data_.find('h1', {'id':'firstHeading'})

                                    RE_title_ = RE_head_.text
                                    prop_dict[prop_name][type_].append(RE_title_) 

                    else:
                        # Any other classes inside Property Window
                        prop_dict[prop_name][type_] = contents_

                elif type_name or contents == None:
                    continue


        else: 
            continue




    """
    'Releasing' class & 'Category' class information from Property window

    - Created node (CN) for each 'Releasing' & 'Category' knot if it is new.
    - For each new "Releasing" entity, create a new cluster adding "knot" after the word with its definition
    """
    for j in range(len(LoK_title)):
        title_c = LoK_title[j]
        title_keys_c = list(prop_dict[title_c].keys())

        if prop_dict[title_c] == {}:
            continue

        elif 'Category' not in title_keys_c:
            continue

        else:
            # Preventing redundancy among entities
            # length = 1 meaning the entity is already appended in the dictionary
            if len(prop_dict[title_c]['Category']) == 1:
                continue

            else:
                Ca_entity = prop_dict[title_c]['Category']
                prop_dict[title_c]['Category'] = []
                prop_dict[title_c]['Category'].append(Ca_entity)


    for j in range(len(LoK_title)):
        title = LoK_title[j]
        title_keys = list(prop_dict[title].keys())

        # If the category does NOT have a Property window
        if prop_dict[title] == {}:
            continue

        # If the category has a Property window but does NOT have a 'Releasing' class
        elif 'Releasing' not in title_keys:
            continue

        else:
            # Preventing redundancy among entities
            # length = 1 meaning the entity is already appended in the dictionary
            if len(prop_dict[title]['Releasing']) == 1:
                continue

            else:
                Re_entity = prop_dict[title]['Releasing']

                # Special Cases in 'Releasing' entities: Different names but lead to the same information
                # Converting string values to list for easier indexing
                if Re_entity == 'Non- jamming':
                    Re_entity = 'Non-jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Jamming possible':
                    Re_entity = 'Jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Often jams':
                    Re_entity = 'Jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Extreme jamming':
                    Re_entity = 'Jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Quick release':
                    Re_entity = 'Quick-release'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Unload the working end':
                    Re_entity = 'Jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Jamming, but not always':
                    Re_entity = 'Jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                elif Re_entity ==  'Non-jamming, releasable under load':
                    Re_entity = 'Non-jamming'
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

                else:
                    prop_dict[title]['Releasing'] = []
                    prop_dict[title]['Releasing'].append(Re_entity)

    # Scraping information completed

    """
    Writing csv file with stored information
    NOTE: 'Related' & 'Releasing' class need to be added AFTER creating all nodes for 'List of Knots'

    """
    # All knot categories have following 'Releasing' entities only
    releasing_class = ['Binding', 'Quick-release', 'Jamming', 'Fair', 'Non-jamming']
    releasing_def = ['Knots that are resistant to jamming are called non-jamming knots.',
                     'A binding knot is a knot that may be used to keep an object or multiple loose objects together, using a string or a rope that passes at least once around them. There are various binding knots, divided into two types. Friction knots are held in place by the friction between the windings of line. Knotted-ends knots are held in place by the two ends of the line being knotted together.',
                    'A jamming knot is any knot that becomes very difficult to untie after use. Knots that are resistant to jamming are called non-jamming knots.',
                     'A jamming knot is any knot that becomes very difficult to untie after use. Knots that are resistant to jamming are called non-jamming knots.',
                     'A jamming knot is any knot that becomes very difficult to untie after use.']   


    id_count = 1
    prop_keys = list(prop_dict.keys())
    dict_node_count = {}    
    # New file: 'output' to write a structured data
    with open('output_knot.csv', 'w+') as output_csv:
        writer = csv.writer(output_csv, lineterminator = '\n')

        # CN for 'Knot' 
        writer.writerow(['CN', str(id_count),knot_title,knot_summary])
        writer.writerow(['SC', str(id_count)])
        writer.writerow(['CL', '84863803',str(id_count),'is a kind of', 'contains'])

        dict_node_count[knot_title] = id_count
        id_count = id_count + 1

        # Creating new cluster for 'Releasing knot' // Linking 'Releasing knot' to 'Knot'
        Releasing_knot_id = id_count
        writer.writerow(['CN', str(id_count),'Releasing knot'])
        writer.writerow(['SC', str(id_count)])
        writer.writerow(['CL', str(id_count-1), str(id_count),'is a kind of', 'contains'])

        dict_node_count['Releasing knot'] = id_count
        id_count = id_count + 1

        # For each new "Releasing" entity, create a new cluster adding "knot" after the word with its definition
        # Link all new Releasing knot clusters to the Releasing knot cluster using the verbs is a kind of/contains
        for i in range(len(releasing_class)):
            re_knot_name = str(releasing_class[i] + ' knot')
            writer.writerow(['CN', str(id_count), re_knot_name, releasing_def[i]])
            writer.writerow(['CL', str(Releasing_knot_id), str(id_count),'is a kind of', 'contains'])

            dict_node_count[re_knot_name] = id_count
            id_count = id_count + 1

        # id_count for 'Knot' = 1 
        # id_count for 'Releasing knot' = 2
        prop_window_class = ['Category', 'Related', 'Releasing', 'Typical use']
        # Loop for creating nodes for each category from Knot page('https://en.wikipedia.org/wiki/Knot')
        # Link each category to 'Knot' cluster (1)
        for i in range(len(knot_categories)):
            writer.writerow(['CN', str(id_count), knot_categories[i],knot_categories_summaries[i]])
            writer.writerow(['SC', str(id_count)])
            writer.writerow(['CL', '1',str(id_count),'is a kind of', 'contains'])

            dict_node_count[knot_categories[i]] = id_count    
            id_count = id_count + 1

        # Define keys for knot category dictionary  
        dict_node_count_keys = list(dict_node_count.keys())
        for j in range(len(LoK_title)):
            title = LoK_title[j] 
            desc = LoK_desc[j]
            url = LoK_url[j]
            title_keys_c = list(prop_dict[title].keys())

            writer.writerow(['CN',str(id_count), title, desc, url])
            writer.writerow(['SC',str(id_count)])
            dict_node_count[title] = id_count 

            # Linking 'Category' information from Property window to knot categories created in Step 1. 
            # When Property window has no fields at all
            if prop_dict[title] == {}:
                id_count = id_count + 1
                continue

            elif 'Category' not in title_keys_c:
                id_count = id_count + 1
                continue

            # If 'Category' class has values
            else:
                # If 'Category' class has ONLY one entity
                if len(prop_dict[title]['Category']) == 1:
                    key_c = str(prop_dict[title]['Category'][0]) + ' knot'

                    if key_c in dict_node_count_keys:
                        writer.writerow(['CL', dict_node_count[key_c], dict_node_count[title], 'is kind of','contains'])

                    # CN for NEW 'Category' entity and append it to dict_node_count
                    else:
                        # need to work on desc, url of new CN
                        writer.writerow(['CN', str(id_count),key_c ])
                        dict_node_count[key_c] = id_count
                        id_count = id_count + 1
                        continue

                # If 'Category' class has more than one entity
                else:
                    key_c = prop_dict[title]['Category']
                    for i in range(len(key_c)):
                        key_c = prop_dict[title]['Category'][i] + ' knot'
                        writer.writerow(['CL', dict_node_count[key_c], dict_node_count[title], 'is kind of','contains'])

                id_count = id_count + 1

    # 'Related' class from Property Window
        _d_keys = list(_dict_.keys())
        dict_node_count_keys = list(dict_node_count.keys())
        for k in range(len(LoK_title)):
            title_ = LoK_title[k] 
            desc_ = LoK_desc[k]
            url_ = LoK_url[k]

            title_keys_ = list(prop_dict[title_].keys())

            if prop_dict[title_] == {}:
                continue

            elif 'Related' not in title_keys_:
                continue

            elif len(prop_dict[title_]['Related']) == 1:
                # 'Related' class with 1 entity
                if prop_dict[title_]['Related'][0] in dict_node_count_keys:
                    key_1 = prop_dict[title_]['Related'][0]
                    writer.writerow(['CL', dict_node_count[key_1], dict_node_count[title_], 'is related to','is related to'])

                # CN if 'Related' entity is not in the existing Nodes
                else:
                    key_2 = prop_dict[title_]['Related'][0]
                    sum_key_2 = wikipedia.WikipediaPage(key_2).summary
                    url_key_2 = wikipedia.WikipediaPage(key_2).url

                    writer.writerow(['CN', str(id_count), key_2, sum_key_2, url_key_2])
                    dict_node_count[key_2] = id_count

                    writer.writerow(['CL', dict_node_count[title_] ,str(id_count),'is related to','is related to'])
                    id_count = id_count + 1

            # 'Related' class with more 1 entities        
            else:
                R_length = len(prop_dict[title_]['Related'])

                for r in range(R_length):

                    if prop_dict[title_]['Related'][r] in dict_node_count_keys:

                        key_3 = prop_dict[title_]['Related'][r]
                        writer.writerow(['CL', dict_node_count[key_3], dict_node_count[title_], 'is related to','is related to'])
                    else:
                        key_4 = prop_dict[title_]['Related'][r]
                        if key_4 == 'Spider hitch':
                            continue
                        else:
                            sum_key_4 = wikipedia.WikipediaPage(key_4).summary
                            url_key_4 = wikipedia.WikipediaPage(key_4).url

                            writer.writerow(['CN', str(id_count), key_4, sum_key_4,url_key_4])
                            dict_node_count[key_4] = id_count

                            writer.writerow(['CL', dict_node_count[title_] ,str(id_count),'is related to','is related to'])
                            id_count = id_count + 1

        # 'Releasing' class from Property window
        for i in range(len(LoK_title)):
            title_r = LoK_title[i] 
            desc_r = LoK_desc[i]
            url_r = LoK_url[i]
            title_keys_r = list(prop_dict[title_r].keys())

            if prop_dict[title_r] == {}:
                continue

            elif 'Releasing' not in title_keys_r:
                continue

            else:
                Re_key = prop_dict[title_r]['Releasing'][0]

                writer.writerow(['CL', dict_node_count[str(Re_key +' knot')] , dict_node_count[title_r],'is a kind of','contains'])


        # 'Typical use' class from Property window
        for i in range(len(LoK_title)):
            title_t = LoK_title[i] 
            desc_t = LoK_desc[i]
            url_t = LoK_url[i]
            title_keys_t = list(prop_dict[title_t].keys())
            dict_node_count_keys = list(dict_node_count.keys())

            if prop_dict[title_t] == {}:
                continue

            elif 'Typical use' not in title_keys_t:
                continue

            else:
                Tu_key = prop_dict[title_t]['Typical use']

                # If there is ONLY 1 entitiy for 'Typical use' class
                if len(Tu_key) == 1:
                    Tu_key = prop_dict[title_t]['Typical use'][0]

                    # If the node does NOT exit, CN for the new entity
                    if Tu_key not in dict_node_count_keys:

                        Tu_key_sum = wikipedia.WikipediaPage(Tu_key).summary
                        Tu_key_url = wikipedia.WikipediaPage(Tu_key).url
                        writer.writerow(['CN', str(id_count), Tu_key + ' knot', Tu_key_sum, Tu_key_url])

                        # Link between 'Activity' cluster and the new node
                        writer.writerow(['CL', '85170354', str(id_count), 'is kind of', 'contains'])
                        writer.writerow(['CL', dict_node_count[title_t] , str(id_count), 'is used for', 'uses'])

                        dict_node_count[Tu_key + ' knot'] = id_count
                        id_count = id_count + 1

                    # If the node already exist in 'dict_node_count'
                    else:
                        writer.writerow(['CL', dict_node_count[title_t], dict_node_count[Tu_key], 'is kind of', 'contains'])

                # If there are more than 1 entity for 'Typical use' class
                else:
                    for i in range(len(Tu_key)):
                        Tu_key = prop_dict[title_t]['Typical use'][i]

                        # If the node does NOT exit, CN for the new entity
                        if Tu_key not in dict_node_count_keys:

                            Tu_key_sum = wikipedia.WikipediaPage(Tu_key).summary
                            Tu_key_url = wikipedia.WikipediaPage(Tu_key).url
                            writer.writerow(['CN', str(id_count), Tu_key + ' knot', Tu_key_sum, Tu_key_url])

                            # Link between 'Activity' cluster and the new node
                            writer.writerow(['CL', '85170354', str(id_count), 'is kind of', 'contains'])
                            writer.writerow(['CL', str(id_count), dict_node_count[title_t], 'is used for', 'uses'])

                            dict_node_count[Tu_key + ' knot'] = id_count
                            id_count = id_count + 1

                        # If the node already exist in 'dict_node_count'
                        else:
                            writer.writerow(['CL', dict_node_count[Tu_key], dict_node_count[title_t], 'is used for', 'uses'])


if __name__ == "__main__":
    main_knot()
