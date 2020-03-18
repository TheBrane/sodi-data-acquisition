'''
	Kaushik Tandon
	January 2020
	NASA Web Of Science conversion for The Brane
'''

import json
import csv
import numpy as np
import pandas as pd

import requests
import inflection as inf
from collections import OrderedDict
from nltk.corpus import wordnet as wn
import nltk
nltk.download('wordnet')
import warnings
warnings.filterwarnings('ignore')

class Convert_Clusters():
	def __init__(self):
		print("Create clusters")
	def convert_clusters(self):
		cluster_topics = list()
		cluster_links = list()
		properties = dict()

		# Create generic properties
		properties['_key'] = ''
		properties['_type'] = ''
		properties['title'] = ""
		properties['terms'] = ''
		properties['definition'] = ''
		properties['sources'] = ''
		properties['firstName'] = ''
		properties['lastName'] = ''
		properties['initials'] = ''
		properties['email'] = ''
		properties['orcidID'] = ''
		properties['Possible_Duplicates'] = ''
		properties['Notes'] = ''
		properties['valueType'] = ''

		# T1
		properties['_key'] = 'T1'
		properties['_type'] = 'system'
		properties['title'] = "Web of Science"
		cluster_topics.append(self.create_topic(properties))
		# T2
		properties['_key'] = 'T2'
		properties['_type'] = 'cluster'
		properties['title'] = "Individual"
		cluster_topics.append(self.create_topic(properties))
		# T3
		properties['_key'] = 'T3'
		properties['_type'] = 'cluster'
		properties['title'] = "Researcher"
		cluster_topics.append(self.create_topic(properties))
		# T4
		properties['_key'] = 'T4'
		properties['_type'] = 'cluster'
		properties['title'] = "Event"
		cluster_topics.append(self.create_topic(properties))
		# T5
		properties['_key'] = 'T5'
		properties['_type'] = 'cluster'
		properties['title'] = "Conference"
		cluster_topics.append(self.create_topic(properties))
		# T6
		properties['_key'] = 'T6'
		properties['_type'] = 'cluster'
		properties['title'] = "Workshop"
		cluster_topics.append(self.create_topic(properties))
		# T7
		properties['_key'] = 'T7'
		properties['_type'] = 'cluster'
		properties['title'] = "Symposium"
		cluster_topics.append(self.create_topic(properties))
		# T8
		properties['_key'] = 'T8'
		properties['_type'] = 'cluster'
		properties['title'] = "Congress"
		cluster_topics.append(self.create_topic(properties))
		# T9
		properties['_key'] = 'T9'
		properties['_type'] = 'cluster'
		properties['title'] = "Meeting"
		cluster_topics.append(self.create_topic(properties))
		# T10
		properties['_key'] = 'T10'
		properties['_type'] = 'cluster'
		properties['title'] = "Publication"
		cluster_topics.append(self.create_topic(properties))
		# T11
		properties['_key'] = 'T11'
		properties['_type'] = 'cluster'
		properties['title'] = "Journal"
		cluster_topics.append(self.create_topic(properties))
		# T12
		properties['_key'] = 'T12'
		properties['_type'] = 'cluster'
		properties['title'] = "Conference Proceeding"
		cluster_topics.append(self.create_topic(properties))
		# T13
		properties['_key'] = 'T13'
		properties['_type'] = 'cluster'
		properties['title'] = "Article"
		cluster_topics.append(self.create_topic(properties))
		# T14
		properties['_key'] = 'T14'
		properties['_type'] = 'property'
		properties['title'] = "Access type"
		properties['valueType'] = 'String'		
		cluster_topics.append(self.create_topic(properties))
		# T15
		properties['_key'] = 'T15'
		properties['_type'] = 'property'
		properties['title'] = "Download date"
		properties['valueType'] = 'Date'		
		cluster_topics.append(self.create_topic(properties))
		# T16
		properties['_key'] = 'T16'
		properties['_type'] = 'property'
		properties['title'] = "Publication type"
		properties['valueType'] = 'String'		
		cluster_topics.append(self.create_topic(properties))
		# T17
		properties['_key'] = 'T17'
		properties['_type'] = 'property'
		properties['title'] = "Language"
		properties['valueType'] = 'String'		
		cluster_topics.append(self.create_topic(properties))
		# T18
		properties['_key'] = 'T18'
		properties['_type'] = 'property'
		properties['title'] = "Published date"
		properties['valueType'] = 'Date'		
		cluster_topics.append(self.create_topic(properties))
		# T19
		properties['_key'] = 'T19'
		properties['_type'] = 'property'
		properties['title'] = "Document type"
		properties['valueType'] = 'String'		
		cluster_topics.append(self.create_topic(properties))
		# T20
		properties['_key'] = 'T20'
		properties['_type'] = 'property'
		properties['title'] = "Conference year"
		properties['valueType'] = 'String'		
		cluster_topics.append(self.create_topic(properties))
		# T21
		properties['_key'] = 'T21'
		properties['_type'] = 'cluster'
		properties['title'] = "Organization"
		properties['valueType'] = ''		
		cluster_topics.append(self.create_topic(properties))
		# T22
		properties['_key'] = 'T22'
		properties['_type'] = 'cluster'
		properties['title'] = "Research organization"
		cluster_topics.append(self.create_topic(properties))
		# T23
		properties['_key'] = 'T23'
		properties['_type'] = 'cluster'
		properties['title'] = "Publisher"
		cluster_topics.append(self.create_topic(properties))
		# T24
		properties['_key'] = 'T24'
		properties['_type'] = 'cluster'
		properties['title'] = "Keyword"
		cluster_topics.append(self.create_topic(properties))
		# T25
		properties['_key'] = 'T25'
		properties['_type'] = 'cluster'
		properties['title'] = "Tagged Keyword"
		cluster_topics.append(self.create_topic(properties))
		# T26
		properties['_key'] = 'T26'
		properties['_type'] = 'cluster'
		properties['title'] = "Untagged Keyword"
		cluster_topics.append(self.create_topic(properties))
		# T97
		properties['_key'] = 'T97'
		properties['_type'] = 'cluster'
		properties['title'] = "Wordnet ontology"
		cluster_topics.append(self.create_topic(properties))

		# Change this if more topics added!
		final_topic = 97

		# Create Links
		properties = dict()
		properties['_key'] = ''
		properties['_type'] = ''
		properties['name'] = ''
		properties['definition'] = ''
		properties['_from'] = ''
		properties['_to'] = ''
		# L1
		properties['_key'] = 'L1'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T2'
		cluster_links.append(self.create_link(properties))
		# L2
		properties['_key'] = 'L2'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T4'
		cluster_links.append(self.create_link(properties))
		# L3
		properties['_key'] = 'L3'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T10'
		cluster_links.append(self.create_link(properties))
		# L4
		properties['_key'] = 'L4'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T21'
		cluster_links.append(self.create_link(properties))
		# L5
		properties['_key'] = 'L5'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T2'
		properties['_to'] = 'T3'
		cluster_links.append(self.create_link(properties))
		# L6
		properties['_key'] = 'L6'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T4'
		properties['_to'] = 'T5'
		cluster_links.append(self.create_link(properties))
		# L7
		properties['_key'] = 'L7'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T4'
		properties['_to'] = 'T6'
		cluster_links.append(self.create_link(properties))
		# L8
		properties['_key'] = 'L8'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T4'
		properties['_to'] = 'T7'
		cluster_links.append(self.create_link(properties))
		# L9
		properties['_key'] = 'L9'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T4'
		properties['_to'] = 'T8'
		cluster_links.append(self.create_link(properties))
		# L10
		properties['_key'] = 'L10'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T4'
		properties['_to'] = 'T9'
		cluster_links.append(self.create_link(properties))
		# L11
		properties['_key'] = 'L11'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T10'
		properties['_to'] = 'T11'
		cluster_links.append(self.create_link(properties))
		# L12
		properties['_key'] = 'L12'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T10'
		properties['_to'] = 'T12'
		cluster_links.append(self.create_link(properties))
		# L13
		properties['_key'] = 'L13'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T10'
		properties['_to'] = 'T13'
		cluster_links.append(self.create_link(properties))
		# L14
		properties['_key'] = 'L14'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T21'
		properties['_to'] = 'T22'
		cluster_links.append(self.create_link(properties))
		# L15
		properties['_key'] = 'L15'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T21'
		properties['_to'] = 'T23'
		cluster_links.append(self.create_link(properties))
		# L16
		properties['_key'] = 'L16'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T24'
		cluster_links.append(self.create_link(properties))
		# L17
		properties['_key'] = 'L17'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T24'
		properties['_to'] = 'T25'
		cluster_links.append(self.create_link(properties))
		# L18
		properties['_key'] = 'L18'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T24'
		properties['_to'] = 'T26'
		cluster_links.append(self.create_link(properties))

		# Change this if more links added!
		final_link = 18

		return cluster_topics, cluster_links, final_topic + 1, final_link + 1
	def create_topic(self, properties):
		topic_json_struct = {}
		for prop, value in properties.items():
			topic_json_struct[prop] = value
		return topic_json_struct
	def create_link(self, properties):
		link_json_struct = {}
		for prop, value in properties.items():
			link_json_struct[prop] = value
		return link_json_struct

class Convert_Researchers():
	def __init__(self):
		print("Protocol B")
	def parse_orcid_id(self, row, authors):
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
	def convert_researchers(self, data, topic_key_val, link_key_val):
		researcher_topics = list()
		researcher_links = list()
		topics = dict()

		for rowidx in range(len(data)):
			# Get current row in dataset
			publication_row = data.iloc[rowidx,:]
			# Get the authors using the AF key
			authors = publication_row['AF'].split(";")
			reprint_address_last_name = publication_row['RP'].split(",")[0].title()
			orcidIDs = self.parse_orcid_id(publication_row['OI'], authors)
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

				set_to_search = topics.get(title)
				if set_to_search != None:
					for topic in set_to_search:
						# If the orcid IDs match and we can't deduplicate
						if (topic['title'] == title and topic['orcidID'] == orcid_id and orcid_id == ""):
							topic['Possible_Duplicates'].append(topic_key)
							possible_duplicates.append(topic['_key'])
						elif (topic['title'] == title and topic['orcidID'] == orcid_id and orcid_id != ""):
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

				if (topics.get(title) == None):
					new_researchers = list()
					new_researchers.append(topic_json_struct)
					topics[title] = new_researchers
				else:
					topics[title].append(topic_json_struct)

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
		for title, topic_json_struct_set in topics.items():
			for topic in topic_json_struct_set:
				researcher_topics.append(topic)
		return researcher_topics, researcher_links, topic_key_val, link_key_val

class Convert_Publications():
	def __init__(self):
		print("Protocol C")
	# Protocol C main function to run
	def convert_publications(self, data, topic_key_val, link_key_val):
		publication_topics = list()
		publication_links = list()

		for rowidx in range(len(data)):
			# Get current row in dataset
			publication_row = data.iloc[rowidx,:]
			issn = publication_row['SN']
			electronic_issn = publication_row['EI']
			isbn = publication_row['BN']
			# Determine which columns to read based off value of ISBN
			if (isbn == ""):
				topic_title = publication_row['SO'].title()
				terms = [topic_title, publication_row['J9'].title(), publication_row['JI'].title()]
				conference_proceeding = False
				_type = "journal"
			else:
				topic_title = publication_row['SE'].title()
				terms = [topic_title, publication_row['J9'].title()]
				conference_proceeding = True
				_type = "journal"

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

class Convert_Journals():
	def __init__(self):
		print("Protocol D")
	def parse_month_published(self, content):
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
	def determine_property_access_link_value(self, content):
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
	def convert_journals(self, data, topic_key_val, link_key_val, publication_topics):
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

			month_published = self.parse_month_published(publication_row['PD'])
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
			access_values = self.determine_property_access_link_value(publication_row['OA'])
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

class Convert_Articles():
	def __init__(self):
		print("Protocol E")
	# Protocol E main function to run
	def convert_articles(self, data, topic_key_val, link_key_val, researcher_topics, publication_topics, journal_topics, journal_links):
		article_topics = list()
		article_links = list()

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
			for topic in article_topics:
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
			article_topics.append(topic_json_struct)

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
			article_links.append(link_json_struct)

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
			article_links.append(link_json_struct)
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
					article_links.append(link_json_struct)

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
						article_links.append(link_json_struct)

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
			article_links.append(link_json_struct)

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
				article_links.append(link_json_struct)
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
			article_links.append(link_json_struct)		

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
			article_links.append(link_json_struct)

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
				article_links.append(link_json_struct)

		return article_topics, article_links, topic_key_val, link_key_val

class Convert_Events():
	def __init__(self):
		print("Protocol F")
	def parse_conference_year(self, date):
		# Format is either MONTH DATE-RANGE, YEAR
		# or format is DAY-MONTH-2_DIGIT_YEAR
		# or format is just YEAR
		if "," in date: # Case 1
			year = str(date[date.find(',') + 2:])
		else:
			if '-' in date: # Case 2
				year = '20' + str(date[date.find('-',3) + 1:])
			else: # Case 3
				year = str(date)
		return year
	# Protocol F main function to run
	def convert_events(self, data, topic_key_val, link_key_val, article_topics):
		event_topics = list()
		event_links = list()

		for rowidx in range(len(data)):
			# Get current row in dataset
			publication_row = data.iloc[rowidx,:]
			# Ensure value for CT
			if (publication_row['CT'] == ''):
				continue

			_type = "topic"
			topic_title = publication_row['CT']
			terms = [topic_title]
			definition = "The " + topic_title + " was hosted on " + publication_row['CY'] + " at " + publication_row['CL'] + '.'
			if (publication_row['SP'] != ""):
				definition = definition + " This event was sponsored by " + publication_row['SP'] + '.'

			# Look for duplicates
			duplicate = False
			topic_key = ''
			for topic in event_topics:
				if topic['title'] == topic_title:
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					duplicate = True
					topic_key = topic['_key']
			# Only make topic if not a duplicate
			if (not duplicate):
				topic_key = 'T' + str(topic_key_val)
				# Increment key value for next topic
				topic_key_val = topic_key_val + 1

				# Output topic to JSON format
				topic_json_struct = {}
				topic_json_struct['_key'] = topic_key
				topic_json_struct["_type"] = _type
				topic_json_struct['title'] = topic_title
				topic_json_struct['terms'] = terms
				topic_json_struct['definition'] = definition
				topic_json_struct['sources'] = "Web of Science, row " + str(rowidx + 2)

				# Store in list to output at end
				event_topics.append(topic_json_struct)

				# (1) Link the events to their corresponding cluster
				# Determine the cluster
				standard_case_topic_title = topic_title.title()
				if 'Conference' in standard_case_topic_title:
					_from = 'T5'
				elif 'Workshop' in standard_case_topic_title:
					_from = 'T6'
				elif 'Symposium' in standard_case_topic_title:
					_from = 'T7'
				elif 'Congress' in standard_case_topic_title:
					_from = 'T8'
				else: 
					# It is a 'Meeting' or one of the following conferences that did not receive a classification
					# Default for 5th Interdisciplinary Transport Phenomena - Fluid, Thermal, Biological, Materials and Space Sciences
					# Default for 35th COSPAR Scientific Assembly
					_from = 'T9'
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['definition'] = ''
				link_json_struct['_from'] = _from 
				link_json_struct['_to'] = topic_key

				# Store in list to output at end
				event_links.append(link_json_struct)

				# (2) Link the events to the conference year property
				year = self.parse_conference_year(publication_row['CY'])
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
				link_json_struct['_to'] = 'T20'
				link_json_struct['value'] = str(year)

				# Store in list to output at end
				event_links.append(link_json_struct)

			# (3) Link the events to the articles. We still want to link the article even if the event already exists. For example, the 18th Humans in Space (HIS) Symposium of the International-Academy-of-Astronautics (IAA) should only be created once but have multiple links to various articles
			# Since articles are unique, we don't need to worry about duplicate links
			# Find corresponding topic in article_topics
			my_row = "row " + str(rowidx + 2) + ','
			my_row2 = "row " + str(rowidx + 2)
			temporary_topic_struct = {}
			for topic in article_topics:
				if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
					temporary_topic_struct = topic
					break
			article_key = temporary_topic_struct['_key']

			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1

			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'link'
			link_json_struct['name'] = 'presents'
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = topic_key 
			link_json_struct['_to'] = article_key

			# Store in list to output at end
			event_links.append(link_json_struct)

		return event_topics, event_links, topic_key_val, link_key_val

class Convert_Organizations():
	def __init__(self):
		print("Protocol G")
	def post_process_organizations(self, organization_topics):
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

	# Protocol G main function to run
	def convert_organizations(self, data, topic_key_val, link_key_val, researcher_topics, publication_topics):
		organization_topics = list()
		organization_links = list()
		
		# This dict will tell us if links are already going to be created. Keyed by (from, to), value doesn't matter
		duplicated_links_dict = dict()
		# For later use, I will convert all the researcher names to a dict mapping name to key
		researchers_name_to_key = dict()
		for topic in researcher_topics:
			researchers_name_to_key[topic['title']] = topic['_key']

		# G1
		for rowidx in range(len(data)):
			# Get current row in dataset
			publication_row = data.iloc[rowidx,:]
			# Set properties
			_type = "topic"
			topic_title = publication_row['PU'].title()
			definition = topic_title + " has address " + publication_row['PA'].title()

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
			for topic in organization_topics:
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
				organization_topics.append(topic_json_struct)

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
				organization_links.append(link_json_struct)

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
				organization_links.append(link_json_struct)
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
				for topic in organization_topics:
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
					organization_topics.append(topic_json_struct)

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
					organization_links.append(link_json_struct)

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
						organization_links.append(link_json_struct)
						duplicated_links_dict[(researcher_key, topic_key)] = 1
		organization_topics = self.post_process_organizations(organization_topics)
		return organization_topics, organization_links, topic_key_val, link_key_val

# General helper function
def add_new_topics(old_topics, new_topics):
	for topic in new_topics:
		old_topics.append(topic)
	return old_topics

# General helper function
def add_new_links(old_links, new_links):
	for link in new_links:
		old_links.append(link)
	return old_links

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

# General helper function
def output_to_file(info, file):
	with open(file, 'w') as f:
		# There's probably a better way to output as a list of JSON objects
		f.write('[')
		i = 0
		for topic in info:
			f.write(json.dumps(topic))
			if i != len(info) - 1:
				f.write(",\n")
			else:
				f.write('\n')
			i = i + 1
		f.write(']')

"""
Protocol A 
		Tashlin Reddy
		March 2020 

"""


#define helper functions
def acquire_definition(keyword):
    keyword = keyword.replace(' ', '_')
    define = wn.synsets(keyword)[0].definition()
    return define

def acquire_hypernym(keyword):
    keyword = keyword.replace(' ', '_')
    hypernym = wn.synsets(keyword)[0].hypernyms()[0].name().split(".")[0]
    return hypernym

def acquire_wordnet_id(keyword):
    keyword = keyword.replace(' ', '_')
    synset = wn.synsets(keyword)[0].name()
    ss = wn.synset(synset)
    offset = str(ss.offset()).zfill(8) + '-' + ss.pos()
    return offset
                                  
def get_link_key(df, link_key_val):
    key_link = list(range(link_key_val+1, link_key_val+df.shape[0]+1))
    results = list(map(str, key_link))
    results = ['L'+ s for s in results]
    return results

def get_topic_key(df, topic_key_val):
    key_topic = list(range(topic_key_val+1, topic_key_val+df.shape[0]+1))
    topic_key_val_new = topic_key_val+df.shape[0]+1
    results = list(map(str, key_topic))
    results = ['T'+ s for s in results]
    return results, topic_key_val_new

def capitalize_first_letter(some_string):
    try:
        new_string = some_string[0].upper() + some_string[1:].lower()
        return new_string
    except:
        return some_string
    
def remove_underscore(some_string):
    try:
        new_string = some_string.replace('_', ' ')
        return new_string
    except:
        return some_string
    

# read and clean function
def read_clean(web_of_science_path):
    df = pd.read_csv(web_of_science_path)
    
    df_filter = df[['TI','DE','ID' , 'DI']]
    df_filter['DE'] = df_filter['DE'].str.replace('; ', ', ')
    df_filter['ID'] = df_filter['ID'].str.replace('; ', ', ')
    df_filter['DE'] = df_filter['DE'].str.replace('-', ' ')
    df_filter['ID'] = df_filter['ID'].str.replace('-', ' ')
    df_filter['DE'] = df_filter['DE'].fillna(' ')
    df_filter['ID'] = df_filter['ID'].fillna(' ')

    # 2. Combine keyword columns
    df_filter['keywords'] = df_filter['DE'] + ', ' + df_filter['ID']

    # 3. lowercase keyword case
    df_filter['keywords'] = df_filter['keywords'].str.lower()
    df_filter = df_filter[['TI','keywords' , 'DI']]

    # 5. Remove duplicates
    # https://stackoverflow.com/questions/47316783/python-dataframe-remove-duplicate-words-in-the-same-cell-within-a-column-in-pyt
    df_filter['keywords'] = (df_filter['keywords'].str.split(', ')
                                  .apply(lambda x: OrderedDict.fromkeys(x).keys())
                                  .str.join(', '))
    # 6. Split strings
    df_filter['keywords'] = df_filter['keywords'].str.split(', ', expand=False)

    # 7. pandas explode - Transform each element of a list-like to a row, replicating the index values.
    df_explode = df_filter.explode('keywords')
    df_explode = df_explode[df_explode['keywords'] != ' ']
    df_explode.reset_index(inplace=True, drop=True)
    df_explode['keywords'] = df_explode['keywords'].apply(lambda x: ' '.join([inf.singularize(item) for item in x.split()]))
    df_explode_unique = df_explode.drop_duplicates(['keywords'])
    
    """Add deduplicating and singularize"""
    
    df_explode_unique.reset_index(drop=True, inplace=True)
    df_clean = df_explode_unique.copy()

    df_clean.rename(columns={'TI': 'topic_title', 'keywords': 'definition', 
                           'DI': 'reference' }, inplace=True)
    df_clean['definition'] = df_clean['definition'].str.replace('^mar$', 'mars', regex=True)
    
    return df_clean


def connect_nodes(df_clean, dict_json, topic_key_val):
    df_json = pd.DataFrame(dict_json) #dict_json
    definition_lst = []
    wordnet_ID_lst = []
    keyword_lst = []
    type_lst = []
    type_2_lst = []
    name_lst = []
    T_key_lst = []
    from_lst = []
    to_lst = []
    untagged_lst = []
    count = topic_key_val
    for index, row in df_clean.iterrows():
        #Links
    #     print('index: ', index, 'keywords: ', row['definition'])
        keyword_lst.append(row['topic_title'])
        definition_lst.append(row['definition'])
        wordnet_ID_lst.append('')
        type_lst.append('Topic')
        type_2_lst.append('link')
        name_lst.append('mentions')
        T_key_lst.append('T'+str(count))
        from_lst.append(list(df_json[df_json['title']==row['topic_title']]['_key'])[0])

        count += 1
        try:
            #hasInstance
            definition = acquire_definition(row['definition'])
            wordnet_ID = acquire_wordnet_id(row['definition'])

            keyword_lst.append(row['definition'])
            definition_lst.append(definition)
            wordnet_ID_lst.append('') #wordnet_ID
            type_lst.append('Topic')
            type_2_lst.append('hasInstance')
            name_lst.append('')
            T_key_lst.append('T'+str(count))

            to_lst.append('T'+str(count))
            to_lst.append('T'+str(count))
            count += 1
        except:
            #untagged 
            #untagged_lst.append(row['definition'])
            keyword_lst.append(row['definition'])
            type_lst.append('Topic')
            type_2_lst.append('hasInstance')
            name_lst.append('')
            T_key_lst.append('T'+str(count))
            from_lst.append('T26')
            to_lst.append('T'+str(count))
            to_lst.append('T'+str(count))

            definition_lst.append('')
            wordnet_ID_lst.append('')
            count += 1
        else:
            try:
                #cluster
                hyper = acquire_hypernym(row['definition'])
                keyword_lst.append(hyper)

                definition = acquire_definition(hyper)
                definition_lst.append(definition)

                wordnet_ID = acquire_wordnet_id(hyper)
                wordnet_ID_lst.append(wordnet_ID)

                type_lst.append('Cluster')
                type_2_lst.append('hasSubclass')
                name_lst.append('')
                T_key_lst.append('T'+str(count))
                from_lst.append('T'+str(count))
                from_lst.append('T96')

                to_lst.append('T'+str(count))
                count += 1
            except:
                from_lst.append('T25')

    df = pd.DataFrame(
        {'key':T_key_lst,
         'type': type_lst,
         'keyword': keyword_lst,
         'definition': definition_lst,
         'wordnet_ID': wordnet_ID_lst,
         '_type': type_2_lst,
         '_from': from_lst,
         '_to': to_lst,
         'name': name_lst,
        })
    return df


def remove_duplicates(df):
    new_df = df.copy()
    df_nolink = new_df[new_df['_type']!= 'link']
    #deduplicate similar clusters
    vc = df_nolink['keyword'].value_counts()
    dups = vc[vc > 1]
    dup_lst = list(dups.index[:])    
    for dup_word in dup_lst:
        dup_key_lst = list(df_nolink[df_nolink['keyword']==dup_word]['key'])
        try:
            new_df = new_df.replace(dup_key_lst[1:],dup_key_lst[0])
        except:
            print(dup_word)
    new_df = new_df.drop_duplicates()     
    return new_df, df

def merge_topic_cluster(df):
    new_df = df[df['_type']!= 'link']
    #merge/deduplicate similar topic/clusters
    new_df['keyword'] = new_df['keyword'].apply(remove_underscore)
    vc_2 = new_df['keyword'].value_counts()
    dups_2 = vc_2[vc_2 > 1]
    dup_lst_2 = list(dups_2.index[:])
    
    for dup_word in dup_lst_2:
        try:
            df_tbd = new_df[new_df['keyword'] == dup_word]
            cluster_key = list(df_tbd[df_tbd['type']=='Cluster']['key'])[0]
            topic_key = list(df_tbd[df_tbd['type']=='Topic']['key'])[0]
            df = df.replace(topic_key, cluster_key)
            index_to_drop = df_tbd[df_tbd['type']=='Topic'].index[0]
            index_to_change = df_tbd[df_tbd['type']=='Cluster'].index[0]
            df.loc[index_to_change]['_from'] = list(df_tbd[df_tbd['type']=='Topic']['_from'])[0]
            df.drop([index_to_drop], inplace=True)
        except:
            print(df_tbd)
    return df

def split_topic_link(df, link_key_val):
    df['reference'] = ''
    df_pre_topic = df[['key',
                     'type',
                     'keyword',
                     'definition',
                     'reference',
                     'wordnet_ID',
                     '_type']]

    df_pre_topic = df_pre_topic[df_pre_topic['_type'] != 'link']
    df_topic = df_pre_topic.iloc[:,:6]
    df_topic.rename(columns={"key": "_key", "type":"_type", "keyword": "title"}, inplace=True)
    df_topic['title'] = df_topic['title'].apply(capitalize_first_letter)
    df_topic['title'] = df_topic['title'].apply(remove_underscore)
    df_topic['definition'] = df_topic['definition'].apply(capitalize_first_letter)
    
    df_link = df[['_type','name','_from', '_to']]
    df_link['definition'] = ''
    df_link['_key'] = get_link_key(df_link, link_key_val)
    df_link = df_link[['_key','_type','name','definition','_from','_to']]
    
    return df_topic, df_link

def protocol_a_combine(df_topic, df_link, new_topics, new_links):
    topic_dict = df_topic.to_dict(orient='records')
    link_dict = df_link.to_dict(orient='records')
    topic_key_val = int(df_topic['_key'].iloc[-1][1:])+1
    link_key_val = int(df_link['_key'].iloc[-1][1:])+1
    new_topics = new_topics + topic_dict
    new_links = new_links + link_dict
    return new_topics, new_links, topic_key_val, link_key_val

def main():
	# Create list of topics
	new_topics = list()
	new_links = list()

	# Load and clean the data
	wos_data = pd.read_csv("wos_data.csv")
	wos_data = wos_data.fillna('')

	print("Creating clusters")
	cluster_runner = Convert_Clusters()
	cluster_topics, cluster_links, topic_key_val, link_key_val = cluster_runner.convert_clusters()
	new_topics = add_new_topics(new_topics, cluster_topics)
	new_links = add_new_links(new_links, cluster_links)

	print("Converting researchers")
	researcher_runner = Convert_Researchers()
	researcher_topics, researcher_links, topic_key_val, link_key_val = 	researcher_runner.convert_researchers(wos_data, topic_key_val, link_key_val)
	new_topics = add_new_topics(new_topics, researcher_topics)
	new_links = add_new_links(new_links, researcher_links)

	print("Converting publications")
	publication_runner = Convert_Publications()
	publication_topics, publication_links, topic_key_val, link_key_val = publication_runner.convert_publications(wos_data, topic_key_val, link_key_val)
	new_topics = add_new_topics(new_topics, publication_topics)
	new_links = add_new_links(new_links, publication_links)

	print("Converting journals")
	journal_runner = Convert_Journals()
	journal_topics, journal_links, topic_key_val, link_key_val = journal_runner.convert_journals(wos_data, topic_key_val, link_key_val, publication_topics)
	new_topics = add_new_topics(new_topics, journal_topics)
	new_links = add_new_links(new_links, journal_links)

	print("Converting articles")
	article_runner = Convert_Articles()
	article_topics, article_links, topic_key_val, link_key_val = article_runner.convert_articles(wos_data, topic_key_val, link_key_val, researcher_topics, publication_topics, journal_topics, journal_links)
	new_topics = add_new_topics(new_topics, article_topics)
	new_links = add_new_links(new_links, article_links)

	print("Converting events")
	event_runner = Convert_Events()
	event_topics, event_links, topic_key_val, link_key_val = event_runner.convert_events(wos_data, topic_key_val, link_key_val, article_topics)
	new_topics = add_new_topics(new_topics, event_topics)
	new_links = add_new_links(new_links, event_links)

	print("Converting organizations")
	organization_runner = Convert_Organizations()
	organization_topics, organization_links, topic_key_val, link_key_val = organization_runner.convert_organizations(wos_data, topic_key_val, link_key_val, researcher_topics, publication_topics)
	new_topics = add_new_topics(new_topics, organization_topics)
	new_links = add_new_links(new_links, organization_links)

	# Protocol A
	print("Classifying ISS Keywords")
	print("Protocol A")
	df_clean = read_clean('wos_data.csv')
	print("WordNet Extraction and Connecting Nodes")
	df = connect_nodes(df_clean, new_topics, topic_key_val)
	print("Removing and Merging duplicates")
	new_df, df = remove_duplicates(df)
	merged_df = merge_topic_cluster(new_df)
	print("Splitting topic and links")
	df_topic, df_link = split_topic_link(merged_df, link_key_val)
	print("Combining jsons")
	new_topics, new_links, topic_key_val,link_key_val = protocol_a_combine(df_topic, df_link, new_topics, new_links)

	print("Outputting to files")
	# Output topics to file
	output_to_file(new_topics, 'output/combined_topics.json')
	output_to_file(new_links, 'output/combined_links.json')

if __name__ == '__main__':
	main()