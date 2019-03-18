# -*- coding: utf-8 -*-

'''Kaushik Tandon
   This program scrapes Wikipedia articles related to Environmental Tech. The goal is to build a knowledge graph
   of topics related to AI and categorize them using The Brane's Knowledge Classification System of tags. This program
   successfully creates nodes and links in a CSV file with a false positive rate of less than 10%.
'''
import requests
import csv
from BeautifulSoup import *
import sys
import codecs
import re
import time
import json

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Node:
	def __init__(self,name,ID,isCluster):
		self.name = name
		self.ID = ID
		self.isCluster = isCluster

#Input files
database = 'All nodes.json' #Entire DB - currently is the August backup
terms_to_collect_file = 'terms_to_gather.csv' #Terms to gather table
avoid_terms_file = 'terms_to_avoid.txt' #Terms to avoid table
avoid_categories_file = 'avoid_categories.txt' #categories that should not be scraped

#Output files
category_file = 'categories.txt' #Generated file of categories scraped
created_CSV_file = 'scrape.csv' #Created file after scraping

#Create a represesentation of a category in order to easily store and access important data
class Category:
	def __init__(self,name,url,sub_categories,linked_pages,level,category_num):
		self.name = name
		self.url = url;
		self.sub_categories = sub_categories
		self.linked_pages = linked_pages;
		self.level = level
		self.category_num = category_num

def getURL():
	''' Ask the user for which category url to scrape - default is AI category
		Returns:
			URL as string
	'''
	url = raw_input("Enter URL of wikipedia category page to scrape (or enter for default)")
	if len(url) < 2 or 'wikipedia' not in url:
		url = 'https://en.wikipedia.org/wiki/Category:Sustainable_technologies'
		#url = 'https://en.wikipedia.org/wiki/Category:Game_artificial_intelligence'
	return url
def getLinksFromCategoryPage(page):
	''' Given a category page, this method can extract the pages and the subcategories on each page
		Example: https://en.wikipedia.org/wiki/Category:Artificial_intelligence should return 2 arrays, one with 326 pages and one with 37 category titles
		
		Args:
			page: The URL of the page to extract pages/subcategories from		
		Returns:
			Two arrays - one with list of page urls, one with list of category urls
	'''
	#Page must be of form Category:Name
	pages = []
	sub_categories = []
	soup_html = getHTML(page)
	#Extract pages
	a =  soup_html.findAll('div',{'class': 'mw-category-group'})
	for temp in a:
		pageNames = extractPageNames(temp)
		for pageName in pageNames:
			ind1 = pageName.find('(')
			ind2 = pageName.find('P')
			ind3 = pageName.find("C")
			ind4 = pageName.find(')')
			num = bool(re.search(r'\d', pageName)) #Number in pageName
			#Trying to catch pages of type (5 C, 40 P)
			if(num and ind1 >= 0 and ind4 > 0 and (ind2 > 0 or ind3 > 0)):
				continue
			#Remove weird characters
			pageName = ''.join([i if ord(i) < 128 else '' for i in pageName])
			if(len(pageName) > 0):
				pages.append('https://en.wikipedia.org/wiki/' + str(pageName.strip()))
	#Check for additional pages
	c = soup_html.find('div',{'id': 'mw-pages'})
	if(c != None and len(c.findAll('a')) > 2):
		elemToCheck = c.findAll('a')[1]
		if(str(elemToCheck.text).strip().lower() == 'next page'):
			more_page = 'https://en.wikipedia.org' + str(elemToCheck.get('href'))
			additional_pages = extractAdditionalPages(more_page)
			for page in additional_pages:
				pages.append(page)
	#Look for subcategories
	b = soup_html.findAll('a',{'class': 'CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory'})
	for sub in b:
		sub = str(sub)
		index = sub.find("Category:")
		name = sub[index:sub.find('"',index)]
		sub_categories.append('https://en.wikipedia.org/wiki/' + name.strip())
	return pages,sub_categories
def extractAdditionalPages(page):
	''' Helper method for getLinksFromCategoryPage() to handle pages which have more than 200 pages linked
		Example url: https://en.wikipedia.org/w/index.php?title=Category:Artificial_intelligence&pagefrom=Leaf+Project%0AThe+Leaf+%28AI%29+Project#mw-pages
		Args:
			page: URL of 'next page' category page being scraped
		Returns:
			List of urls of pages in category on specific page
	'''
	additional_pages = list()
	soup_html = getHTML(page)
	a =  soup_html.findAll('div',{'class': 'mw-category-group'})
	for temp in a:
		pageNames = extractPageNames(temp)
		for pageName in pageNames:
			#Trying to catch pages of type (5 C, 40 P) and ignore them
			ind1 = pageName.find('(')
			ind2 = pageName.find('P')
			ind3 = pageName.find("C")
			ind4 = pageName.find(')')
			num = bool(re.search(r'\d', pageName))
			if(num and ind1 >= 0 and ind4 > 0 and (ind2 > 0 or ind3 > 0)):
				continue
			pageName = ''.join([i if ord(i) < 128 else '' for i in pageName])
			if(len(pageName) > 0):
				additional_pages.append('https://en.wikipedia.org/wiki/' + str(pageName.strip()))
	return additional_pages
def getHTML(url):
	''' Uses BeautifulSoup to get the HTML for a page
		Args:
			url: URL of page to get HTML for
		Returns:
			Beautiful Soup object with HTML
	'''
	try:
		r = requests.get(url)
		return BeautifulSoup(r.text)
	except:
		print("Couldn't get HTML for: " + url)

def getTitle(soup_html):
	''' Uses BeautifulSoup html to get the title of the article
		Args:
			soup_html: Beautiful Soup object with HTML (returned by getHTML())
		Returns:
			title of article or "Error"
	'''	
	if(len(soup_html.findAll("h1", {"id": "firstHeading"})) == 0):
		return "Error"
	txt = soup_html.findAll("h1", {"id": "firstHeading"})[0].getText()
	txt = ''.join([i if ord(i) < 128 else '-' for i in txt])
	return txt

def extractSeeAlso(soup_html):
	''' Uses BeautifulSoup html to get the see also categories from a Wikipedia article
		Args:
			soup_html: Beautiful Soup object with HTML (returned by getHTML())
		Returns:
			list of names of articles in the see also category (or empty list)
	'''
	seeAlso = list()
	section = soup_html.find('span', id='See_also')
	if section != None:
		wrongUL = True
		section = section.parent.findNext('ul')
		count = 0
		while(wrongUL):
			count = count + 1
			for litag in section.findAll('a', href=True):
				if litag.get('href') == None and wrongUL:
					continue
				elif 'wiki' not in str(litag.get('href')) and wrongUL:
					continue
				else:
					wrongUL = False
					name = litag.text
					if name == None:
						continue
					name = str(name).strip()

					if('page does not exist' in name):
						continue
					if name in seeAlso:
						continue
					else:
						seeAlso.append(name)
			if(wrongUL):
				section = section.parent.findNext('ul')
			if(count == 5):
				break
	return seeAlso

def extractCategories(soup_html):
	''' Uses BeautifulSoup html to get the categories of a Wikipedia article
		Args:
			soup_html: Beautiful Soup object with HTML (returned by getHTML())
		Returns:
			list of names of categories (or empty list)
	'''
	categories = []
	a = soup_html.find('div',{'class': 'mw-normal-catlinks'})
	if a != None:
		for litag in a.findAll('li'):
			categories.append(str(litag.text))
	return categories

def extractReferences(soup_html):
	''' Uses BeautifulSoup html to get the references of a Wikipedia article
		Args:
			soup_html: Beautiful Soup object with HTML (returned by getHTML())
		Returns:
			list of names of references (or empty list)
	'''	
	references = []
	a = soup_html.find('ol',{'class': 'references'})
	if a != None:
		for litag in a.findAll('li'):
			references.append(str(litag.text))
	return references

def isStub(soup_html):
	''' Uses BeautifulSoup html to determine whether Wikipedia article is a stub
		Args:
			soup_html: Beautiful Soup object with HTML (returned by getHTML())
		Returns:
			True if article is a stub (should be skipped)
	'''
	a = soup_html.find('table',{'class': 'metadata plainlinks stub'})
	if a != None:
		return True
	return False

def loadAvoidTerms():
	''' Load the terms to avoid table from a predefined text file
		Returns:
			list of terms to avoid (lowercase)
	'''
	with open(avoid_terms_file) as f:
		content = f.readlines()
	content = [x.strip().lower() for x in content] 
	return content

def loadAvoidCategories():
	''' Load the categories to avoid from a predefined text file
		Returns:
			list of categories to avoid (lowercase)
	'''
	with open(avoid_categories_file) as f:
		content = f.readlines()
	content = [x.strip().lower() for x in content] 
	return content

def loadGatherTerms():
	''' Load the terms to gather table from a predefined csv file
		Returns:
			dictionary with key being lower case word (and plural versions) and value being the database ID
	'''	
	terms = dict()
	with open(terms_to_collect_file) as f:
		for line in f.readlines():
			words = line.split(',')
			temp_id = str(words[0])
			for word in words:
				word = word.strip().lower()
				word2 = word + 's'
				word3 = word + 'es'
				if(len(word) > 0 and (word[0] < '0' or word[0] > '9')):
					terms[word] = temp_id
					terms[word2] = temp_id
					terms[word3] = temp_id
	return terms
def splitAndLower(words):
	''' Returns a list of words ignoring parentheses and splitting to lowercase
		Args:
			words: list of words to handle
		Returns:
			list of words where each word is lowercase
	'''
	words = words.replace("("," ")
	words = words.replace(")"," ")
	words = words.lower().strip()
	all_words = words.split(" ")
	for i in range(len(all_words)):
		all_words[i] = all_words[i].strip()
	return all_words
def numCapitalsInTitle(title):
	''' Determine the number of capitals in an article title
		Args:
			title: article title to check
		Returns:
			integer number of capitals in the title
	'''
	title = title.replace("("," ").replace(")"," ").strip()
	all_words = title.split(" ")
	numCap = 0
	for word in all_words:
		if len(word) > 0 and word[0].isupper():
			numCap = numCap + 1
	return numCap

def validArticleTitle(article_title,avoid_terms,gather_terms):
	''' Determine if a Wikipedia article title is valid, or if the article should be skipped
		Args:
			article_title: title to check
			avoid_terms: list of terms to avoid
			gather_terms: dict of terms to gather
		Returns:
			True if article title is valid
	'''
	#check for partial match
	words_in_title = splitAndLower(article_title)
	for word in words_in_title:
		if word.lower() in avoid_terms:
			return False
	#All individual words cannot be capital
	allCapital = True
	individualWords = article_title.split(" ")
	if(len(individualWords) > 1):
		for word in individualWords:
			word = word.strip()
			if word[0].islower():
				allCapital = False
			if word.lower() in gather_terms or word[:-1].lower() in gather_terms or (word+'s').lower() in gather_terms or (word+'es').lower() in gather_terms:
				return True
			if word[0] == '(' and word[1].islower():
				allCapital = False
		if(allCapital):
			return False
	#avoid_terms only contains lower case, so convert article_title to lower case for checking
	article_title = article_title.lower()
	#check for full title
	if article_title in avoid_terms:
		return False
	#check for plural title
	if article_title + 's' in avoid_terms or article_title + 'es' in avoid_terms:
		return False
	return True

def validCategoryName(name,invalidNames):
	''' Determines whether a category name is invalid and should be scraped
		Args:
			name: string name of category
			invalidNames: list of invalid names loaded from file
		Returns:
			True if valid name, False if not
	'''
	invalidWords = ['researchers','video games','competitions','comic','film','history','fiction']
	if name in invalidNames:
		return False
	for word in invalidWords:
		if word in name.lower() or word + 's' in invalidWords:
			return False
	return True

#This is needed since the getText() method in beautiful soup returns some messy data here
def extractTextFromParagraph(paragraph):
	''' Extract actual text from a paragraph element
		Args:
			paragraph: Beautiful Soup paragraph element
		Returns:
			string containing text in paragraph
	'''
	paragraph = str(paragraph)
	string = ''
	i = 0
	while(i < len(paragraph)):
		c = str(paragraph[i])
		#Skip until end of tag
		if c == '<':
			i = paragraph.find('>',i)
		elif c == '&':
			if((paragraph.find(';',i+1)) != -1):
				i = paragraph.find(';',i+1)
			#I actually want the 2nd occurence, else I get left with the source number. However there may be a legitimate ;
			if((paragraph.find(';',i+1)) != -1):
				i = paragraph.find(';',i+1)
		#Skip until end of bracket
		elif c == '[' and paragraph.find(']',i) != -1:
			i = paragraph.find(']',i)
		#Good character
		else:
			string += c;
		i = i + 1
	#Replace all weird characters (mainly hyphens)
	string =''.join([i if ord(i) < 128 else '-' for i in string])
	return string.replace("--","-").strip()
def extractLinksFromParagraph(paragraph):
	''' Extract any links in the paragraph in order to check for matches later
		Args:
			paragraph: Beautiful Soup paragraph element
		Returns:
			list of links in the paragraph
	'''
	titles = list()
	a = (paragraph.findAll('a'))
	for link in a:
		link = str(link)
		if('href' not in link):
			continue
		ind = link.find('>') + 1
		if(ind == 0):
			continue
		text = link[ind:link.find('<',ind)]
		titles.append(text.strip())
	return titles
def extractPageNames(tags):
	''' Helper method to extract the list of pages from a category page
		Args:
			tags: Beautiful Soup div element
		Returns:
			List of names of pages
	'''
	names = []
	tags = str(tags)
	index = tags.find('>',tags.find('title='))
	while index != -1 and index < len(tags) and tags.find('<',index) != -1:
		names.append(tags[index+1:tags.find('<',index)])
		index = tags.find('>',tags.find('title=',index))
	return names

def getPotentialFirstNoun(paragraph, article_title):
	''' Extract potential nouns to look at from the paragraph of the Wikipedia article
		Args:
			paragraph: Wikipedia article first paragraph
			article_title: title of Wikipedia article
		Returns:
			True if article title is valid
	'''
	nouns = list()
	first_sentence = paragraph[0:paragraph.find('.')]
	second_half = first_sentence#[len(article_title) + 1:]
	if(second_half == None or len(second_half) <= 1):
		return nouns

	if(second_half[0] == '('):
		second_half = second_half[second_half.find(')') + 2:]

	if('(' in second_half):
		second_half = second_half[0:second_half.find('(')] + second_half[second_half.find(')')+1:]

	words = second_half.split(' ')
	ind = 0
	for word in words:
		if ('-' in word and 'human' not in word and ('machine' not in word or 'computer' not in word)):
			#words.remove(word)
			#word1 = word.split('-')[0]
			#word2 = word.split('-')[1]
			#words.insert(ind,word1)
			#words.insert(ind,word2)
			continue
		elif(',' in word):
			#fix comma
			words.remove(word)
			word = word[:-1]
			words.insert(ind,word)
		ind = ind + 1

	emptyList = list()
	#Don't bother returning anything important since these verbs aren't there
	if 'is' not in words and 'are' not in words and 'refer' not in words and 'refers' not in words and 'consist' not in words and 'consists' not in words and 'was' not in words and 'has' not in words:
		return emptyList		
	for i in range(len(words)):
		if(i <= 25):
			ind1 = words[i].find('(')
			ind2 = words[i].find(')')
			if(ind1 != -1 and ind2 != -1):
				continue
				#nouns.append(words[i][ind1+1:ind2])
			else:
				nouns.append(words[i].strip())
	#Return 1 word and 2 word phrases since some nouns in terms to gather table are 2 words
	if(len(words) > 2):
		for i in range(len(words) - 1):
			if(i <= 25):
				nouns.append(words[i].strip() + " " + words[i+1].strip())
	return nouns

#Return's ID or -1 if title matches term
def database_match(article_title,nodes):
	''' Determine if a Wikipedia article title is already in the database
		Args:
			article_title: title to check
		Returns:
			String ID if in database, '-1' if not
	'''
	#First load the terms
	for i in range(len(nodes)):
		if(nodes[i].name.lower().strip() == article_title.lower().strip()):
			return str(nodes[i].ID)
	return '-1';
def database_lookup(id, nodes):
	''' Get's the name of the node with the given ID
		Args:
			id: database id
		Returns:
			Name of node, or 'Not found'
	'''
	for i in range(len(nodes)):
		if nodes[i].ID == str(id):
			return nodes[i].name
	return 'Not found'

def is_cluster(id,nodes):
	''' Determine if the given id is a cluster
		Args:
			id: database id to check
		Returns:
			True if is cluster, False if not
	'''
	for i in range(len(nodes)):
		if nodes[i].ID == str(id):
			return nodes[i].isCluster
	return False
def csv_match(article_title):
	''' Determine if a Wikipedia article title matches any created node in the CSV file
		Args:
			article_title: title to check
		Returns:
			string id of node if matches created node, or '-1'
	'''
	with open(created_CSV_file,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			if(str(row[0]) == 'CN'):
				database_id = str(row[1])
				title = row[2]
				if article_title.lower() == title.lower():
					return database_id
	return '-1'

def create_link(columnB,columnC,isCluster, otherTitle,database_nodes):
	''' Adds a link between 2 nodes to the CSV file
		Args:
			columnB: ID from database or csv that categorizes the column C node
			columnC: ID from database that is categorized by the column B node
			isCluster: Whether the column B node is a cluster
			otherTitle: Noun/Title being used to verify accuracy
	'''
	if(not (linkExistsInCSV(columnB,columnC))):
		with open(created_CSV_file, 'a+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			if isCluster:
				writer.writerow(['CL',str(columnB),str(columnC),'is categorised as','categorises',str(database_lookup(columnB,database_nodes)),str(otherTitle)])
			else:
				writer.writerow(['CL',str(columnB),str(columnC),'is related to','is related to',str(database_lookup(columnB,database_nodes)),str(otherTitle)])
def create_node(ID,title,description,noun,url):
	''' Creates a node with given ID in the CSV file
		Args:
			ID: ID of node to create
			title: name of node to create
			descrption: paragraph of node from Wikipedia article
			noun: noun being used to categorize to help verify accuracy
			url: url of Wikipedia article to help verify accuracy
		Returns:
			True if node is created, False if node already has been created
	'''
	if(csv_match(title) == '-1'): #Node not already in CSV
		with open(created_CSV_file, 'a+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			writer.writerow(['CN',str(ID),title,'description',description,"reference",str(url)])
			return True
	else:
		print(title + " already exists " + str(ID))
		return False
def linkExistsInCSV(columnB,columnC):
	''' Determine if a link between 2 nodes already exists
		Args:
			columnB: 2nd column of CSV file ID - used to categorize the columnC node
			columnC: 3rd column of CSV file ID - is categorized by the columnB node
		Returns:
			True if link exists, False is it doesn't
	'''
	with open(created_CSV_file,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			if(str(row[0]) == 'CL'):
				b = str(row[1])
				c = str(row[2])
				if b == columnB and c == columnC:
					return True
	return False
def loadDatabase():
	nodes = list()
	with open(database, 'r+') as f:
		data = json.load(f)
		for i in range(len(data)):
			database_id = str(data[i]['_key'])
			isCluster = False
			if(data[i].get('cl') != None):
				cluster = data[i].get('cl')
				if cluster == 'true' or cluster == "TRUE":
					isCluster = True
			value = str(data[i]['t'])
			nodes.append(Node(value,database_id,isCluster))
	return nodes


def main():
	#Load some things that may be needed later
	myTime = time.time()
	avoid_terms = loadAvoidTerms()
	gather_terms = loadGatherTerms()
	avoid_categories = loadAvoidCategories()
	every_ever_category = []
	urls = list()
	database_nodes = loadDatabase()
	#create files so that they exist
	file = open(created_CSV_file, 'w+')
	file.close()
	file2 = open(category_file, 'w+')
	file2.close()
	#Prompt user for category url to start at
	start_category = str(getURL())
	#Default layer of AI is 0
	init_layer = 0
	cat_num = 1

	#Build Category array - contains all categories. Will be used to get all URLs
	category_name = start_category[start_category.find('Category:')+9:].strip().replace("_"," ").lower()
	new_urls, sub_categories = getLinksFromCategoryPage(start_category)
	every_ever_category.append(Category(category_name,start_category,sub_categories,new_urls,init_layer,cat_num))
	with open(category_file,'r+') as f:
		for current_category in every_ever_category:
			#Don't want to go too far past AI
			if(current_category.level >= 3):
				continue
			else:
				for sub in current_category.sub_categories:
					category_name = str(sub[sub.find('Category:')+9:]).strip().replace("_"," ").lower()
					if(not validCategoryName(category_name,avoid_categories)):
						continue
					next_urls, next_categories = getLinksFromCategoryPage(sub)
					layer = current_category.level + 1
					append = True
					if(len(next_urls) == 0 and len(next_categories) == 0):
						continue
					elif(len(next_urls) == 0 and layer == 3):
						continue
					#Check if category already appended -> don't want to append twice
					for cat in every_ever_category:
						if cat.name == category_name:
							append = False
							break
					if(append):
						cat_num = cat_num + 1	
						every_ever_category.append(Category(category_name,sub,next_categories,next_urls,layer,cat_num))
						f.write(category_name + "\n")
						print category_name, layer,cat_num
	f.close()
	#Load list of urls
	for current_category in every_ever_category:
		category_urls = current_category.linked_pages
		for url in category_urls:
			urls.append(url)
	print len(every_ever_category)
	#Start scraping a certain page
	for i in every_ever_category:
		print "Category:" + i.name + " has " + str(len(i.linked_pages)) + " pages "
	#No longer needed, trying to save memory since there were some issues when running on the entire thing
	del every_ever_category

	id_count = 1
	num_invalid = 0
	length = len(urls)
	count = 0.0
	for url in urls:
		print url, id_count
		count = count + 1
		if (count % 50 == 0):
			print (count * 100 / length, '%')
		soup = getHTML(url)
		if(soup == None):
			continue
		#Don't bother if is stub
		if(isStub(soup)):
			print(url," is stub\n")
			continue
		#get title and first paragraph
		article_title = getTitle(soup)
		if article_title == 'Error':
			continue
		paragraph = ""
		titles_in_paragraph = list()
		every = soup.find('div',{'class': 'mw-parser-output'})
		if every == None:
			print("Error on: ",url)
			continue
		else:
			every = every.findAll('p')
		#Don't know which paragraph is actual - most likely 1st or 2nd
		for p in every:
			potentialParagraph = extractTextFromParagraph(p)
			titles_in_paragraph = extractLinksFromParagraph(p)
			#If the title is in the paragraph, then it is most likely legitimate
			if article_title.lower() in potentialParagraph.lower():
				paragraph = potentialParagraph
				break
			elif '(' in article_title and ')' in article_title:
				if(article_title[:article_title.find('(')].strip().lower() in potentialParagraph.lower()):
					paragraph = potentialParagraph
					break
			else:
				flag = False
				all_words = splitAndLower(article_title)
				for w in all_words:
					if not flag and w.lower().strip() in potentialParagraph.lower():
						paragraph = potentialParagraph
						flag = True
				if flag:
					break
		#Really annoying if there's latex in the paragraph, so just skipping those pages
		if('{\displaystyle' in paragraph or 'alt=' in paragraph):
			paragraph = ""
			titles_in_paragraph = list()
		#Determine if the article title is already in the database
		database_id = database_match(article_title,database_nodes)
		node_created = False
		valid_title = True #If in database it is a valid title
		if database_id == '-1':
			#If the title is valid, we should try creating a node
			if validArticleTitle(article_title,avoid_terms,gather_terms) and len(paragraph) > 0:
				valid_title = True
				database_id = str(id_count)
			else:
				num_invalid = num_invalid + 1
				valid_title = False
		else:
			node_created = True
		#Attempt to create and categorize a node if the title is valid
		if(valid_title):
			firstNouns = getPotentialFirstNoun(paragraph, article_title)
			valid_noun = False
			appeared = False
			detected_noun = ""
			invalid_nouns = ['information','field','extraction','vocabulary','corpus','translation','programming','software','tree','system','data','technology',
							 'framework','language','device','network','actvity','branch','approaches','business','way','area','domain','robot','study','studies'
							 'use','university','college','interface']
			#Try to categorize by paragraph nouns
			if(not valid_noun):
				num_words_to_look_at = 6
				noun_index = 0
				#Attempt to categorize by noun and terms to gather table
				for index, noun in enumerate(firstNouns):
					noun = ' ' + str(noun).strip() + ' '
					if not appeared and noun == ' is ' or noun == ' are ' or noun == ' refer ' or noun == ' refers ' or noun == ' consist ' or noun == ' consists ' or noun == 'was' or noun == ' has ':
						appeared = True
						detected_noun = noun.strip()
						noun_index = index
					noun = noun.strip()
					#Don't care about 'was'
					if appeared and detected_noun == 'was':
						appeared = False
						print("skipping since doesn't exist anymore")
						break
					#Skipping these for now
					if appeared and noun == 'metric' or noun == 'measurement' or noun == 'measure':
						appeared = False
						print("skipping since type of metric/measurement/measure")
						break
					#Valid, can exist loop
					if appeared:
						break
				#Look at first nouns from the index after the verb was detected
				noun_subset = firstNouns[noun_index:]
				if(len(noun_subset) > num_words_to_look_at):
					noun_subset = noun_subset[:num_words_to_look_at + 1]
				#Valid verb, so look for the noun
				if(appeared):
					for index in range(len(noun_subset)-1):
						bigNoun = False
						#Check what the next word is classified as -> helps make 2 word terms to gather work as well as ensure things like 'software company' are classified as company
						noun = noun_subset[index].lower().strip()
						next_noun = noun_subset[index+1].lower().strip()
						#2 word match
						if((noun + ' ' + next_noun) in gather_terms):
							noun = noun + ' ' + next_noun
							bigNoun = True
						if not bigNoun:
							if(next_noun in gather_terms and index != len(noun_subset)-2):
								continue
							elif(next_noun in gather_terms and index == len(noun_subset)-2):
								if(firstNouns[noun_index+index+2] in gather_terms):
									noun = firstNouns[noun_index+index+2]
								else:
									noun = next_noun
						if noun in gather_terms and not valid_noun and appeared:
							#Create node if it doesn't exist
							if(not node_created):
								database_id = str(id_count)
								modifyID = create_node(database_id,article_title,paragraph,noun,url)
								if(modifyID):
									id_count = id_count + 1
								else:
									database_id = csv_match(article_title)
								node_created = True
							#Create link if node exists
							if(node_created):
								term_id = gather_terms[noun]
								isCluster = is_cluster(term_id,database_nodes)
								create_link(term_id,database_id,isCluster,noun,database_nodes)
								valid_noun = True				 
			#If can't categorize by noun, attempt to categorize by title if there is only one capital in the word. Don't categorize by title if the noun is in invalid_nouns
			if(not valid_noun and not node_created and numCapitalsInTitle(article_title) <= 1):
				words_in_title = article_title.split(" ")
				for title_word in words_in_title:
					#Ignore '(' and ')' in title
					if('(' in title_word and ')' in title_word):
						title_word = title_word[title_word.find('(')+1:title_word.find(')')]
					#Ignore "was company" or "was software company" as they no longer exist
					if(not('was' in firstNouns and 'company' in firstNouns)):
						if title_word.lower() in gather_terms and title_word.lower() not in invalid_nouns and title_word.lower()[:-1] not in invalid_nouns:
							t_id = gather_terms[title_word.lower()]
							#Create a node if node does not exist
							if(not node_created):
								modifyID = create_node(database_id,article_title,paragraph,title_word.lower(),url)
								if(modifyID):
									id_count = id_count + 1
								else:
									database_id = csv_match(article_title)
								node_created = True
							#Create a link if there is a node
							if(node_created):
								isCluster = is_cluster(t_id,database_nodes)
								create_link(t_id,database_id,isCluster,title_word.lower(),database_nodes)
								valid_noun = True

			#Valid node and categorization -> Can look at see also, categories, and links in paragraph
			if(valid_noun and node_created):
				see_also_titles = extractSeeAlso(soup)
				#Node must either be in database or csv file now
				database_id = database_match(article_title,database_nodes)
				if(database_id == '-1'):
					database_id = csv_match(article_title)

				#Check for matches with see also titles
				for title in see_also_titles:
					title_id = database_match(title,database_nodes)
					if (title_id != '-1' and title_id != database_id):
						isCluster = is_cluster(title_id,database_nodes)
						create_link(title_id,database_id,isCluster,title,database_nodes)

					csv_id = csv_match(title)
					if(csv_id != '-1' and csv_id != database_id):
						create_link(csv_id,database_id,False,title,database_nodes) #Anything in the CSV is guaranteed to not be in the database and not be a cluster
				#Check for matches with categories at bottom of Wikipedia article
				category_titles = extractCategories(soup)
				for title in category_titles:
					title_id = str(database_match(title,database_nodes))
					if (title_id != '-1' and title_id != database_id):
						isCluster = is_cluster(title_id,database_nodes)
						create_link(title_id,database_id,isCluster,title,database_nodes)

					csv_id = csv_match(title)
					if(csv_id != '-1' and csv_id != database_id):
						create_link(csv_id,database_id,False,title,database_nodes) #Anything in the CSV is guaranteed to not be in the database and not be a cluster
				#Check for matches with links in first paragraph
				for title in titles_in_paragraph:
					title_id = str(database_match(title,database_nodes))
					if (title_id != '-1' and title_id != database_id):
						isCluster = is_cluster(title_id,database_nodes)
						create_link(title_id,database_id,isCluster,title,database_nodes)

					csv_id = csv_match(title)
					if(csv_id != '-1' and csv_id != database_id):
						create_link(csv_id,database_id,False,title,database_nodes) #Anything in the CSV is guaranteed to not be in the database and not be a cluster
	print("Created: " + created_CSV_file)
	print(str(id_count) + " nodes, " + str(num_invalid) + " invalid titles")
	time2 = time.time()
	print(str((time2-myTime)/60) + " minutes to run")
if __name__ == '__main__':
	main()