import json
import csv
import numpy as np
import pandas as pd

def main():
	# Create list of topics
	new_topics = list()
	new_links = list()

	# Load and clean the data
	data = pd.read_csv("data.csv")
	data = data.fillna('')
	# Starting at key value T24 for topics
	topic_key_val = 24
	# Starting at key value L23 for links
	link_key_val = 23
	for rowidx in range(len(data)):
		# Get current row in dataset
		publication_row = data.iloc[rowidx,:]
		issn = publication_row['SN']
		electronic_issn = publication_row['EI']
		isbn = publication_row['BN']
		_type = "publication"
		# Determine which columns to read based off value of ISBN
		if (isbn == ""):
			topic_title = publication_row['SO'].title()
			terms = [topic_title, publication_row['J9'].title(), publication_row['JI'].title()]
			conference_proceeding = False
		else:
			topic_title = publication_row['SE'].title()
			terms = [topic_title, publication_row['J9'].title()]
			conference_proceeding = True

		# Look for duplicates
		duplicate = False
		for topic in new_topics:
			if topic['title'] == topic_title:
				# If the ISSN or ISBN match, assuming there is data, then this is a duplicate
				if (topic['ISBN'] == isbn and isbn != "") or (topic['ISSN'] == issn and issn != ""):
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					duplicate = True
				# No data for issn/isbn but electronic issn matches
				elif (isbn == '' and issn == '' and topic['Electronic_ISSN'] == electronic_issn):
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					duplicate = True
		# Skip making a topic for this publication
		if (duplicate):
			continue

		topic_key = 'T' + str(topic_key_val)
		# Increment key value for next topic
		topic_key_val = topic_key_val + 1

		# Output topic to JSON format
		topic_json_struct = {}
		topic_json_struct['_key'] = topic_key
		topic_json_struct["_type"] = _type
		topic_json_struct['title'] = topic_title
		topic_json_struct['terms'] = terms
		topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)
		topic_json_struct['ISSN'] = issn
		topic_json_struct['Electronic_ISSN'] = electronic_issn
		topic_json_struct['ISBN'] = isbn

		# Store in list to output at end
		new_topics.append(topic_json_struct)

		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1

		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'hasSubclass'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = 'T12' if conference_proceeding else 'T11' 
		link_json_struct['_to'] = topic_key

		# Store in list to output at end
		new_links.append(link_json_struct)

	# Output topics to file
	with open('output/publication_topics.json', 'w') as f:
		# There's probably a better way to output as a list of JSON objects
		f.write('[')
		i = 0
		for topic in new_topics:
			f.write(json.dumps(topic))
			if i != len(new_topics) - 1:
				f.write(",\n")
			else:
				f.write('\n')
			i = i + 1
		f.write(']')
	# Output links to file
	with open('output/publication_links.json', 'w') as f:
		f.write('[')
		i = 0
		for link in new_links:
			f.write(json.dumps(link))
			if i != len(new_topics) - 1:
				f.write(",\n")
			else:
				f.write('\n')
			i = i + 1
		f.write(']')
if __name__ == '__main__':
	main()