import json
import csv
import numpy as np
import pandas as pd

# Protocol C main function to run
def convert_publications(data, topic_key_val, link_key_val):
	publication_topics = list()
	publication_links = list()

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
		for topic in publication_topics:
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
		publication_topics.append(topic_json_struct)

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
		publication_links.append(link_json_struct)
	return publication_topics, publication_links, topic_key_val, link_key_val
		
def parse_month_published(content):
	if (content == ""):
		return ""
	# Could be 26-Sep, OCT, SEP-OCT
	content = content.upper()
	if ('-' in content):
		content = content[content.find('-')+1:]
	if content == "JAN":
		return "01"
	elif content == "FEB":
		return "02"
	elif content == "MAR":
		return "03"
	elif content == "APR":
		return "04"
	elif content == "MAY":
		return "05"
	elif content == "JUN":
		return "06"
	elif content == "JUL":
		return "07"
	elif content == "AUG":
		return "08"
	elif content == "SEP":
		return "09"
	elif content == "OCT":
		return "10"
	elif content == "NOV":
		return "11"
	else:
		return "12"

def determine_property_access_link_value(content):
	if content == '':
		return ["Traditional Publishing"]
	else:
		if "," in content:
			output = []
			strs = content.split(",")
			for element in strs:
				output.append(element.strip() + " Open Access")
			return output
		else:
			return [content + " Open Access"]

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

	publication_topics, publication_links, topic_key_val, link_key_val = convert_publications(data, topic_key_val, link_key_val)

	# This dict will tell us if links are already going to be created. Keyed by (from, to), value doesn't matter
	duplicated_links_dict = dict()

	for rowidx in range(len(data)):
		# Get current row in dataset
		publication_row = data.iloc[rowidx,:]

		# Find corresponding topic in publication_topics
		my_row = "row " + str(rowidx + 2) + ','
		my_row2 = "row " + str(rowidx + 2)
		temporary_topic_struct = {}
		for topic in publication_topics:
			if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
				temporary_topic_struct = topic
				break

		month_published = parse_month_published(publication_row['PD'])
		year_published = str(publication_row['PY'])
		volume = str(publication_row['VL'])
		issue = str(publication_row['IS'])
		part = str(publication_row['PN'])

		# Determine title for this journal instance
		topic_title = 'Volume '
		if volume == '':
			topic_title = topic_title + year_published
		else:
			topic_title = topic_title + volume

		if issue != '':
			topic_title = topic_title + ', Issue ' + issue
		if part != '':
			topic_title = topic_title + ', Part ' + part

		if month_published != '':
			topic_title = topic_title + ', ' + month_published + '-' + year_published + ' - ' + temporary_topic_struct['title']
		else:
			topic_title = topic_title + ', ' + year_published + ' - ' + temporary_topic_struct['title']
		# Terms is just the topic title
		terms = [topic_title]

		# Look for duplicates
		duplicate = False
		for topic in new_topics:
			if topic['title'] == topic_title:
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
		topic_json_struct["_type"] = 'publication'
		topic_json_struct['title'] = topic_title
		topic_json_struct['terms'] = terms
		topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)
		topic_json_struct['month published'] = month_published
		topic_json_struct['year published'] = year_published
		topic_json_struct['volume'] = volume
		topic_json_struct['issue'] = issue
		topic_json_struct['part'] = part
		topic_json_struct['ISSN'] = temporary_topic_struct['ISSN']
		topic_json_struct['Electronic_ISSN'] = temporary_topic_struct['Electronic_ISSN']
		topic_json_struct['ISBN'] = temporary_topic_struct['ISBN']
		# Store in list to output at end
		new_topics.append(topic_json_struct)

		# (1) Link from journal to instance
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'hasInstance'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = temporary_topic_struct['_key'] 
		link_json_struct['_to'] = topic_key
		# Store in list to output at end
		new_links.append(link_json_struct)

		# (2) Link to property access type
		access_values = determine_property_access_link_value(publication_row['OA'])
		for value in access_values:
			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1
			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'has'
			link_json_struct['name'] = ''
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = temporary_topic_struct['_key'] 
			link_json_struct['_to'] = "T14"
			link_json_struct['value'] = value
			# Store in list to output at end if link does not already exit
			if (duplicated_links_dict.get((temporary_topic_struct['_key'], "T14")) == None):
				new_links.append(link_json_struct)
		# This can only be marked at the end of the first run, otherwise there will only be one link, when actually we want 'duplicate links' with different values
		duplicated_links_dict[(temporary_topic_struct['_key'], "T14")] = 1


		# (3) Link to property publication type
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1

		value = ''
		if publication_row['PT'] == 'J':
			value = "Journal"
		elif publication_row['PT'] == 'S':
			value = "Series"
		elif publication_row['PT'] == 'P':
			value = 'Patent'
		elif publication_row['PT'] == 'B':
			value = 'Book'
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = temporary_topic_struct['_key'] 
		link_json_struct['_to'] = "T16"
		link_json_struct['value'] = value
		# Store in list to output at end if link does not already exit
		if (duplicated_links_dict.get((temporary_topic_struct['_key'], "T16")) == None):
			new_links.append(link_json_struct)
			duplicated_links_dict[(temporary_topic_struct['_key'], "T16")] = 1

		# (4) Link to property Language
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1

		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = temporary_topic_struct['_key'] 
		link_json_struct['_to'] = "T17"
		link_json_struct['value'] = publication_row['LA']
		# Store in list to output at end if link does not already exit
		if (duplicated_links_dict.get((temporary_topic_struct['_key'], "T17")) == None):
			new_links.append(link_json_struct)
			duplicated_links_dict[(temporary_topic_struct['_key'], "T17")] = 1

		# (5) Link to property published date
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1

		value = ''
		if month_published != '' and year_published != '':
			value = month_published + '-' + year_published
		elif month_published == '' and year_published != '':
			value = year_published
		elif month_published != '' and year_published == '':
			value = month_published

		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = temporary_topic_struct['_key'] 
		link_json_struct['_to'] = "T18"
		link_json_struct['value'] = value
		if (duplicated_links_dict.get((temporary_topic_struct['_key'], "T18")) == None):
			new_links.append(link_json_struct)
			duplicated_links_dict[(temporary_topic_struct['_key'], "T18")] = 1

	new_topics = publication_topics + new_topics
	new_links = publication_links + new_links
	# Output topics to file
	with open('output/journal_topics.json', 'w') as f:
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
	with open('output/journal_links.json', 'w') as f:
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