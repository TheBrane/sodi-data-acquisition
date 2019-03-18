'''Recursive Densification of Nodes (3-gram)'''
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
	return nodes
def load_nodesJSON(nodes_file,title_split, invalid_ids):
	nodes = list()
	invalid_ids = set(invalid_ids)
	print ("Loading nodes")
	with open(nodes_file) as f:
		for line in f:

			data = json.loads(line)
			a_id = str(data['data']['_key'])
			name = str(data['data']['t'])
			if(name == ' ' or len(name.split(" ")) < title_split):
				continue

			cluster = ""
			if(data['data'].get('cl') != None):
				cluster = str(data['data'].get('cl'))
				if(cluster == "TRUE"):
					continue
			if(data['data'].get('a') == None or data['data']['a'].get('description') == None):
				definition = ""
			else:
				definition = str(data['data']['a']['description'])
			if(title_split != 0):
				if(invalid_ids != None and a_id not in invalid_ids):
					if(definition != "" and definition != " " and definition != "Enter a definition" and definition != "Add a definition"):
						nodes.append(Node(name,a_id,definition))
			else:
				if(invalid_ids != None and a_id not in invalid_ids):
					if(definition != "" and definition != " " and definition != "Enter a definition" and definition != "Add a definition"):
						nodes.append(Node(name,a_id,definition))	
				elif(invalid_ids == None):
					if(definition != "" and definition != " " and definition != "Enter a definition" and definition != "Add a definition"):
						nodes.append(Node(name,a_id,definition))
	print ("Loaded nodes")
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
def load_linksJSON(links_file):
	links = dict()
	with open(links_file, 'r+') as f:
		for line in f:
			data = json.loads(line)
			from_ = str(data['data']['_from'])[6:]
			to_ = str(data['data']['_to'])[6:]
			if(links.get(from_) == None):
				links[from_] = [to_]
			else:
				links[from_].append(to_)
	print("Loaded links")
	return links
def link_exists(id_1,id_2, links):
	links1 = links.get(id_1)
	links2 = links.get(id_2)
	if(links1 == None and links2 == None):
		return False
	elif links1 != None and links2 == None:
		if id_2 in links1:
			return True
		return False
	elif links1 == None and links2 != None:
		if(id_1 in links2):
			return True
		return False
	else:
		if(id_1 in links2):
			return True
		if id_2 in links1:
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

def loadList(fileName):
	ids = list()
	with open(fileName,'r+') as f:
		reader = csv.reader(f)
		for row in reader:
			if(len(row) == 1):
				a_id = str(row[0])
				ids.append(a_id)
	return ids

if __name__ == '__main__':
	if(len(sys.argv) != 4):
		print("USAGE: python node_recursion.py [Input JSON Nodes File] [Input JSON Links File] [Name of output csv file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python node_recursion.py \"All nodes.json\" \"All links.json\" output.csv ")
	else:
		nodes_file = sys.argv[1]#'All nodes.json'
		links_file = sys.argv[2]#'All links.json'
		#exceptions_file = sys.argv[3]#"exceptions.csv"
		created_CSV_file = sys.argv[3]#'output_All nodes.csv'
		invalid_ids = ['84863573', '84863703','85165547','84865090','84873582','84865696','84863588','84863730','84864590','85166489','84878834','84863710','84864681','85170352','85165586','84867280','85165549','85165556','85165553','85165563','84873191','85165548','85165570']
		nodes = load_nodesJSON(nodes_file,0, invalid_ids)
		links = load_linksJSON(links_file)
		
		#currently doing 2 gram
		x_gram = 2

		potential_nodes_to_link = load_nodesJSON(nodes_file,x_gram, invalid_ids)
		#valid_nodes = valid_exceptions()
		with open(created_CSV_file, 'w+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			count = 0.0
			length = len(nodes)
			print length, len(potential_nodes_to_link)
			for temp in nodes:
				node_name = temp.name
				node_ID = temp.ID
				node_def = temp.definition.lower()

				count = count + 1
				if (count % 25 == 0):
					print (count * 100 / length, '%')

				for temp2 in potential_nodes_to_link:
					if(temp2.ID != node_ID):
						a = temp2.name
						if(len(a.split(" ")) < x_gram):# and a not in valid_nodes): #Current doing 2 gram
							continue
						a = a.lower()
						if((" " + temp2.name.lower() + " ") in node_def and not link_exists(node_ID,temp2.ID,links)):
							#print temp2.name, node_def
							writer.writerow(['CL',str(node_ID),str(temp2.ID),'is related to','is related to',node_name,temp2.name])#,temp2.name,temp.definition])
							#print 'CN',str(node_ID),str(temp2.ID),'is related to','is related to'