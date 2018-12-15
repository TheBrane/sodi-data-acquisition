import requests
import csv
from BeautifulSoup import *
import sys
import codecs
import re
import time
import operator
import json

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def loadNodes(nodes_file):
	''' Loads a dictionary of nodes from the backup file
		Returns:
			dictionary where key is name and value is string ID
	'''
	nodes = dict()
	with open(nodes_file,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			a_id = str(row[0])
			name = str(row[4])
			nodes[name] = a_id
	return nodes
def loadNodesJSON(nodes_file):
	nodes = dict()
	with open(nodes_file) as f:
		data = json.load(f)
		for i in range(len(data)):
			a_id = str(data[i]['_key'])
			name = str(data[i]['t'])
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

def output_node(ID,url,author,date,license):
	with open(created_CSV_file, 'a+') as csvfile:
		writer = csv.writer(csvfile,lineterminator = '\n')
		if(author != "" and date != "" and license != ""):
			writer.writerow(['UI',str(ID),'image',url,"authorname",author,"date",date,"license",license])
		elif(author != "" and date != "" and license == ""):
			writer.writerow(['UI',str(ID),'image',url,"authorname",author,"date",date])
		elif(author != "" and date == "" and license == ""):
			writer.writerow(['UI',str(ID),'image',url,"authorname",author])
		elif(author != "" and date == "" and license != ""):
			writer.writerow(['UI',str(ID),'image',url,"authorname",author,"license",license])
		elif(author == "" and date == "" and license != ""):
			writer.writerow(['UI',str(ID),'image',url,"license",license])
		elif(author == "" and date != "" and license != ""):
			writer.writerow(['UI',str(ID),'image',url,"date",date,"license",license])
		elif(author == "" and date != "" and license == ""):
			writer.writerow(['UI',str(ID),'image',url,"date",date])
		else:
			writer.writerow(['UI',str(ID),'image',url])
def output_url(url):
	url = '<img src="' + url + '">'
	fh = open(created_html_file, "a+")
 	fh.write(url+'\n')
	fh.close()

def parseText(text):
	i = 0
	txt = ""
	text = str(text)
	while i < len(text):
		if(ord(text[i]) < 128):
			if(text[i] == '<'):
				while(text[i] != '>'):
					i = i + 1
			else:
				txt = txt + text[i]
		i = i + 1
	return txt.replace("  ", " ")

def validTime(time):
	times = time.split(" ")
	if(len(times) != 3):
		return False
	date = times[0]
	if(not(date.isdigit() and int(date) >= 1 and int(date) <= 31)):
		return False
	month = times[1]
	if(month != 'January' and month != 'February' and month != 'March' and month !='April' and month != "May" and month != "June" and month != "July" and month != "August" and month != "September" and month != "October" and month != "November" and month != "December"):
		return False
	year = times[2]
	if(not(year.isdigit())):
		return False
	return True

if __name__ == '__main__':
	if(len(sys.argv) != 4):
		print("USAGE: python image_scraper.py [Input JSON File] [Name of output csv file] [Name of output html file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python image_scraper.py \"ALL NODES - 06-10-2018.json\" images.csv files.html")
	else:
		#input file
		nodes_file = sys.argv[1]#'ALL NODES_ALL.csv'
		#output file
		created_CSV_file = sys.argv[2]#'images.csv'
		created_html_file = sys.argv[3]#'files.html'

		nodes = loadNodesJSON(nodes_file)
		start_url = 'https://en.wikipedia.org/wiki'
		count = 0.0

		invalidImages = ['Disambig_gray.svg','Question_book-new.svg','Commons-logo.svg','Antique-books-woodward.jpg','Edit-clear.svg','Wikisource-logo.svg','Wiki_letter_w.svg','Wiki_letter_w_cropped.svg']

		with open(created_CSV_file, 'w+') as csvfile:
			length = len(nodes)
			writer = csv.writer(csvfile,lineterminator = '\n')
			for title,a_id in nodes.iteritems():
				#print progress
				count = count + 1
				if (count % 25 == 0):
					print (count * 100 / length, '%')
				#query wikipedia
				url = start_url + "/" + title
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
				every = soup.find('div',{'class': 'mw-parser-output'})
				if every == None:
					continue	

				imageExists = False
				imageURL = start_url
				for p in soup.findAll('a',{'class': 'image'}):
					#if("CentralAutoLogin" in str(p.get('src')) or 'wikimedia-button' in str(p.get('src')) or 'poweredby_mediawiki' in str(p.get('src'))):
					#	continue
					#https://en.wikipedia.org/wiki/File:SerraEstrela-MAR2007-5.jpg is what I want
					#
					#print url, p.get('src')
					imageURL = start_url + str(p.get('href'))[5:]
					skip = False
					for invalid in invalidImages:
						if invalid in imageURL:
							skip = True
					if skip:
						continue
					else:
						imageExists = True
						break
				if(imageExists):
					hasTime = False
					hasAuthor = False
					hasLicense = False
					time = ""
					author = ""
					license = ""

					image_soup = getHTML(imageURL)

					
					#print soup.findAll('div',{'class': 'mw-parser-output'})
					#print image_soup.find('div',{'class': 'hproduct commons-file-information-table'})
					a = image_soup.find('td',{'id':'fileinfotpl_aut'})
					if(a != None):
						hasAuthor = True
					if(hasAuthor):
						characters = a.findNext('td')
						if(characters.find('a') != None):
							characters = str(characters.find('a').text)
						else:
							characters = str(characters)
							#print characters
							x = characters.find('>')
							y = characters.find('<',x)
							if(characters != "" and y != -1 and x != -1):
								characters = characters[x+1:y]
						if('.svg' in characters or '.png' in characters or ('[' in characters and ']' in characters)):
							author = ""
						else:
							author = characters
					a = image_soup.find('td',{'id':'fileinfotpl_date'})
					if(a != None):
						hasTime = True
					if(hasTime):
						imageTime = image_soup.find('time',{'class':'dtstart'})
						if(imageTime == None):
							characters = str(a.findNext('td'))
							x = characters.find('>')
							y = characters.find('<',x)
							if(characters != "" and y != -1 and x != -1):
								characters = characters[x+1:y]
								imageTime = characters.strip()
						else:
							characters = str(imageTime)
							x = characters.find('>')
							y = characters.find('<',x)
							imageTime = characters[x+1:y].strip()

						if(',' in imageTime):
							imageTime = imageTime[:imageTime.find(',')]
						if(len(imageTime.split(" ")) == 2):
							imageTime = "1 " + imageTime
						if(imageTime != "" and len(imageTime.split(" ")) != 3):
							imageTime = "1 January " + imageTime
						if(validTime(imageTime)):
							time = imageTime.strip()

					table = image_soup.find('table')
					i = 0
					for td in table.findChildren('td'):
						#skip first element
						if i == 0:
							i = 1
							continue
						if('Wikimedia Commons' in str(td.text)):
							license = "Wikimedia Commons"
					if(license == ""):
						table2 = image_soup.find('table',{'class': 'layouttemplate licensetpl mw-content-ltr'})
						if(table2 == None):
							table3 = image_soup.find('table',{'class': 'toccolours licensetpl fileinfotpl fileinfotpl-type-fairuse'})
							if(table.find('th') != None):
								license = parseText(table.find('th')).strip()
						else:
							license = "Creative Commons"

					other_images = image_soup.findAll('span',{'class':'mw-filepage-other-resolutions'})
					print imageURL
					for span in other_images:
						links = span.findAll('a')
						imageURL = 'https:' + links[-1].get('href')
					output_node(a_id,imageURL,author,time,license)
					output_url(imageURL)