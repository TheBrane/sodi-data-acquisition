import csv
import requests
import sys
import json
import codecs
import pandas as pd
import sqlite3
from sqlite3 import Error
import operator

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

database = 'links.db'

#only run if need to recreate table
def deleteTable():
	try:
		conn = sqlite3.connect(database)
		cursor = conn.cursor()
		cursor.execute("DROP TABLE data")
		conn.commit()
	except Error as e:
		print(e)
	finally:
		conn.close()
def loadDatabase(links_file):
	link_ids = dict()
	deleteTable()
	with open(links_file,'r+') as f:

		sql = sqlite3.connect(str(database))
		cur = sql.cursor()
		#Create the data table
		cur.execute('''CREATE TABLE IF NOT EXISTS data(link1 TEXT, link2 TEXT, link_id TEXT)''')

		numRows = 0
		for line in f:
			data = json.loads(line)
			key1 = str(data['data']['_from'])
			id_1 = key1[6:]
			key2 = str(data['data']['_to'])
			id_2 = key2[6:]
			key3 = str(data['data']['_key'])
			cur.execute('''INSERT INTO data VALUES(?,?,?)''',(id_1,id_2,key3))
			if((id_1,id_2) not in link_ids):
				link_ids[id_1,id_2] = 1
			else:
				link_ids[id_1,id_2] = link_ids[id_1,id_2] + 1
			numRows = numRows + 1
		f.close()
		sql.commit()
		sql.close()
	return numRows, link_ids

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("USAGE: python delete_links.py [Input JSON Links File] [Name of output csv file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python link_recursion.py \"All links.json\" output.csv ")
	else:
		links_file = sys.argv[1]#'All links.json'
		created_CSV_file = sys.argv[2]#'output_All deleted.csv'

		count = 0.0
		length, link_ids = loadDatabase(links_file)
		with open(created_CSV_file, 'w+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			sql = sqlite3.connect(str(database))
			cur = sql.cursor()
			for keyPair, value in link_ids.iteritems():
				count = count + 1
				if (count % 100 == 0):
					print (count * 100 / length, '%')
			
				if(value == 1): continue
				
				print keyPair
				try:
					queryString = "SELECT * FROM data WHERE link1=" + keyPair[0] + " AND link2=" + keyPair[1]
					cur.execute(queryString)
					all_rows = cur.fetchall()
					oneToKeep = True
					for row in all_rows:
						if(oneToKeep):
							oneToKeep = False
							continue
						else:
							link_id = str(row[2])
							writer.writerow(['DL',link_id])
				except Exception as e:
					print "Something weird happened"
					continue