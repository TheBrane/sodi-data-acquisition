import json
import csv
import numpy as np
import pandas as pd

def parse_author(author):
	# The form is LastName, FirstName or LastName, FirstName Middle
	# The middle name will remain part of the first name
	author = author.strip()
	last_name = author.split(',')[0].strip().title()
	first_name = author.split(",")[1].strip().title()
	return first_name, last_name

def form_author_name(first_name, last_name):
	return first_name + " " + last_name

def parse_orcid_id(row, authors):
	orcidIDs = dict()
	if (row == ''):
		return orcidIDs
	# First check for /xxxx-xxxx-xxxx-xxxx versus lastName, firstName/xxxx-xxxx-xxxx-xxxx
	if row[0] == '/':
		# In this case, we need the author name. I will assume it is the first, and hopefully only, author
		first_name, last_name = parse_author(authors[0])
		author = form_author_name(first_name, last_name)
		orcid_id = row[1:]
		orcidIDs[author] = orcid_id
	else:
		# If there is more than one, they will be separated by ;.
		if (row.find(';') == -1):
			# Only one orcidId
			reversed_author = parse_author(row[:row.find('/')])
			author = form_author_name(reversed_author[0], reversed_author[1])

			orcid_id = row[row.find('/') + 1:]
			# print(row, author, orcid_id)
			orcidIDs[author] = orcid_id
		else:
			# There are multiple
			elements = row.split(';')
			for element in elements:
				if (element != '' and element.find(',') != -1):
					reversed_author = parse_author(element[:element.find('/')])
					author = form_author_name(reversed_author[0], reversed_author[1])

					orcid_id = element[element.find('/') + 1:]
					orcidIDs[author] = orcid_id

	return orcidIDs

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
		# Get the authors using the AF key
		authors = publication_row['AF'].split(";")
		reprint_address_last_name = publication_row['RP'].split(",")[0].title()
		orcidIDs = parse_orcid_id(publication_row['OI'], authors)
		for author in authors:
			# Check for incorrectly formatted name - very rare, but has to be done
			if (author.find(',') == -1):
				# Skip if no comma
				continue
			topic_key = 'T' + str(topic_key_val)
			# Increment key value for next topic
			topic_key_val = topic_key_val + 1

			first_name, last_name = parse_author(author)
			initials = first_name[0] + "." + last_name[0] + "."
			terms = [form_author_name(first_name, last_name), last_name, initials]
			title = form_author_name(first_name, last_name)

			if (last_name == reprint_address_last_name):
				email = publication_row['EM']
			else:
				email = ""

			orcid_id = orcidIDs.get(title)
			if (orcid_id == None):
				orcid_id = ''

			# Look for duplicates
			possible_duplicates = []
			duplicate = False
			for topic in new_topics:
				if topic['title'] == title:
					# If the orcid IDs match and we can't deduplicate
					if (topic['orcidID'] == orcid_id and orcid_id == ""):
						topic['Possible_Duplicates'].append(topic_key)
						possible_duplicates.append(topic['_key'])
					elif (topic['orcidID'] == orcid_id and orcid_id != ""):
						# This is a duplicate based on orcid id - we don't need to store it
						duplicate = True
			# Skip making a topic for this author
			if (duplicate):
				continue

			# Output topic to JSON format
			topic_json_struct = {}
			topic_json_struct['_key'] = topic_key
			topic_json_struct["_type"] = "individual"
			topic_json_struct['title'] = title
			topic_json_struct['terms'] = terms
			topic_json_struct['definition'] = ''
			topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)
			topic_json_struct['firstName'] = first_name
			topic_json_struct['lastName'] = last_name
			topic_json_struct['initials'] = initials
			topic_json_struct['email'] = email
			topic_json_struct['orcidID'] = orcid_id
			topic_json_struct['Possible_Duplicates'] = possible_duplicates

			# Store in list to output at end
			new_topics.append(topic_json_struct)

			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1

			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'hasInstance'
			link_json_struct['name'] = ''
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = 'T3'
			link_json_struct['_to'] = topic_key

			# Store in list to output at end
			new_links.append(link_json_struct)

	# Output topics to file
	with open('output/researcher_topics.json', 'w') as f:
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
	with open('output/researcher_links.json', 'w') as f:
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