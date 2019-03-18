# -*- coding: utf-8 -*-
'''
	Kaushik Tandon
	March 2019
	Given a Wikipedia list (ie https://en.wikipedia.org/wiki/List_of_intergovernmental_organizations), extract the different headers, subheaders, and individual topics as nodes.
	Create links to maintain the tree structure and correctly classify the nodes. 
'''

import sys
import codecs
import csv
import time
from bs4 import BeautifulSoup,NavigableString
import requests
import json

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

'''
Determine the title of the List
'''
def extractTitle(soup,start_url):
	if(soup != None):
		try:
			title = soup.find('h1',{'id':'firstHeading'})
			if(title != None):
				return title.text
		except Exception as e:
			pass			
	print("Unable to cleanly find title of list. Returning default value")
	#Default value is extracting straight from the URL
	title = start_url[start_url.find("List_of_") + 8:]
	title = title.replace("_", " ")
	return title

'''
Determine an URL from the first paragraph for the list
'''
	
def extractTitleURL(soup,title,start_url):
	if(soup != None):
		#print title
		try:
			paragraph = soup.find('p')
			return 'https://en.wikipedia.org' + paragraph.find('a',href=True)['href']
		except Exception as e:
			print("Title URL not found in first paragraph")
			return start_url
	return start_url
'''
Create a new node and link it to the corresponding parent. Link text depends on if the parent is a cluster
'''

def createNode(title,url,idCount,output_file,createdNodes, linkedToCluster,parent, description):
	if(title in createdNodes):
		print(title + " was already created with ID " + createdNodes[title])
		return idCount, createdNodes
	with open(output_file,'a+') as csvfile:
		writer = csv.writer(csvfile,lineterminator = '\n')#,delimiter=';',quoting=csv.QUOTE_NONE)
		node_id = str(idCount)
		idCount = idCount + 1
		title = title.replace(' ', ' ')

		if(description == None):
			writer.writerow(['CN',node_id,str(title),'reference',url])
		else:
			description = description.replace(';','-')
			writer.writerow(['CN',node_id,str(title),'reference',url,'description',description])

		createdNodes[title] = node_id

		if(linkedToCluster and parent != None):
			#writer.writerow(["SC",node_id])
			writer.writerow(['CL',parent,node_id,'is a kind of','contains'])
		elif(not linkedToCluster and parent != None):
			writer.writerow(['CL',parent,node_id,'is categorised as','categorizes'])

	return idCount, createdNodes
'''
If the node already exists, we can just create the corresponding links
'''
def createLink(node_id,linkedToCluster,parent,output_file):
	with open(output_file,'a+') as csvfile:
		writer = csv.writer(csvfile,lineterminator = '\n')#,delimiter=';',quoting=csv.QUOTE_NONE)
		#if(SC):
		#	writer.writerow(["SC",node_id])
		if(linkedToCluster and parent != None):
			writer.writerow(['CL',parent,node_id,'is a kind of','contains'])
		elif(not linkedToCluster and parent != None):
			writer.writerow(['CL',parent,node_id,'is categorised as', 'categorizes'])
'''
Load the nodes JSON file into a dict
'''
def load_nodesJSON(nodes_file):
	nodes = dict()
	print ("Loading nodes")
	with open(nodes_file) as f:
		for line in f:
			data = json.loads(line)
			a_id = str(data['data']['_key'])
			name = str(data['data']['t'])
			nodes[name] = a_id
	print ("Loaded nodes")
	return nodes
'''
Given the title of the list, determine a potential cluster ID for the title. 
This is done by looking at the last word of the title and checking if that or the non-plural form of the word is in the database.
'''
def determineClusterParent(title,nodes):
	if(len(title.split(" ")) > 1):
		title_spaces = title.split(" ")
		last_word = title_spaces[-1]

		if(nodes.get(last_word) != None):
			return str(nodes[last_word])
		elif(nodes.get(last_word[0:-1]) != None):
			return str(nodes[last_word[0:-1]])
		elif(nodes.get(last_word.title()) != None):
			return str(nodes[last_word.title()])
		elif(nodes.get(last_word[0:-1].title()) != None):
			return str(nodes[last_word[0:-1].title()])
		else:
			return None
	else:
		if(nodes.get(title) != None):
			return nodes[title]
		else:
			return None
def main():
	if(len(sys.argv) < 4):
		print("USAGE: python wikipedia_lists.py [Start Wikipedia URL] [Database JSON Links File] [Name of output csv file] [Cluster ID]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python link_recursion.py https://en.wikipedia.org/wiki/List_of_artificial_intelligence_projects \"All links.json\" output.csv 85013123 ")
	else:
		start_url = sys.argv[1]
		nodes_file = sys.argv[2]
		output_file = sys.argv[3]
	
		#Create file to write to
		with open(output_file,'w+') as csvfile:
			pass
		idCount = 1
		parent_dict = dict()
		createdNodes = dict()
		db_nodes = load_nodesJSON(nodes_file)
		#Query wikipedia lists page
		response = requests.get(start_url)
		soup = BeautifulSoup(response.text,'html.parser')

		#Determine the title of the list (ie intergovernmental organizations)
		title_of_list = extractTitle(soup,start_url)
		if("List of" in title_of_list):
			title_of_list = title_of_list[8:]
		#Find a relevant URL for the title
		title_url = extractTitleURL(soup,title_of_list,start_url)
		title_of_list = title_of_list[0].upper() + title_of_list[1:]
		#Try to determine the parent
		if(len(sys.argv) >= 5):
			cluster_parent = sys.argv[4]
		else:
			cluster_parent = determineClusterParent(title_of_list,db_nodes)
			print("Using " + str(cluster_parent) + " as cluster for this list")
			if(cluster_parent == None):
				sys.exit("Unable to determine cluster for this list. Please manually define this parameter")
		parent_dict[title_of_list] = cluster_parent
		#Create the title of list node and set parent
		if(title_of_list in db_nodes):
			createdNodes[title_of_list] = db_nodes[title_of_list]
		else:
			idCount, createdNodes = createNode(title_of_list,title_url,idCount,output_file,createdNodes,True,cluster_parent,None)

		#Use the table of contents to determine the relationships of the list items
		table_of_contents = soup.find('div',{'class':'toc'})
		table_of_contents_hrefs = dict()
		if(table_of_contents != None):
			#Check if table of content descriptiptions are helpful
			if(len(table_of_contents.findAll('li', {'class': 'toclevel-1'})) != 0):
				#I can't recall seeing a table structure that had more than 2 layers. If something breaks, than this might be the case.
				class_to_check = 'toclevel-1'
				for element in table_of_contents.findAll('li', {'class': 'toclevel-1'}):
					names = str(element.text).split("\n")

					i = 0
					parent = ""
					hrefs = element.findAll('a',href=True)
					#Item 2 will contain Item 2.1, 2.2, etc. Using a counter to keep track of what's been seen so far
					for name in names:
						if(name != ""):
							name = name.split(" ")[1:]
							name = ' '.join(name)

							if(name == 'See also' or name == 'References' or name == "External links" or name == "Notes"):
								i = i + 1
								continue
							else:
								if(i == 0):
									parent_dict[name] = title_of_list
									parent = name
								else:
									if(parent == ""): continue
									parent_dict[name] = parent
								table_of_contents_hrefs[name] = start_url + hrefs[i]['href']

								if(name in db_nodes):
									node_id = str(db_nodes[name])
									createdNodes[name] = node_id
									createLink(node_id,False,createdNodes[parent_dict[name]],output_file)
								else:
									idCount, createdNodes = createNode(name,table_of_contents_hrefs[name],idCount,output_file,createdNodes,False,createdNodes[parent_dict[name]],None)
								i = i + 1
				#Now I have the general table structure. Going to each section to see what content there is
				to_create_hrefs = dict()
				for name, link in table_of_contents_hrefs.iteritems():
					subheaders = soup.find('span',{'id':name.replace(" ", "_")})
					list_elements = subheaders.parent.find_next_sibling('ul')
					print ("Extracting from: " + link)
					if(list_elements == None):
						print("Nothing found for: " + name)
						continue

					#Each element under a subheader
					for element in list_elements:
						#Is there another list embedded?
						if(element.find('ul') != -1 and element.find('ul') != None):
							this_parent_name = element.find('a').text
							if('/wiki/' in element.find('a')['href'] or '/w/' in element.find('a')['href']):
								this_parent_href = 'https://en.wikipedia.org' + element.find('a')['href']
							else:
								this_parent_href = str(element.find('a')['href'])

							#Create the node here and find children
							if(this_parent_name in db_nodes):
								node_id = str(db_nodes[this_parent_name])
								createdNodes[this_parent_name] = node_id
								createLink(node_id,False,createdNodes[name],output_file)
								createLink(node_id,True,cluster_parent,output_file)
							else:
								idCount, createdNodes = createNode(this_parent_name,this_parent_href,idCount,output_file,createdNodes,False,createdNodes[name],None)
								createLink(idCount-1,True,cluster_parent,output_file)
							for li in element.find('ul'):
								#Only look at Tags, not NavigableStrings
								if(isinstance(li,NavigableString)):
									continue
								new_name = li.text
								if('/wiki/' in li.find('a')['href'] or '/w/' in li.find('a')['href']):
									new_href = 'https://en.wikipedia.org' + li.find('a')['href']
								else:
									new_href = li.find('a')['href']
								#Set parent 
								parent_dict[new_name] =  this_parent_name
								to_create_hrefs[new_name] = new_href
								#Create node

						else:
							#Find the element
							new_element = element.find('a')
							if(new_element == -1 or new_element == None): continue
							#Get name and link of element
							element_name = new_element.text
							if('/wiki/' in new_element['href'] or '/w/' in new_element['href']):
								element_href = 'https://en.wikipedia.org' + new_element['href']
							else:
								element_href = new_element['href']
							parent_dict[element_name] = name
							to_create_hrefs[element_name] = element_href
							#Create element
				for name, link in to_create_hrefs.iteritems():
					if(name in db_nodes):
						node_id = str(db_nodes[name])
						createdNodes[name] = node_id
						createLink(node_id,False,createdNodes[parent_dict[name]],output_file)
						createLink(node_id,True,cluster_parent,output_file)
					else:
						idCount, createdNodes = createNode(name,link,idCount,output_file,createdNodes,False,createdNodes[parent_dict[name]],None)
						createLink(idCount-1,True,cluster_parent,output_file)

			else:
				#List of Knots like. Table of content headers are meaningless
				print("Can't handle this kind of list too well. Attempting output")
				
				parent = title_of_list
				lists = soup.find('div',{'id':'mw-content-text'}).findAll('ul')
				toc = True
				for li in lists:
					if(li.get('id') == "footer-icons" or li.get('id') == "footer-places" or li.get('id') == "footer-info"):
						continue
					elif(li.get('class') != None and ('menu' in li.get('class') or 'noprint' in li.get('class'))):
						continue
					if(toc):
						toc = False
						continue
					try:
						title = li.find('a').text
						if('List of ' in title or title == 'Category'):
							continue
					except Exception as e:
						continue
					if(title == 'See also' or title == 'References' or title == 'External links'):
						continue
					if(li.parent.get('class') != None and 'navbar' in li.parent.get('class')):
						continue
					if(li.parent.get('style') != None and str(li.parent.get('style')) == 'padding:0em 0.25em'):
						continue
					else:
						print (li.parent.get('style'))
					for element in li:
						if(isinstance(element,NavigableString)):
							continue
						try:
							element_name = element.find('a')['title']
							if("List of" in element_name):
								continue
							element_href = 'https://en.wikipedia.org' + element.find('a')['href']
							#print element, element.text
							element_description = element.text
							if(element_name in db_nodes):
								node_id = str(db_nodes[element_name])
								createdNodes[element_name] = node_id
								createLink(node_id,False,createdNodes[parent],output_file)
							else:
								idCount, createdNodes = createNode(element_name,element_href,idCount,output_file,createdNodes,False,createdNodes[parent],element_description)
								createLink(idCount-1,True,cluster_parent,output_file)
						except Exception as e:
							pass
				

		else:
			#No table of contents lists. This likely will not work for all kinds of lists yet
			print ("No table of contents found. Please verify the output to ensure it meets the criteria")
			for headline in soup.findAll('span',{'class':'mw-headline'}):
				header = headline.text
				href = start_url + '#' + header.replace(" ", "_")
				if(header in db_nodes):
					node_id = str(db_nodes[header])
					createdNodes[header] = node_id
					createLink(node_id,False,createdNodes[title_of_list],output_file)
				else:
					idCount, createdNodes = createNode(header,href,idCount,output_file,createdNodes,False,createdNodes[title_of_list],None)
				parent_dict[header] = title_of_list

				print("Extracting from: " + href)
				list_elements = headline.parent.find_next_sibling('ul')
				for element in list_elements:
					if(isinstance(element,NavigableString)):
						continue

					new_element_name = element.text
					new_element_href = element.find('a').get('href')
					if('/wiki/' in new_element_href or '/w/' in new_element_href):
						new_element_href = 'https://en.wikipedia.org' + new_element_href
					parent_dict[new_element_name] = header
					if(new_element_name in db_nodes):
						node_id = str(db_nodes[new_element_name])
						createdNodes[new_element_name] = node_id
						createLink(node_id,False,createdNodes[parent_dict[new_element_name]],output_file)
						createLink(node_id,True,cluster_parent,output_file)
					else:
						idCount, createdNodes = createNode(new_element_name,new_element_href,idCount,output_file,createdNodes,False,createdNodes[parent_dict[new_element_name]],None)
						createLink(idCount-1,True,cluster_parent,output_file)


if __name__ == '__main__':
	main()