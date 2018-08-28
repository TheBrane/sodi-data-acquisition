'''Kaushik Tandon
   This program scrapes Wikipedia articles given a csv file of article titles. For each node, this script gets the url
   and the first paragraph of the article. It creates a csv file with the updated nodes.
'''
import csv
from BeautifulSoup import *
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

#input file
august_nodes_file = 'august_backup.csv' #backup file containing ID in first column and name of node in second column
#output file
created_CSV_file = 'fixed.csv' #file that is created

def loadNodes():
	''' Loads a dictionary of nodes from the backup file
		Returns:
			dictionary where key is name and value is string ID
	'''
	nodes = dict()
	with open(august_nodes_file,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			a_id = str(row[0])
			name = str(row[1])
			nodes[name] = a_id
	return nodes

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

#This is needed since the getText() method in beautiful soup returns some messy data here. Trying to recognize weird characters as well
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
	return string.replace("--","").strip()
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

august_nodes = loadNodes()
start_url = 'https://en.wikipedia.org/wiki/'
count = 0.0
with open(created_CSV_file, 'w+') as csvfile:
	length = len(august_nodes)
	writer = csv.writer(csvfile,lineterminator = '\n')

	for title,a_id in august_nodes.iteritems():
		#print progress
		count = count + 1
		if (count % 25 == 0):
			print (count * 100 / length, '%')
		#change ? to -
		if('?' in title):
			title = title.replace("?","-")
		#query wikipedia
		url = start_url + title
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
			continue
		else:
			every = every.findAll('p')

		for p in every:
			potentialParagraph = extractTextFromParagraph(p).encode('utf-8')
			
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
		#This node needs to be updated
		if paragraph != "":
			print url
			#print("UN,"+str(a_id)+","+str(article_title)+ ",description," + paragraph.encode('utf-8') + "," + url)
			writer.writerow(['UN',str(a_id),str(article_title),'description',paragraph,url])
