import csv
import requests
from BeautifulSoup import *
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Link:
	def __init__(self, id1, id2):
		self.id1 = id1
		self.id2 = id2
class Node:
	def __init__(self,name,ID,definition):
		self.name = name
		self.ID = ID
		self.definition = definition
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
def link_exists(id_1,id_2):
	for link in links:
		if link.id1 == id_1 and link.id2 == id_2:
			return True
		elif link.id1 == id_2 and link.id2 == id_1:
			return True
	return False
def valid_exceptions():
	nodes = dict()
	with open(exceptions_file,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			a_id = str(row[0])
			name = str(row[1])
			nodes[name] = a_id
	return nodes

if __name__ == '__main__':
	if(len(sys.argv) != 5):
		print("USAGE: python node_recursion.py [Input JSON Nodes File] [Input JSON Links File] [Name of exceptions CSV file] [Name of output csv file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python node_recursion.py \"All nodes.json\" \"All links.json\" exceptions.csv output.csv ")
	else:
		nodes_file = sys.argv[1]#'All nodes.json'
		links_file = sys.argv[2]#'All links.json'
		exceptions_file = sys.argv[3]#"exceptions.csv"
		created_CSV_file = sys.argv[4]#'output_All nodes.csv'
		nodes = load_nodes(nodes_file)
		links = load_links(links_file)
		
		valid_nodes = valid_exceptions()
		invalid_ids = ['84863573', '84863703','85165547','84865090','84873582','84865696','84863588','84863730','84864590','85166489','84878834','84863710','84864681','85170352','85165586','84867280','85165549','85165556','85165553','85165563','84873191','85165548','85165570']
		with open(created_CSV_file, 'w+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			count = 0.0
			length = len(nodes)

			for temp in nodes:
				node_name = temp.name
				node_ID = temp.ID
				node_def = temp.definition.lower()

				count = count + 1
				if (count % 25 == 0):
					print (count * 100 / length, '%')

				if(node_ID not in invalid_ids):
					for temp2 in nodes:
						if(temp2 != temp):
							a = temp2.name
							if(len(a.split(" ")) < 2 and a not in valid_nodes):
								continue
							a = a.lower()
							if(temp2.ID not in invalid_ids and (" " + temp2.name.lower() + " ") in node_def and not link_exists(node_ID,temp2.ID)):
								#print temp2.name, node_def
								writer.writerow(['CL',str(node_ID),str(temp2.ID),'is related to','is related to',temp2.name,temp.definition])
								#print 'CN',str(node_ID),str(temp2.ID),'is related to','is related to'
				else:
					print "Invalid"