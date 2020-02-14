import json
import csv
import numpy as np
import pandas as pd

# General helper function
def parse_author(author):
	# The form is LastName, FirstName or LastName, FirstName Middle
	# The middle name will remain part of the first name
	author = author.strip()
	last_name = author.split(',')[0].strip().title()
	first_name = author.split(",")[1].strip().title()
	return first_name, last_name

# General helper function
def form_author_name(first_name, last_name):
	return first_name + " " + last_name

# Protocol B helper function
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

# Protocol B main function to run
def convert_researchers(data, topic_key_val, link_key_val):
	researcher_topics = list()
	researcher_links = list()

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
			for topic in researcher_topics:
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
			researcher_topics.append(topic_json_struct)

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
			researcher_links.append(link_json_struct)
	return researcher_topics, researcher_links, topic_key_val, link_key_val

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

# Protocol D helper function
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

# Protocol D helper function
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

# Protocol D main function to run
def convert_journals(data, topic_key_val, link_key_val, publication_topics):
	journal_topics = list()
	journal_links = list()
	
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
		for topic in journal_topics:
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
		journal_topics.append(topic_json_struct)

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
		journal_links.append(link_json_struct)

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
				journal_links.append(link_json_struct)
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
			journal_links.append(link_json_struct)
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
			journal_links.append(link_json_struct)
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
			journal_links.append(link_json_struct)
			duplicated_links_dict[(temporary_topic_struct['_key'], "T18")] = 1
	return journal_topics, journal_links, topic_key_val, link_key_val

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

	researcher_topics, researcher_links, topic_key_val, link_key_val = 	convert_researchers(data, topic_key_val, link_key_val)
	publication_topics, publication_links, topic_key_val, link_key_val = convert_publications(data, topic_key_val, link_key_val)
	journal_topics, journal_links, topic_key_val, link_key_val = convert_journals(data, topic_key_val, link_key_val, publication_topics)

	# For later use, I will convert all the researcher names to a dict mapping name to key
	researchers_name_to_key = dict()
	for topic in researcher_topics:
		researchers_name_to_key[topic['title']] = topic['_key']

	for rowidx in range(len(data)):
		# Get current row in dataset
		publication_row = data.iloc[rowidx,:]

		topic_title = publication_row['TI']
		terms = [topic_title]
		definition = publication_row['AB']
		acknowledgement = publication_row['FX']
		b_page = str(publication_row['BP'])
		e_page = str(publication_row['EP'])
		doi = str(publication_row['DI'])
		articleID = publication_row['AR']
		woSID = publication_row['UT']
		pubMedID = publication_row['PM']
		date_downloaded = publication_row['DA']
		grants = publication_row['FU']
		cited_reference = [x.strip() for x in publication_row['CR'].split(';')]

		# Look for duplicates
		duplicate = False
		for topic in new_topics:
			if topic['title'] == topic_title:
				topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
				duplicate = True
		# Skip making a topic for this article. There is one duplicate, so to simplify the logic, we will just say that line in the dataset does not provide any additional information
		if (duplicate):
			continue

		# Find corresponding created topic in journal_topics
		my_row = "row " + str(rowidx + 2) + ','
		my_row2 = "row " + str(rowidx + 2)
		temporary_journal_topic_struct = {}
		for topic in journal_topics:
			if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
				temporary_journal_topic_struct = topic
				break

		# Find corresponding created topic in publication_topics
		my_row = "row " + str(rowidx + 2) + ','
		my_row2 = "row " + str(rowidx + 2)
		temporary_publication_topic_struct = {}
		for topic in publication_topics:
			if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
				temporary_publication_topic_struct = topic
				break

		# Inherit certain properties from this topic
		journal_key = temporary_journal_topic_struct['_key']
		issn = temporary_journal_topic_struct['ISSN']
		electronic_issn = temporary_journal_topic_struct['Electronic_ISSN']
		isbn = temporary_journal_topic_struct['ISBN']
		month_published = temporary_journal_topic_struct['month published']
		year_published = temporary_journal_topic_struct['year published']
		volume = temporary_journal_topic_struct['volume']
		issue = temporary_journal_topic_struct['issue']
		part = temporary_journal_topic_struct['part']
		journal = temporary_publication_topic_struct['title']

		topic_key = 'T' + str(topic_key_val)
		# Increment key value for next topic
		topic_key_val = topic_key_val + 1

		# Output topic to JSON format
		topic_json_struct = {}
		topic_json_struct['_key'] = topic_key
		topic_json_struct["_type"] = "publication"
		topic_json_struct['title'] = topic_title
		topic_json_struct['terms'] = terms
		topic_json_struct['definition'] = definition
		topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)
		topic_json_struct['ISSN'] = issn
		topic_json_struct['Electronic_ISSN'] = electronic_issn
		topic_json_struct['ISBN'] = isbn
		topic_json_struct['month published'] = month_published
		topic_json_struct['year published'] = year_published
		topic_json_struct['volume'] = volume
		topic_json_struct['issue'] = issue
		topic_json_struct['part'] = part
		topic_json_struct['acknowledgement'] = acknowledgement
		topic_json_struct['beginning page'] = b_page
		topic_json_struct['ending page'] = e_page
		topic_json_struct['DOI'] = doi
		topic_json_struct['ArticleID'] = articleID
		topic_json_struct['WoSID'] = woSID
		topic_json_struct['PubMedID'] = pubMedID
		topic_json_struct['date downloaded'] = date_downloaded
		topic_json_struct['grants'] = grants
		topic_json_struct['cited reference'] = cited_reference
		topic_json_struct['journal'] = journal

		# Store in list to output at end
		new_topics.append(topic_json_struct)

		# (1) Create links between cluster - topic
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'hasInstance'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = 'T13'
		link_json_struct['_to'] = topic_key
		# Store in list to output at end
		new_links.append(link_json_struct)

		# (2) Create link between journal instances and article
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'link'
		link_json_struct['name'] = 'contains_01'
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = journal_key
		link_json_struct['_to'] = topic_key
		# Store in list to output at end
		new_links.append(link_json_struct)
		# (3) Create links between researcher and article
		authors = publication_row['AF'].split(";")
		# Determine who reprint author is
		reprint = publication_row['RP']
		loc = reprint.find('(reprint author)') + 18
		flipped_name = reprint[:loc - 19]
		reprint_last_name = flipped_name[:flipped_name.find(',')].title()

		researcher_key = None
		for author in authors:
			# Check for incorrectly formatted name - very rare, but has to be done
			if (author.find(',') == -1):
				# Skip if no comma
				continue
			first, last = parse_author(author)
			researcher_key = researchers_name_to_key.get(form_author_name(first, last))
			# This is possible and is due to different spellings of the name. 
			if researcher_key == None:
				pass
			else:
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1
				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'link'
				link_json_struct['name'] = 'authors'
				link_json_struct['definition'] = ''
				link_json_struct['_from'] =  researcher_key
				link_json_struct['_to'] = topic_key
				# Add to list
				new_links.append(link_json_struct)

				# Reprint author link
				if reprint_last_name == last:
					link_key = 'L' + str(link_key_val)
					# Increment key value for next link
					link_key_val = link_key_val + 1
					# Output link to JSON format
					link_json_struct = {}
					link_json_struct['_key'] = link_key
					link_json_struct['_type'] = 'link'
					link_json_struct['name'] = 'reprint'
					link_json_struct['definition'] = ''
					link_json_struct['_from'] =  researcher_key
					link_json_struct['_to'] = topic_key
					# Add to list
					new_links.append(link_json_struct)

		# (5) Link to download date
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = topic_key
		link_json_struct['_to'] = 'T15'
		link_json_struct['value'] = date_downloaded
		# Store in list to output at end
		new_links.append(link_json_struct)

		# (4, 6, 7) Link to property access type, language, published date,
		# First find the corresponding journal from this journal instance
		j_key = ''
		for link in journal_links:
			if link['_to'] == journal_key:
				j_key = link['_from']

		# Now get the values for the specific properties using the original journal's key
		access_types = []
		language = ''
		published_date = ''
		for link in journal_links:
			if link['_from'] == j_key and j_key != journal_key:
				if link['_to'] == 'T14':
					access_types.append(link['value'])
				elif link['_to'] == 'T17':
					language = link['value']
				elif link['_to'] == 'T18':
					published_date = link['value']

		# Link for each access type
		for access_type in access_types:
			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1
			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'has'
			link_json_struct['name'] = ''
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = topic_key
			link_json_struct['_to'] = 'T14'
			link_json_struct['value'] = access_type
			# Store in list to output at end
			new_links.append(link_json_struct)
		# (6) Link for language
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = topic_key
		link_json_struct['_to'] = 'T17'
		link_json_struct['value'] = language
		# Store in list to output at end
		new_links.append(link_json_struct)		

		# (7) Link to published date
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1
		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'has'
		link_json_struct['name'] = ''
		link_json_struct['definition'] = ''
		link_json_struct['_from'] = topic_key
		link_json_struct['_to'] = 'T18'
		link_json_struct['value'] = published_date
		# Store in list to output at end
		new_links.append(link_json_struct)

		# (8) Link to property document type
		doc_types = []
		# There are multiple document types
		if publication_row['DT'].find(';') != -1:
			doc_types = publication_row['DT'].split(';')
		else:
			doc_types = [publication_row['DT']]
		for doc_type in doc_types:
			doc_type = doc_type.strip()

			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1
			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'has'
			link_json_struct['name'] = ''
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = topic_key
			link_json_struct['_to'] = 'T19'
			link_json_struct['value'] = doc_type
			# Store in list to output at end
			new_links.append(link_json_struct)

	new_topics = journal_topics + new_topics
	new_links = journal_links + new_links
	new_topics = publication_topics + new_topics
	new_links = publication_links + new_links
	new_topics = researcher_topics + new_topics
	new_links = researcher_links + new_links

	# Output topics to file
	with open('output/article_topics.json', 'w') as f:
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
	with open('output/article_links.json', 'w') as f:
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