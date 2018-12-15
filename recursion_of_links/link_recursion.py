import csv
import requests
from BeautifulSoup import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Link:
	def __init__(self, id1, id2):
		self.id1 = id1
		self.id2 = id2
def load_nodes(nodes_file):
	nodes = list()
	with open(nodes_file) as f:
		data = json.load(f)
		for i in range(len(data)):
			a_id = str(data[i]['_key'])
			name = str(data[i]['t'])
			cluster = "";
			if(data[i].get('cl') != None):
				cluster = data[i].get('cl')
			if(cluster == "TRUE"):
				continue
			if(data[i].get('a') == None or data[i]['a'].get('description') == None):
				definition = ""
			else:
				definition = str(data[i]['a']['description'])
			if(definition != "" and definition != "Enter a definition" and definition != "Add a definition"):
				nodes.append(Node(name,a_id,definition))
	return nodes
def load_links(links_file):
	links = list()
	with open(links_file,'r+') as f:
		data = json.load(f)
		for i in range(len(data)):
			key1 = str(data[i]['_from'])
			id_1 = key1[6:]
			key2 = str(data[i]['_to'])
			id_2 = key2[6:]
			links.append(Link(id_1,id_2))
	return links
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
def create_link(columnB,columnC, otherTitle):
	''' Adds a link between 2 nodes to the CSV file
		Args:
			columnB: ID from database or csv that categorizes the column C node
			columnC: ID from database that is categorized by the column B node
			otherTitle: Noun/Title being used to verify accuracy
	'''
	if(not (linkExistsInCSV(columnB,columnC))):
		with open(created_CSV_file, 'a+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			writer.writerow(['CL',str(columnB),str(columnC),'is related to','is related to'])
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
			if(len(row) > 0 and str(row[0]) == 'CL'):
				b = str(row[1])
				c = str(row[2])
				if b == columnB and c == columnC:
					return True
	return False
def link_exists(links, id_1, id_2):
	for link in links:
		if link.id1 == id_1 and link.id2 == id_2:
			return True
		elif link.id1 == id_2 and link.id2 == id_1:
			return True
	return False

def main():
	nodes_file = sys.argv[1]
	links_file = sys.argv[2]
	created_CSV_file = sys.argv[3]
	
	links = load_links(links_file)
	nodes = load_nodes(nodes_file)

	start_url = 'https://en.wikipedia.org/wiki/'
	length = len(nodes)
	count = 0.0
	for title, ID in nodes.iteritems():
		#print progress
		count = count + 1
		if (count % 25 == 0):
			print (count * 100 / length, '%')

		url = start_url + title;

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
		print url
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
		if('{\displaystyle' in paragraph or 'alt=' in paragraph):
			paragraph = ""
			titles_in_paragraph = list()

		#Check for matches with see also titles
		csv_id = ID
		see_also_titles = extractSeeAlso(soup)
		for title in see_also_titles:
			database_id = nodes.get(title)
			if(database_id != None and csv_id != database_id and not link_exists(links,csv_id,database_id)):
				create_link(csv_id,database_id,title) #Anything in the CSV is guaranteed to not be in the database and not be a cluster
		#Check for matches with categories at bottom of Wikipedia article
		category_titles = extractCategories(soup)
		for title in category_titles:
			database_id = nodes.get(title)
			if(database_id != None and csv_id != database_id and not link_exists(links,csv_id,database_id)):
				create_link(csv_id,database_id,title) #Anything in the CSV is guaranteed to not be in the database and not be a cluster
		#Check for matches with links in first paragraph
		for title in titles_in_paragraph:
			database_id = nodes.get(title)
			if(database_id != None and csv_id != database_id and not link_exists(links,csv_id,database_id)):
				print(csv_id,database_id,title)
				create_link(csv_id,database_id,title) #Anything in the CSV is guaranteed to not be in the database and not be a cluster		
if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("USAGE: python link_recursion.py [Input JSON Nodes File] [Input JSON Links File] [Name of output csv file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python link_recursion.py \"All nodes.json\" \"All links.json\" output.csv ")
	else:
		main()