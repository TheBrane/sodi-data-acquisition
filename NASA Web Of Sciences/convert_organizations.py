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

def post_process_organizations(organization_topics):
	terms = dict()
	terms['Univ'] = 'University'
	terms['Amer'] = 'American'
	terms['Assoc'] = 'Association'
	terms['Soc'] = 'Society'
	terms['Int'] = 'International'
	terms['Inst'] = 'Institute'
	terms['Acad'] = 'Academy'
	terms['Sci'] = 'Science'
	terms['Appl'] = 'Applied'
	terms['Natl'] = 'National'
	terms['Extraterr'] = 'Extraterrestrial'
	terms['Mech'] = 'Mechanics'
	terms['Calif'] = 'California'
	terms['Technol'] = 'Technology'
	terms['Ctr'] = 'Center'
	terms['Nucl'] = 'Nuclear'
	terms['Explorat'] = 'Exploration'
	terms['Agcy'] = 'Agency'
	terms['Mol'] = 'Molecular'
	terms['Physiol'] = 'Physiology'
	terms['Hlth'] = 'Health'
	terms['Fdn'] = 'Foundation'
	terms['Hosp'] = 'Hospital'
	terms['Sch'] = 'School'
	terms['Res'] = 'Research'
	terms['Math'] = 'Mathematics'
	terms['Aeron'] = 'Aeronomy'
	terms['Genet'] = 'Genetics'
	terms['Select'] = 'Selection'
	terms['Ind'] = 'Industrial'
	terms['Grp'] = 'Group'
	terms['Engn'] = 'Engineering'
	terms['Atmospher'] = 'Atmospheric'
	terms['Pharmaceut'] = 'Pharmaceutical'
	terms['Coll'] = 'College'
	terms['Lab'] = 'Laboratory'
	terms['Biochem'] = 'Biochemistry'
	terms['Hop'] = 'Hopital'
	terms['Fac'] = 'Faculty'
	terms['Prop'] = 'Propulsion'
	terms['Nutr'] = 'Nutritional'
	terms['Dept'] = 'Department'
	terms['Federat'] = 'Federation'
	terms['Promot'] = 'Promotion'
	terms['Informat'] = 'Information'
	terms['Commun'] = 'Communication'
	terms['Ecol'] = 'Ecology'
	terms['Techn'] = 'Techniques'
	terms['Solut'] = 'Solutions'
	terms['Adm'] = 'Administration'
	terms['Vet'] = 'Veterans'
	terms['Tech'] = 'Technology'
	terms['Radiol'] = 'Radiological'
	terms['Environm'] = 'Environmental'
	terms['Syst'] = 'Systems'
	terms['Off'] = 'Office'
	terms['Rech'] = 'Recherches'
	terms['Meteorol'] = 'Meteorological'
	terms['Minist'] = 'Ministry'
	terms['Canc'] = 'Cancer'
	terms['Biosci'] = 'Bioscience'
	terms['Bldg'] = 'Building'
	terms['Cent'] = 'Central'
	terms['Surg'] = 'Surgery'
	terms['Operat'] = 'Operations'
	terms['Adv'] = 'Advanced'
	terms['So'] = 'Southern'
	terms['S'] = 'Southern'
	terms['Infect'] = 'Infection'
	terms['Biol'] = 'Biology'
	terms['Dynam'] = 'Dynamics'
	terms['Corp'] = 'Corportation'
	terms['Gen'] = 'General'
	terms['Utilizat'] = 'Utilization'
	terms['Promot'] = 'Promotion'
	terms['Isl'] = 'Island'	

	for topic in organization_topics:
		topic_title = topic['title']
		words_in_title = topic_title.split(" ")
		temp_topic_title = ""
		for index, word in enumerate(words_in_title):
			if index == 0 and word == 'Univ':
				word = 'University of'
			else:
				word = terms.get(word) or word
			temp_topic_title = temp_topic_title + " " + word
		topic['title'] = temp_topic_title.strip()
	return organization_topics

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

	# For later use, I will convert all the researcher names to a dict mapping name to key
	researchers_name_to_key = dict()
	for topic in researcher_topics:
		researchers_name_to_key[topic['title']] = topic['_key']
	# This dict will tell us if links are already going to be created. Keyed by (from, to), value doesn't matter
	duplicated_links_dict = dict()

	# G1
	for rowidx in range(len(data)):
		# Get current row in dataset
		publication_row = data.iloc[rowidx,:]
		# Set properties
		_type = "topic"
		topic_title = publication_row['PU'].title()
		definition = topic_title + " as for address " + publication_row['PA'].title()

		# Find corresponding topic in publication_topics
		my_row = "row " + str(rowidx + 2) + ','
		my_row2 = "row " + str(rowidx + 2)
		temporary_topic_struct = {}
		for topic in publication_topics:
			if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
				temporary_topic_struct = topic
				break

		# Look for duplicates
		duplicate = False
		topic_key = ''
		for topic in new_topics:
			if topic['title'] == topic_title:
				topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
				duplicate = True
				topic_key = topic['_key']
		# Only make a topic for this publisher if it is not a duplicate. In that case, we have to link to the publishers cluster.
		# We have to link to the journal regardless as long as that specific link is not a duplicate. A publisher could have multiple journals, so a row in the dataset could have an already created publisher with a new journal we have not seen yet
		if (not duplicate):
			topic_key = 'T' + str(topic_key_val)
			# Increment key value for next topic
			topic_key_val = topic_key_val + 1

			# Output topic to JSON format
			topic_json_struct = {}
			topic_json_struct['_key'] = topic_key
			topic_json_struct["_type"] = _type
			topic_json_struct['title'] = topic_title
			topic_json_struct['definition'] = definition
			topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)

			# Store in list to output at end
			new_topics.append(topic_json_struct)

			# (1) Link from publishers cluster to publisher
			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1
			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'hasInstance'
			link_json_struct['name'] = ''
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = 'T23' 
			link_json_struct['_to'] = topic_key
			# Store in list to output at end
			new_links.append(link_json_struct)

		# (2) Link publisher to journal
		link_key = 'L' + str(link_key_val)
		# Increment key value for next link
		link_key_val = link_key_val + 1

		# Output link to JSON format
		link_json_struct = {}
		link_json_struct['_key'] = link_key
		link_json_struct['_type'] = 'link'
		link_json_struct['name'] = 'publishes'
		link_json_struct['definition'] = ''
		link_json_struct['_from'] =  topic_key
		link_json_struct['_to'] = temporary_topic_struct['_key']
		# Store in list to output at end if link does not already exit
		if (duplicated_links_dict.get((topic_key, temporary_topic_struct['_key'])) == None):
			new_links.append(link_json_struct)
			duplicated_links_dict[(topic_key, temporary_topic_struct['_key'])] = 1
	# G2
	for rowidx in range(len(data)):
		# Get current row in dataset
		publication_row = data.iloc[rowidx,:]
		if (publication_row['RP'] != ""):
			_type = "topic"
			reprint = publication_row['RP']
			loc = reprint.find('(reprint author)') + 18
			topic_title = reprint[loc: reprint.find(',', loc)].title()
			terms = [topic_title]
			definition = reprint[loc: reprint.find('.', loc) + 1]

			# Look for duplicates
			duplicate = False
			topic_key = ''
			for topic in new_topics:
				if topic['title'] == topic_title:
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					duplicate = True
					topic_key = topic['_key']
			# Only make a topic for this publisher if it is not a duplicate. In that case, we have to link to the research organizations cluster. 
			# However, linking research organizations to the researcher needs to be done regardless rows refering to the the same research organization may have different researchers
			if (not duplicate):
				topic_key = 'T' + str(topic_key_val)
				# Increment key value for next topic
				topic_key_val = topic_key_val + 1

				# Output topic to JSON format
				topic_json_struct = {}
				topic_json_struct['_key'] = topic_key
				topic_json_struct["_type"] = _type
				topic_json_struct['title'] = topic_title
				topic_json_struct['definition'] = definition
				topic_json_struct['terms'] = terms
				topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)

				# Store in list to output at end
				new_topics.append(topic_json_struct)

				# (1) Link from research organizations cluster to organization
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1
				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['definition'] = ''
				link_json_struct['_from'] = 'T22' 
				link_json_struct['_to'] = topic_key
				# Store in list to output at end
				new_links.append(link_json_struct)

			# (2) Link research organizations to researcher
			# Researchers does not follow the same method of adding row x, row y to sources. We have a last name and a first initial, but that is not enough due to duplicate names. We cannot rely on topic['sources'] either
			# As a result, I am getting a list of all the authors for this row and finding the corresponding key in researcher_topics. 
			flipped_name = reprint[:loc - 19]
			last_name = flipped_name[:flipped_name.find(',')].title()
			authors = publication_row['AF'].split(";")
			researcher_key = None
			for author in authors:
				# Check for incorrectly formatted name - very rare, but has to be done
				if (author.find(',') == -1):
					# Skip if no comma
					continue
				first, last = parse_author(author)
				if (last_name == last):
					researcher_key = researchers_name_to_key.get(form_author_name(first, last))
			# This is possible and is due to different spellings of the name. There are 7 researchers where this occurs
			if researcher_key == None:
				pass
				# print(flipped_name + " on row " + str(rowidx + 2) + " could not be found in the created researchers")
			else:
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1
				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'link'
				link_json_struct['name'] = 'is affiliated with'
				link_json_struct['definition'] = ''
				link_json_struct['_from'] =  researcher_key
				link_json_struct['_to'] = topic_key
				# Store in list to output at end if link does not already exit
				if (duplicated_links_dict.get((researcher_key, topic_key)) == None):
					new_links.append(link_json_struct)
					duplicated_links_dict[(researcher_key, topic_key)] = 1

	new_topics = post_process_organizations(new_topics)

	new_topics = publication_topics + new_topics
	new_links = publication_links + new_links
	new_topics = researcher_topics + new_topics
	new_links = researcher_links + new_links

	# Output topics to file
	with open('output/organization_topics.json', 'w') as f:
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
	with open('output/organization_links.json', 'w') as f:
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