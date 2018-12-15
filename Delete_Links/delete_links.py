import csv
import requests
import sys
import json
import codecs
import pandas as pd
import sqlite3
from sqlite3 import Error

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
	deleteTable()
	with open(links_file,'r+') as f:
		data = json.load(f)

		sql = sqlite3.connect(str(database))
		cur = sql.cursor()
		#Create the data table
		cur.execute('''CREATE TABLE IF NOT EXISTS data(link1 TEXT, link2 TEXT, link_id TEXT)''')

		for i in range(len(data)):
			key1 = str(data[i]['_from'])
			id_1 = key1[6:]
			key2 = str(data[i]['_to'])
			id_2 = key2[6:]
			key3 = str(data[i]['_key'])
			cur.execute('''INSERT INTO data VALUES(?,?,?)''',(id_1,id_2,key3))
		f.close()
		sql.commit()
		sql.close()

def verify(link1,link2,numExpected):
	queryString = "SELECT * FROM data WHERE link1=" + link1 + " AND link2=" + link2
	try:
		conn = sqlite3.connect(str(database))
		cursor = conn.cursor()
		cursor.execute(queryString);
		all_rows = cursor.fetchall()

		if(len(all_rows)) == numExpected:
			return True, len(all_rows)
	except Error as e:
		print(e)
	finally:
		conn.close()

	return False, len(all_rows)
def getID(link1,link2):
	queryString = "SELECT * FROM data WHERE link1=" + link1 + " AND link2=" + link2
	try:
		conn = sqlite3.connect(str(database))
		cursor = conn.cursor()
		cursor.execute(queryString);
		all_rows = cursor.fetchall()
		return all_rows[0][2]
	except Error as e:
		print(e)
	finally:
		conn.close()

	return -1;

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("USAGE: python delete_links.py [Input JSON Links File] [Name of output csv file]")
		print("If there is a space in any of the files, put the name in quotes \"[NAME]\" ")
		print("Example: python link_recursion.py \"All links.json\" output.csv ")
	else:
		links_file = sys.argv[1]#'All links.json'
		created_CSV_file = sys.argv[2]#'output_All deleted.csv'
		#links = load_links()
		loadDatabase(links_file)
		full_links = pd.read_json(links_file)
		full_links['_from'].apply(str)
		full_links['_to'].apply(str)
		full_links['_from'] = (full_links['_from'].str.extract('(\d+)'))
		full_links['_to'] = (full_links['_to'].str.extract('(\d+)'))

		links = pd.concat([full_links['_from'],full_links['_to']],axis=1)

		print links.head()
		links = links[links.duplicated(keep=False)]

		df1 = (links.groupby(links.columns.tolist())
		       .apply(lambda x: tuple(x.index))
		       .reset_index(name='idx'))

		count = 0.0
		length = len(df1)
		with open(created_CSV_file, 'w+') as csvfile:
			writer = csv.writer(csvfile,lineterminator = '\n')
			print df1
			for index, row in df1.iterrows():
				count = count + 1
				if (count % 100 == 0):
					print (count * 100 / length, '%')
				correct, actual = verify(row['_from'],row['_to'],len(row['idx']))
				link_id = getID(row['_from'],row['_to'])
				if correct:
					writer.writerow(['DL',str(link_id)])#str(row['_from']),str(row['_to'])])
					continue
				else:
					print row['_from'], row['_to'], len(row['idx']), actual