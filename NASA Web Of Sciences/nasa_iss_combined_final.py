'''
	Kaushik Tandon
	January - February 2020
	NASA Web Of Science + ISS conversion for The Brane
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
import warnings

nltk.download('wordnet')
warnings.filterwarnings('ignore')

class Convert_Clusters():
	def __init__(self):
		print("Create clusters")
	def convert_clusters(self):
		cluster_topics = list()
		cluster_links = list()
		properties = dict()

		final_topic = 0
		final_link = 0

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
		properties['title'] = "ISS research ecosystem"
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
		properties['title'] = "Other research organization"
		cluster_topics.append(self.create_topic(properties))
		# T23
		properties['_key'] = 'T23'
		properties['_type'] = 'cluster'
		properties['title'] = "Publisher"
		cluster_topics.append(self.create_topic(properties))
		# T24
		properties['_key'] = 'T24'
		properties['_type'] = 'cluster'
		properties['title'] = "Web of Science Keyword"
		cluster_topics.append(self.create_topic(properties))
		# T25
		properties['_key'] = 'T25'
		properties['_type'] = 'cluster'
		properties['title'] = 'Tagged Web of Science Keyword'
		cluster_topics.append(self.create_topic(properties))
		# T26
		properties['_key'] = 'T26'
		properties['_type'] = 'cluster'
		properties['title'] = 'Untagged Web of Science Keyword'
		cluster_topics.append(self.create_topic(properties))
		# T27
		properties['_key'] = 'T27'
		properties['_type'] = 'cluster'
		properties['title'] = 'ISS Investigation'
		cluster_topics.append(self.create_topic(properties))
		# T29
		properties['_key'] = 'T29'
		properties['_type'] = 'cluster'
		properties['title'] = 'Space agency'
		cluster_topics.append(self.create_topic(properties))
		# T30
		properties['_key'] = 'T30'
		properties['_type'] = 'cluster'
		properties['title'] = 'Sponsoring organization'
		cluster_topics.append(self.create_topic(properties))
		# T31
		properties['_key'] = 'T31'
		properties['_type'] = 'cluster'
		properties['title'] = 'Principal investigator'
		cluster_topics.append(self.create_topic(properties))
		# T32
		properties['_key'] = 'T32'
		properties['_type'] = 'cluster'
		properties['title'] = 'City'
		cluster_topics.append(self.create_topic(properties))
		# T33
		properties['_key'] = 'T33'
		properties['_type'] = 'cluster'
		properties['title'] = 'State'
		cluster_topics.append(self.create_topic(properties))
		# T34
		properties['_key'] = 'T34'
		properties['_type'] = 'cluster'
		properties['title'] = 'Country'
		cluster_topics.append(self.create_topic(properties))
		# T35
		properties['_key'] = 'T35'
		properties['_type'] = 'property'
		properties['title'] = 'Operations location'
		cluster_topics.append(self.create_topic(properties))
		# T36
		properties['_key'] = 'T36'
		properties['_type'] = 'cluster'
		properties['title'] = 'Academic activity'
		cluster_topics.append(self.create_topic(properties))
		# T37
		properties['_key'] = 'T37'
		properties['_type'] = 'cluster'
		properties['title'] = 'Location'
		cluster_topics.append(self.create_topic(properties))
		# T39
		properties['_key'] = 'T39'
		properties['_type'] = 'cluster'
		properties['title'] = 'Biology and Biotechnology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T40
		properties['_key'] = 'T40'
		properties['_type'] = 'cluster'
		properties['title'] = 'Animal Biology - Invertebrates investigation'
		cluster_topics.append(self.create_topic(properties))
		# T41
		properties['_key'] = 'T41'
		properties['_type'] = 'cluster'
		properties['title'] = 'Animal Biology - Vertebrates investigation'
		cluster_topics.append(self.create_topic(properties))
		# T42
		properties['_key'] = 'T42'
		properties['_type'] = 'cluster'
		properties['title'] = 'Cellular Biology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T43
		properties['_key'] = 'T43'
		properties['_type'] = 'cluster'
		properties['title'] = 'Macromolecular Crystal Growth investigation'
		cluster_topics.append(self.create_topic(properties))
		# T44
		properties['_key'] = 'T44'
		properties['_type'] = 'cluster'
		properties['title'] = 'Microbiology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T45
		properties['_key'] = 'T45'
		properties['_type'] = 'cluster'
		properties['title'] = 'Microencapsulation investigation'
		cluster_topics.append(self.create_topic(properties))
		# T46
		properties['_key'] = 'T46'
		properties['_type'] = 'cluster'
		properties['title'] = 'Plant Biology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T47
		properties['_key'] = 'T47'
		properties['_type'] = 'cluster'
		properties['title'] = 'Vaccine Development investigation'
		cluster_topics.append(self.create_topic(properties))
		# T48
		properties['_key'] = 'T48'
		properties['_type'] = 'cluster'
		properties['title'] = 'Earth and Space Science investigation'
		cluster_topics.append(self.create_topic(properties))
		# T49
		properties['_key'] = 'T49'
		properties['_type'] = 'cluster'
		properties['title'] = 'Astrobiology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T50
		properties['_key'] = 'T50'
		properties['_type'] = 'cluster'
		properties['title'] = 'Astrophysics investigation'
		cluster_topics.append(self.create_topic(properties))
		# T51
		properties['_key'] = 'T51'
		properties['_type'] = 'cluster'
		properties['title'] = 'Earth Remote Sensing investigation'
		cluster_topics.append(self.create_topic(properties))
		# T52
		properties['_key'] = 'T52'
		properties['_type'] = 'cluster'
		properties['title'] = 'Heliophysics investigation'
		cluster_topics.append(self.create_topic(properties))
		# T53
		properties['_key'] = 'T53'
		properties['_type'] = 'cluster'
		properties['title'] = 'Educational and cultural activities investigation'
		cluster_topics.append(self.create_topic(properties))
		# T54
		properties['_key'] = 'T54'
		properties['_type'] = 'cluster'
		properties['title'] = 'Classroom Versions of ISS Investigations investigation'
		cluster_topics.append(self.create_topic(properties))
		# T55
		properties['_key'] = 'T55'
		properties['_type'] = 'cluster'
		properties['title'] = 'Educational Competitions investigation'
		cluster_topics.append(self.create_topic(properties))
		# T56
		properties['_key'] = 'T56'
		properties['_type'] = 'cluster'
		properties['title'] = 'Educational Demonstrations investigation'
		cluster_topics.append(self.create_topic(properties))
		# T57
		properties['_key'] = 'T57'
		properties['_type'] = 'cluster'
		properties['title'] = 'Student-Developed Investigations investigation'
		cluster_topics.append(self.create_topic(properties))
		# T58
		properties['_key'] = 'T58'
		properties['_type'] = 'cluster'
		properties['title'] = 'Human Research investigation'
		cluster_topics.append(self.create_topic(properties))
		# T59
		properties['_key'] = 'T59'
		properties['_type'] = 'cluster'
		properties['title'] = 'Bone and Muscle Physiology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T60
		properties['_key'] = 'T60'
		properties['_type'] = 'cluster'
		properties['title'] = 'Cardiovascular and Respiratory Systems investigation'
		cluster_topics.append(self.create_topic(properties))
		# T61
		properties['_key'] = 'T61'
		properties['_type'] = 'cluster'
		properties['title'] = 'Crew Healthcare Systems investigation'
		cluster_topics.append(self.create_topic(properties))
		# T62
		properties['_key'] = 'T62'
		properties['_type'] = 'cluster'
		properties['title'] = 'Habitability and Human Factors investigation'
		cluster_topics.append(self.create_topic(properties))
		# T63
		properties['_key'] = 'T63'
		properties['_type'] = 'cluster'
		properties['title'] = 'Human Behavior and Performance investigation'
		cluster_topics.append(self.create_topic(properties))
		# T64
		properties['_key'] = 'T64'
		properties['_type'] = 'cluster'
		properties['title'] = 'Human Microbiome investigation'
		cluster_topics.append(self.create_topic(properties))
		# T65
		properties['_key'] = 'T65'
		properties['_type'] = 'cluster'
		properties['title'] = 'Immune System investigation'
		cluster_topics.append(self.create_topic(properties))
		# T66
		properties['_key'] = 'T66'
		properties['_type'] = 'cluster'
		properties['title'] = 'Integrated Physiology and Nutrition investigation'
		cluster_topics.append(self.create_topic(properties))
		# T67
		properties['_key'] = 'T67'
		properties['_type'] = 'cluster'
		properties['title'] = 'Nervous and Vestibular Systems investigation'
		cluster_topics.append(self.create_topic(properties))
		# T68
		properties['_key'] = 'T68'
		properties['_type'] = 'cluster'
		properties['title'] = 'Radiation Impacts on Humans investigation'
		cluster_topics.append(self.create_topic(properties))
		# T69
		properties['_key'] = 'T69'
		properties['_type'] = 'cluster'
		properties['title'] = 'Vision investigation'
		cluster_topics.append(self.create_topic(properties))
		# T70
		properties['_key'] = 'T70'
		properties['_type'] = 'cluster'
		properties['title'] = 'Physical science investigation'
		cluster_topics.append(self.create_topic(properties))
		# T71
		properties['_key'] = 'T71'
		properties['_type'] = 'cluster'
		properties['title'] = 'Combustion Science investigation'
		cluster_topics.append(self.create_topic(properties))
		# T72
		properties['_key'] = 'T72'
		properties['_type'] = 'cluster'
		properties['title'] = 'Complex Fluids investigation'
		cluster_topics.append(self.create_topic(properties))
		# T73
		properties['_key'] = 'T73'
		properties['_type'] = 'cluster'
		properties['title'] = 'Fluid Physics investigation'
		cluster_topics.append(self.create_topic(properties))
		# T74
		properties['_key'] = 'T74'
		properties['_type'] = 'cluster'
		properties['title'] = 'Fundamental Physics investigation'
		cluster_topics.append(self.create_topic(properties))
		# T75
		properties['_key'] = 'T75'
		properties['_type'] = 'cluster'
		properties['title'] = 'Materials Science investigation'
		cluster_topics.append(self.create_topic(properties))
		# T76
		properties['_key'] = 'T76'
		properties['_type'] = 'cluster'
		properties['title'] = 'Technology Development and Demonstration investigation'
		cluster_topics.append(self.create_topic(properties))
		# T77
		properties['_key'] = 'T77'
		properties['_type'] = 'cluster'
		properties['title'] = 'Air, Water and Surface Monitoring investigation'
		cluster_topics.append(self.create_topic(properties))
		# T78
		properties['_key'] = 'T78'
		properties['_type'] = 'cluster'
		properties['title'] = 'Avionics and Software investigation'
		cluster_topics.append(self.create_topic(properties))
		# T79
		properties['_key'] = 'T79'
		properties['_type'] = 'cluster'
		properties['title'] = 'Characterizing Experiment Hardware investigation'
		cluster_topics.append(self.create_topic(properties))
		# T80
		properties['_key'] = 'T80'
		properties['_type'] = 'cluster'
		properties['title'] = 'Commercial Demonstrations investigation'
		cluster_topics.append(self.create_topic(properties))
		# T81
		properties['_key'] = 'T81'
		properties['_type'] = 'cluster'
		properties['title'] = 'Communication and Navigation investigation'
		cluster_topics.append(self.create_topic(properties))
		# T82
		properties['_key'] = 'T82'
		properties['_type'] = 'cluster'
		properties['title'] = 'Fire Suppression and Detection investigation'
		cluster_topics.append(self.create_topic(properties))
		# T83
		properties['_key'] = 'T83'
		properties['_type'] = 'cluster'
		properties['title'] = 'Food and Clothing Systems investigation'
		cluster_topics.append(self.create_topic(properties))
		# T84
		properties['_key'] = 'T84'
		properties['_type'] = 'cluster'
		properties['title'] = 'Imaging Technology investigation'
		cluster_topics.append(self.create_topic(properties))
		# T85
		properties['_key'] = 'T85'
		properties['_type'] = 'cluster'
		properties['title'] = 'Life Support Systems and Habitation investigation'
		cluster_topics.append(self.create_topic(properties))
		# T86
		properties['_key'] = 'T86'
		properties['_type'] = 'cluster'
		properties['title'] = 'Microbial Populations in Spacecraft investigation'
		cluster_topics.append(self.create_topic(properties))
		# T87
		properties['_key'] = 'T87'
		properties['_type'] = 'cluster'
		properties['title'] = 'Microgravity Environment Measurement investigation'
		cluster_topics.append(self.create_topic(properties))
		# T88
		properties['_key'] = 'T88'
		properties['_type'] = 'cluster'
		properties['title'] = 'Radiation Measurements and Shielding investigation'
		cluster_topics.append(self.create_topic(properties))
		# T89
		properties['_key'] = 'T89'
		properties['_type'] = 'cluster'
		properties['title'] = 'Repair and Fabrication Technologies investigation'
		cluster_topics.append(self.create_topic(properties))
		# T90
		properties['_key'] = 'T90'
		properties['_type'] = 'cluster'
		properties['title'] = 'Robotics investigation'
		cluster_topics.append(self.create_topic(properties))
		# T91
		properties['_key'] = 'T91'
		properties['_type'] = 'cluster'
		properties['title'] = 'Small Satellites and Control Technologies investigation'
		cluster_topics.append(self.create_topic(properties))
		# T92
		properties['_key'] = 'T92'
		properties['_type'] = 'cluster'
		properties['title'] = 'Space Structures investigation'
		cluster_topics.append(self.create_topic(properties))
		# T93
		properties['_key'] = 'T93'
		properties['_type'] = 'cluster'
		properties['title'] = 'Spacecraft and Orbital Environments investigation'
		cluster_topics.append(self.create_topic(properties))
		# T94
		properties['_key'] = 'T94'
		properties['_type'] = 'cluster'
		properties['title'] = 'Spacecraft Materials investigation'
		cluster_topics.append(self.create_topic(properties))
		# T95
		properties['_key'] = 'T95'
		properties['_type'] = 'cluster'
		properties['title'] = 'Thermal Management Systems investigation'
		cluster_topics.append(self.create_topic(properties))
		# T96
		properties['_key'] = 'T96'
		properties['_type'] = 'cluster'
		properties['title'] = 'Wordnet ontology'
		cluster_topics.append(self.create_topic(properties))
		# T97
		properties['_key'] = 'T97'
		properties['_type'] = 'cluster'
		properties['title'] = 'University'
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
		properties['_to'] = 'T27'
		cluster_links.append(self.create_link(properties))
		# L3
		properties['_key'] = 'L3'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T36'
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
		# L19
		properties['_key'] = 'L19'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T21'
		properties['_to'] = 'T29'
		cluster_links.append(self.create_link(properties))
		# L20
		properties['_key'] = 'L20'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T21'
		properties['_to'] = 'T30'
		cluster_links.append(self.create_link(properties))
		# L21
		properties['_key'] = 'L21'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T2'
		properties['_to'] = 'T31'
		cluster_links.append(self.create_link(properties))
		# L22
		properties['_key'] = 'L22'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T37'
		properties['_to'] = 'T32'
		cluster_links.append(self.create_link(properties))
		# L23
		properties['_key'] = 'L23'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T37'
		properties['_to'] = 'T33'
		cluster_links.append(self.create_link(properties))
		# L24
		properties['_key'] = 'L24'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T37'
		properties['_to'] = 'T34'
		cluster_links.append(self.create_link(properties))
		# L25
		properties['_key'] = 'L25'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T39'
		cluster_links.append(self.create_link(properties))
		# L26
		properties['_key'] = 'L26'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T48'
		cluster_links.append(self.create_link(properties))
		# L27
		properties['_key'] = 'L27'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T53'
		cluster_links.append(self.create_link(properties))
		# L28
		properties['_key'] = 'L28'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T58'
		cluster_links.append(self.create_link(properties))
		# L29
		properties['_key'] = 'L29'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T70'
		cluster_links.append(self.create_link(properties))
		# L30
		properties['_key'] = 'L30'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T27'
		properties['_to'] = 'T76'
		cluster_links.append(self.create_link(properties))
		# L31
		properties['_key'] = 'L31'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T40'
		cluster_links.append(self.create_link(properties))
		# L32
		properties['_key'] = 'L32'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T41'
		cluster_links.append(self.create_link(properties))
		# L33
		properties['_key'] = 'L33'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T42'
		cluster_links.append(self.create_link(properties))
		# L34
		properties['_key'] = 'L34'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T43'
		cluster_links.append(self.create_link(properties))
		# L35
		properties['_key'] = 'L35'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T44'
		cluster_links.append(self.create_link(properties))
		# L36
		properties['_key'] = 'L36'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T45'
		cluster_links.append(self.create_link(properties))
		# L37
		properties['_key'] = 'L37'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T46'
		cluster_links.append(self.create_link(properties))
		# L38
		properties['_key'] = 'L38'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T39'
		properties['_to'] = 'T47'
		cluster_links.append(self.create_link(properties))
		# L39
		properties['_key'] = 'L39'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T48'
		properties['_to'] = 'T49'
		cluster_links.append(self.create_link(properties))
		# L40
		properties['_key'] = 'L40'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T48'
		properties['_to'] = 'T50'
		cluster_links.append(self.create_link(properties))
		# L41
		properties['_key'] = 'L41'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T48'
		properties['_to'] = 'T51'
		cluster_links.append(self.create_link(properties))
		# L42
		properties['_key'] = 'L42'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T48'
		properties['_to'] = 'T52'
		cluster_links.append(self.create_link(properties))
		# L43
		properties['_key'] = 'L43'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T53'
		properties['_to'] = 'T54'
		cluster_links.append(self.create_link(properties))
		# L44
		properties['_key'] = 'L44'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T53'
		properties['_to'] = 'T55'
		cluster_links.append(self.create_link(properties))
		# L45
		properties['_key'] = 'L45'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T53'
		properties['_to'] = 'T56'
		cluster_links.append(self.create_link(properties))
		# L46
		properties['_key'] = 'L46'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T53'
		properties['_to'] = 'T57'
		cluster_links.append(self.create_link(properties))
		# L47
		properties['_key'] = 'L47'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T59'
		cluster_links.append(self.create_link(properties))
		# L48
		properties['_key'] = 'L48'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T60'
		cluster_links.append(self.create_link(properties))
		# L49
		properties['_key'] = 'L49'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T61'
		cluster_links.append(self.create_link(properties))
		# L50
		properties['_key'] = 'L50'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T62'
		cluster_links.append(self.create_link(properties))
		# L51
		properties['_key'] = 'L51'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T63'
		cluster_links.append(self.create_link(properties))
		# L52
		properties['_key'] = 'L52'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T64'
		cluster_links.append(self.create_link(properties))
		# L53
		properties['_key'] = 'L53'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T65'
		cluster_links.append(self.create_link(properties))
		# L54
		properties['_key'] = 'L54'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T66'
		cluster_links.append(self.create_link(properties))
		# L55
		properties['_key'] = 'L55'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T67'
		cluster_links.append(self.create_link(properties))
		# L56
		properties['_key'] = 'L56'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T68'
		cluster_links.append(self.create_link(properties))
		# L57
		properties['_key'] = 'L57'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T58'
		properties['_to'] = 'T69'
		cluster_links.append(self.create_link(properties))
		# L58
		properties['_key'] = 'L58'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T70'
		properties['_to'] = 'T71'
		cluster_links.append(self.create_link(properties))
		# L59
		properties['_key'] = 'L59'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T70'
		properties['_to'] = 'T72'
		cluster_links.append(self.create_link(properties))
		# L60
		properties['_key'] = 'L60'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T70'
		properties['_to'] = 'T73'
		cluster_links.append(self.create_link(properties))
		# L61
		properties['_key'] = 'L61'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T70'
		properties['_to'] = 'T74'
		cluster_links.append(self.create_link(properties))
		# L62
		properties['_key'] = 'L62'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T70'
		properties['_to'] = 'T75'
		cluster_links.append(self.create_link(properties))
		# L63
		properties['_key'] = 'L63'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T77'
		cluster_links.append(self.create_link(properties))
		# L64
		properties['_key'] = 'L64'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T78'
		cluster_links.append(self.create_link(properties))
		# L65
		properties['_key'] = 'L65'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T79'
		cluster_links.append(self.create_link(properties))
		# L66
		properties['_key'] = 'L66'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T80'
		cluster_links.append(self.create_link(properties))
		# L67
		properties['_key'] = 'L67'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T81'
		cluster_links.append(self.create_link(properties))
		# L68
		properties['_key'] = 'L68'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T82'
		cluster_links.append(self.create_link(properties))
		# L69
		properties['_key'] = 'L69'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T83'
		cluster_links.append(self.create_link(properties))
		# L70
		properties['_key'] = 'L70'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T84'
		cluster_links.append(self.create_link(properties))
		# L71
		properties['_key'] = 'L71'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T85'
		cluster_links.append(self.create_link(properties))
		# L72
		properties['_key'] = 'L72'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T86'
		cluster_links.append(self.create_link(properties))
		# L73
		properties['_key'] = 'L73'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T87'
		cluster_links.append(self.create_link(properties))
		# L74
		properties['_key'] = 'L74'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T88'
		cluster_links.append(self.create_link(properties))
		# L75
		properties['_key'] = 'L75'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T89'
		cluster_links.append(self.create_link(properties))
		# L76
		properties['_key'] = 'L76'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T90'
		cluster_links.append(self.create_link(properties))
		# L77
		properties['_key'] = 'L77'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T91'
		cluster_links.append(self.create_link(properties))
		# L78
		properties['_key'] = 'L78'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T92'
		cluster_links.append(self.create_link(properties))
		# L79
		properties['_key'] = 'L79'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T93'
		cluster_links.append(self.create_link(properties))
		# L80
		properties['_key'] = 'L80'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T94'
		cluster_links.append(self.create_link(properties))
		# L81
		properties['_key'] = 'L81'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T76'
		properties['_to'] = 'T95'
		cluster_links.append(self.create_link(properties))
		# L82
		properties['_key'] = 'L82'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T36'
		properties['_to'] = 'T4'
		cluster_links.append(self.create_link(properties))
		# L83
		properties['_key'] = 'L83'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T36'
		properties['_to'] = 'T10'
		cluster_links.append(self.create_link(properties))
		# L84
		properties['_key'] = 'L84'
		properties['_type'] = 'encompasses'
		properties['_from'] = 'T1'
		properties['_to'] = 'T96'
		cluster_links.append(self.create_link(properties))
		# L85
		properties['_key'] = 'L85'
		properties['_type'] = 'hasSubclass'
		properties['_from'] = 'T21'
		properties['_to'] = 'T97'
		cluster_links.append(self.create_link(properties))

		# Change this if more links added!
		final_link = 85

		# T28, T38 missing
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
	def post_process_organizations(self, organization_topics, organization_links, link_key_val):
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

		for topic in organization_topics:
			if 'University' in topic['title'] or 'College' in topic['title']:
				# (1.1) Link to university
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1
				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['definition'] = ''
				link_json_struct['_from'] = 'T97' 
				link_json_struct['_to'] = topic['_key']
				# Store in list to output at end
				organization_links.append(link_json_struct)

		return organization_topics, organization_links, link_key_val

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
		organization_topics, organization_links, link_key_val = self.post_process_organizations(organization_topics, organization_links, link_key_val)
		return organization_topics, organization_links, topic_key_val, link_key_val

class Convert_Investigations():
	def __init__(self):
		print("ISS - Convert Investigations")
	def convert_investigations(self, data, topic_key_val, link_key_val, subcategory_topics, article_topics):
		investigation_topics = list()
		investigation_links = list()

		# Preprocess by mapping article DOI to article key
		article_topic_doi_to_key = dict()
		for article_topic_json in article_topics:
			article_topic_doi_to_key[article_topic_json['DOI']] = article_topic_json["_key"]

		for rowidx in range(len(data)):
			# Get current row in dataset
			investigation_row = data.iloc[rowidx,:]
			_type = "topic"
			topic_title = investigation_row['Name']
			definition = topic_title + " - " + investigation_row['PAOSummary']
			terms = [topic_title, investigation_row['PAOSummary']]
			pst_id = investigation_row['PST ID']
			# Look for duplicates
			duplicate = False
			for topic in investigation_topics:
				if topic['title'] == topic_title:
					duplicate = True
			# Skip making a topic for this publication
			if (duplicate):
				continue

			topic_key = 'T' + str(topic_key_val)
			# Increment key value for next topic
			topic_key_val = topic_key_val + 1

			# (1) Output investigation topic to JSON format
			topic_json_struct = {}
			topic_json_struct['_key'] = topic_key
			topic_json_struct["_type"] = _type
			topic_json_struct['title'] = topic_title
			topic_json_struct['definition'] = definition
			topic_json_struct['terms'] = terms
			topic_json_struct['PST ID'] = str(pst_id)
			topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

			# Store in list to output at end
			investigation_topics.append(topic_json_struct)

			# (3) Link between subcategory and investigation ID
			found = False
			subcategory_id = -1
			title_to_check = investigation_row['Subcategory'] + " investigation"
			for subcategory_topic_json in subcategory_topics:
				if subcategory_topic_json['title'] == title_to_check:
					found = True
					subcategory_id = subcategory_topic_json['_key']
			if found:
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['_from'] = subcategory_id 
				link_json_struct['_to'] = topic_key

				# Store in list to output at end
				investigation_links.append(link_json_struct)

			# (8) Link between Operations and investigation ID
			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1

			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'has'
			link_json_struct['name'] = ''
			link_json_struct['_from'] = topic_key 
			link_json_struct['_to'] = 'T35'
			link_json_struct['value'] = investigation_row['OperationsLocation']

			# Store in list to output at end
			investigation_links.append(link_json_struct)

			# (21) Link between investigation ID and article ID
			for i in range(1, 46):
				doi = investigation_row['DOI' + str(i)]
				if (doi == ''): break
				article_key = article_topic_doi_to_key.get(doi)
				if (article_key != None):
					link_key = 'L' + str(link_key_val)
					# Increment key value for next link
					link_key_val = link_key_val + 1

					link_json_struct = {}
					link_json_struct['_key'] = link_key
					link_json_struct['_type'] = 'link'
					link_json_struct['name'] = 'outputs'
					link_json_struct['_from'] = topic_key 
					link_json_struct['_to'] = article_key
					investigation_links.append(link_json_struct)
				
		return investigation_topics, investigation_links, topic_key_val, link_key_val
class Convert_Sponsoring_Space_Agencies():
	def __init__(self):
		print("ISS - Convert Sponsoring Space Agencies")
	def post_process_space_agencies(self, sponsoring_space_agency_topics, sponsoring_space_agency_links, research_organization_topics, research_organization_links, topic_key_val, link_key_val):
		# Post process based off research_organization_topics (Protocol G)
		topics_to_delete = list()
		links_to_delete = list()
		new_links = list()
		duplicated_links_dict = dict()
		print("Post processing space agencies")
		nasa_key = None
		for topic in sponsoring_space_agency_topics:
			if ("NASA" in topic['title']):
				nasa_key = topic['_key']
		for topic in research_organization_topics:
			if ("Nasa" in topic['title']):
				topics_to_delete.append(topic)
				for link in research_organization_links:
					if link['_to'] == topic['_key']:
						links_to_delete.append(link)
						if link['_type'] != 'hasInstance' and duplicated_links_dict.get((link['_from'], nasa_key)) == None:
							link_key = 'L' + str(link_key_val)
							# Increment key value for next link
							link_key_val = link_key_val + 1

							link_json_struct = {}
							link_json_struct['_key'] = link_key
							link_json_struct['_type'] = link['_type']
							link_json_struct['name'] = ''
							link_json_struct['_from'] = link['_from'] 
							link_json_struct['_to'] = nasa_key
							new_links.append(link_json_struct)
							duplicated_links_dict[(link['_from'], nasa_key)] = 1

		return topics_to_delete, links_to_delete, new_links, topic_key_val, link_key_val
	def convert_sponsoring_space_agencies(self, data, topic_key_val, link_key_val, investigation_topics):
		sponsoring_space_agency_topics = list()
		sponsoring_space_agency_links = list()
		for rowidx in range(len(data)):
			# Get current row in dataset
			agency_row = data.iloc[rowidx,:]
			topic_title = agency_row['SponsoringSpaceAgency']
			abrev = topic_title[topic_title.find('(') + 1 : topic_title.find(')')]
			terms = [topic_title, abrev]		
			# Look for duplicates
			duplicate = False
			topic_key = None
			for topic in sponsoring_space_agency_topics:
				if topic['title'] == topic_title:
					duplicate = True
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					topic_key = topic['_key']
			# Make a new topic if not duplicate
			if (not duplicate):

				topic_key = 'T' + str(topic_key_val)
				# Increment key value for next topic
				topic_key_val = topic_key_val + 1

				# (4a) Create topic for sponsoring agency
				topic_json_struct = {}
				topic_json_struct['_key'] = topic_key
				topic_json_struct["_type"] = 'topic'
				topic_json_struct['title'] = topic_title
				topic_json_struct['definition'] = ''
				topic_json_struct['terms'] = terms
				topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

				sponsoring_space_agency_topics.append(topic_json_struct)

				# (4b) Link sponsoring agency to cluster T29
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['_from'] = 'T29' 
				link_json_struct['_to'] = topic_key

				sponsoring_space_agency_links.append(link_json_struct)

			# (4c) Link between SponsoringSpaceAgency and investigation ID
			# Find corresponding topic in investigation_topics
			my_row = "row " + str(rowidx + 2) + ','
			my_row2 = "row " + str(rowidx + 2)
			temporary_topic_struct = {}
			for topic in investigation_topics:
				if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
					temporary_topic_struct = topic
					break
			investigation_key = temporary_topic_struct['_key']

			link_key = 'L' + str(link_key_val)
			# Increment key value for next link
			link_key_val = link_key_val + 1

			# Output link to JSON format
			link_json_struct = {}
			link_json_struct['_key'] = link_key
			link_json_struct['_type'] = 'link'
			link_json_struct['name'] = 'sponsors'
			link_json_struct['definition'] = ''
			link_json_struct['_from'] = topic_key 
			link_json_struct['_to'] = investigation_key

			# Store in list to output at end
			sponsoring_space_agency_links.append(link_json_struct)

		return sponsoring_space_agency_topics, sponsoring_space_agency_links, topic_key_val, link_key_val

class Convert_Sponsoring_Space_Organizations():
	def __init__(self):
		print("ISS - Convert Sponsoring Space Organizations")
	def convert_sponsoring_space_organizations(self, data, topic_key_val, link_key_val, investigation_topics, sponsoring_space_agency_topics):
		sponsoring_space_organization_topics = list()
		sponsoring_space_organization_links = list()

		nasa_key = None
		for topic in sponsoring_space_agency_topics:
			if topic['title'] == 'National Aeronautics and Space Administration (NASA)':
				nasa_key = topic['_key']
				break

		for rowidx in range(len(data)):
			# Get current row in dataset
			agency_row = data.iloc[rowidx,:]
			topic_title = agency_row['SponsoringOrganization']
			# Don't need to create a topic for this organization
			if topic_title == "Not Applicable":
				continue
			abrev = topic_title[topic_title.find('(') + 1 : topic_title.find(')')]
			terms = [topic_title, abrev]		
			# Look for duplicates
			duplicate = False
			topic_key = None
			matched_with_space_agency = False
			for topic in sponsoring_space_agency_topics:
				if topic['title'] == topic_title:
					matched_with_space_agency = True
					topic_key = topic['_key']
			# Will be overwritten if duplicate
			for topic in sponsoring_space_organization_topics:
				if topic['title'] == topic_title:
					duplicate = True
					topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
					topic_key = topic['_key']
			# Make a new topic if not duplicate
			if (not duplicate and not matched_with_space_agency):

				topic_key = 'T' + str(topic_key_val)
				# Increment key value for next topic
				topic_key_val = topic_key_val + 1

				# (5) Create topic for sponsoring organization
				topic_json_struct = {}
				topic_json_struct['_key'] = topic_key
				topic_json_struct["_type"] = 'topic'
				topic_json_struct['title'] = topic_title
				topic_json_struct['definition'] = ''
				topic_json_struct['terms'] = terms
				topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

				sponsoring_space_organization_topics.append(topic_json_struct)

				# (6) Link sponsoring agency to cluster T30
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['_from'] = 'T30' 
				link_json_struct['_to'] = topic_key

				sponsoring_space_organization_links.append(link_json_struct)

				# (6a) Check if links with NASA
				if ('NASA' in topic_title):
					link_key = 'L' + str(link_key_val)
					# Increment key value for next link
					link_key_val = link_key_val + 1

					link_json_struct = {}
					link_json_struct['_key'] = link_key
					link_json_struct['_type'] = 'is affiliated with'
					link_json_struct['name'] = ''
					link_json_struct['_from'] = nasa_key 
					link_json_struct['_to'] = topic_key

					sponsoring_space_organization_links.append(link_json_struct)
			if (matched_with_space_agency):
				# (5) Link sponsoring agency to cluster T30
				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'hasInstance'
				link_json_struct['name'] = ''
				link_json_struct['_from'] = 'T30' 
				link_json_struct['_to'] = topic_key

				sponsoring_space_organization_links.append(link_json_struct)
			else:
				# (7) Link between SponsoringAgency and investigation ID
				# Find corresponding topic in investigation_topics
				my_row = "row " + str(rowidx + 2) + ','
				my_row2 = "row " + str(rowidx + 2)
				temporary_topic_struct = {}
				for topic in investigation_topics:
					if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
						temporary_topic_struct = topic
						break
				investigation_key = temporary_topic_struct['_key']

				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'link'
				link_json_struct['name'] = 'sponsors'
				link_json_struct['definition'] = ''
				link_json_struct['_from'] = topic_key 
				link_json_struct['_to'] = investigation_key

				# Store in list to output at end
				sponsoring_space_organization_links.append(link_json_struct)

		# Post process to fix a broken character
		for topic in sponsoring_space_organization_topics:
			topic['title'] = topic['title'].replace('\u2013', '-')
			topic['terms'][0] = topic['terms'][0].replace('\u2013', '-')

		return sponsoring_space_organization_topics, sponsoring_space_organization_links, topic_key_val, link_key_val

class Convert_Principal_Investigators():
	def __init__(self):
		print("ISS - Convert Principal Investigators")
	def convert_principal_investigators(self, data, topic_key_val, link_key_val, investigation_topics):
		principal_investigator_topics = list()
		principal_investigator_links = list()

		# This dict will tell us if links are already going to be created. Keyed by (from, to), value doesn't matter
		duplicated_links_dict = dict()

		for rowidx in range(len(data)):
			# Get current row in dataset
			investigation_row = data.iloc[rowidx,:]
			pis_in_row = [(investigation_row['PI1-FN'], investigation_row['PI1-LN'], investigation_row['PI1-City'], investigation_row['PI1-State'], investigation_row['PI1-Country']),
			 			  (investigation_row['PI2-FN'], investigation_row['PI2-LN'], investigation_row['PI2-City'], investigation_row['PI2-State'], investigation_row['PI2-Country']),
			 			  (investigation_row['PI3-FN'], investigation_row['PI3-LN'], investigation_row['PI3-City'], investigation_row['PI3-State'], investigation_row['PI3-Country']),
			 			  (investigation_row['PI4-FN'], investigation_row['PI4-LN'], investigation_row['PI4-City'], investigation_row['PI4-State'], investigation_row['PI4-Country']),
			 			  (investigation_row['PI5-FN'], investigation_row['PI5-LN'], investigation_row['PI5-City'], investigation_row['PI5-State'], investigation_row['PI5-Country']),
			 			  (investigation_row['PI6-FN'], investigation_row['PI6-LN'], investigation_row['PI6-City'], investigation_row['PI6-State'], investigation_row['PI6-Country']),
			 			  (investigation_row['PI7-FN'], investigation_row['PI7-LN'], investigation_row['PI7-City'], investigation_row['PI7-State'], investigation_row['PI7-Country'])]
			for idx, pi in enumerate(pis_in_row):
				if(pi[0] == '' or pi[1] == ''): # No info for name, just skip this entry
					continue
				if(',' in pi[0]):
					name = pi[0][:pi[0].find(',')]
					first_name = name.split(" ")[0]
					last_name = name.split(" ")[1]
				else:
					first_name = pi[0]
					last_name = pi[1]
				topic_title = first_name + " " + last_name
				initials = first_name[0] + "." + last_name[0] + "."
				terms = [topic_title, last_name, initials]
				# (9) Create topic for this PI if doesn't already exist
				# Look for duplicates
				duplicate = False
				investigator_topic_key = None
				for topic in principal_investigator_topics:
					if topic['title'] == topic_title:
						duplicate = True
						topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
						investigator_topic_key = topic['_key']
				# Make a new topic if not duplicate
				if (not duplicate):

					investigator_topic_key = 'T' + str(topic_key_val)
					# Increment key value for next topic
					topic_key_val = topic_key_val + 1
					topic_json_struct = {}
					topic_json_struct['_key'] = investigator_topic_key
					topic_json_struct["_type"] = 'individual'
					topic_json_struct['title'] = first_name + " " + last_name
					topic_json_struct['firstName'] = first_name 
					topic_json_struct['lastName'] = last_name
					topic_json_struct['initials'] = initials
					topic_json_struct['terms'] = terms
					topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

					principal_investigator_topics.append(topic_json_struct)

					# (10) Link PI to cluster T31
					link_key = 'L' + str(link_key_val)
					# Increment key value for next link
					link_key_val = link_key_val + 1

					link_json_struct = {}
					link_json_struct['_key'] = link_key
					link_json_struct['_type'] = 'hasInstance'
					link_json_struct['name'] = ''
					link_json_struct['_from'] = 'T31' 
					link_json_struct['_to'] = investigator_topic_key

					principal_investigator_links.append(link_json_struct)
				# (11) Link between PI and investigation ID
				# Find corresponding topic in investigation_topics
				my_row = "row " + str(rowidx + 2) + ','
				my_row2 = "row " + str(rowidx + 2)
				temporary_topic_struct = {}
				for topic in investigation_topics:
					if my_row in topic['sources'] or topic['sources'].endswith(my_row2):
						temporary_topic_struct = topic
						break
				investigation_key = temporary_topic_struct['_key']

				link_key = 'L' + str(link_key_val)
				# Increment key value for next link
				link_key_val = link_key_val + 1

				definition = topic_title + " is the "
				if (idx == 0):
					definition += "first"
				elif (idx == 1):
					definition += "second"
				elif (idx == 2):
					definition += "third"
				elif (idx == 3):
					definition += "fourth"
				elif (idx == 4):
					definition += "fifth"
				elif (idx == 5):
					definition += "sixth"
				elif (idx == 6):
					definition += "seventh"
				definition += " person responsible for " + temporary_topic_struct['title']

				# Output link to JSON format
				link_json_struct = {}
				link_json_struct['_key'] = link_key
				link_json_struct['_type'] = 'link'
				link_json_struct['name'] = 'leads'
				link_json_struct['definition'] = definition
				link_json_struct['_from'] = investigator_topic_key 
				link_json_struct['_to'] = investigation_key

				# Store in list to output at end
				principal_investigator_links.append(link_json_struct)

				# (12) Create topic for city if not duplicate
				topic_title = pi[2]
				if (topic_title != ''):
					duplicate = False
					city_topic_key = None
					for topic in principal_investigator_topics:
						if topic['title'] == topic_title:
							duplicate = True
							if (', row ' + str(rowidx + 2) not in topic['sources']):
								topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
							city_topic_key = topic['_key']
					# Make a new topic if not duplicate
					if (not duplicate):
						city_topic_key = 'T' + str(topic_key_val)
						# Increment key value for next topic
						topic_key_val = topic_key_val + 1
						topic_json_struct = {}
						topic_json_struct['_key'] = city_topic_key
						topic_json_struct["_type"] = 'topic'
						topic_json_struct['title'] = topic_title
						topic_json_struct['terms'] = [topic_title]
						topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

						principal_investigator_topics.append(topic_json_struct)

						# (13) Link PI city to cluster T32
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'hasInstance'
						link_json_struct['name'] = ''
						link_json_struct['_from'] = 'T32' 
						link_json_struct['_to'] = city_topic_key

						principal_investigator_links.append(link_json_struct)

					# (14) Link PI to city if link doesn't already exist
					if (duplicated_links_dict.get((investigator_topic_key, city_topic_key)) == None):
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'link'
						link_json_struct['name'] = 'is located in'
						link_json_struct['_from'] = investigator_topic_key
						link_json_struct['_to'] = city_topic_key

						principal_investigator_links.append(link_json_struct)
						duplicated_links_dict[(investigator_topic_key, city_topic_key)] = 1

				# (15) Create topic for state if not duplicate
				topic_title = pi[3]
				if (topic_title != ""):
					duplicate = False
					state_topic_key = None
					for topic in principal_investigator_topics:
						if topic['title'] == topic_title:
							duplicate = True
							if (', row ' + str(rowidx + 2) not in topic['sources']):
								topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
							state_topic_key = topic['_key']
					# Make a new topic if not duplicate
					if (not duplicate):
						state_topic_key = 'T' + str(topic_key_val)
						# Increment key value for next topic
						topic_key_val = topic_key_val + 1
						topic_json_struct = {}
						topic_json_struct['_key'] = state_topic_key
						topic_json_struct["_type"] = 'topic'
						topic_json_struct['title'] = topic_title
						topic_json_struct['terms'] = [topic_title]
						topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

						principal_investigator_topics.append(topic_json_struct)

						# (16) Link PI state to cluster T33
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'hasInstance'
						link_json_struct['name'] = ''
						link_json_struct['_from'] = 'T33' 
						link_json_struct['_to'] = state_topic_key

						principal_investigator_links.append(link_json_struct)

					# (17) Link city to state if link doesn't already exist
					if (duplicated_links_dict.get((city_topic_key, state_topic_key)) == None):
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'link'
						link_json_struct['name'] = 'is located in'
						link_json_struct['_from'] = city_topic_key
						link_json_struct['_to'] = state_topic_key

						principal_investigator_links.append(link_json_struct)
						duplicated_links_dict[(city_topic_key, state_topic_key)] = 1
				# (18) Create topic for country if not duplicate
				topic_title = pi[4]
				if (topic_title != ""):
					duplicate = False
					country_topic_key = None
					for topic in principal_investigator_topics:
						if topic['title'] == topic_title:
							duplicate = True
							if (', row ' + str(rowidx + 2) not in topic['sources']):
								topic['sources'] = topic['sources'] + ', row ' + str(rowidx + 2)
							country_topic_key = topic['_key']
					# Make a new topic if not duplicate
					if (not duplicate):
						country_topic_key = 'T' + str(topic_key_val)
						# Increment key value for next topic
						topic_key_val = topic_key_val + 1
						topic_json_struct = {}
						topic_json_struct['_key'] = country_topic_key
						topic_json_struct["_type"] = 'topic'
						topic_json_struct['title'] = topic_title
						topic_json_struct['terms'] = [topic_title]
						topic_json_struct['sources'] = "Investigations, row " + str(rowidx + 2)

						principal_investigator_topics.append(topic_json_struct)

						# (19) Link PI country to cluster T34
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'hasInstance'
						link_json_struct['name'] = ''
						link_json_struct['_from'] = 'T34' 
						link_json_struct['_to'] = country_topic_key

						principal_investigator_links.append(link_json_struct)
					if (pi[3] == ''):
						key_to_use = city_topic_key
					else:
						key_to_use = state_topic_key
					# (20) Link city/state to country if link doesn't already exist
					if (duplicated_links_dict.get((key_to_use, country_topic_key)) == None):
						link_key = 'L' + str(link_key_val)
						# Increment key value for next link
						link_key_val = link_key_val + 1

						link_json_struct = {}
						link_json_struct['_key'] = link_key
						link_json_struct['_type'] = 'link'
						link_json_struct['name'] = 'is located in'
						link_json_struct['_from'] = key_to_use
						link_json_struct['_to'] = country_topic_key

						principal_investigator_links.append(link_json_struct)
						duplicated_links_dict[(key_to_use, country_topic_key)] = 1
				
		return principal_investigator_topics, principal_investigator_links, topic_key_val, link_key_val

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

def delete_topics(old_topics, topics_to_delete):
	for topic in topics_to_delete:
		old_topics.remove(topic)
	return old_topics

def delete_links(old_links, links_to_delete):
	for link in links_to_delete:
		print("DELETING: " + link["_to"] + " to " + link['_from'])
		old_links.remove(link)
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

    df_explode_unique = df_explode.drop_duplicates(['keywords'])
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

def find_missing_links(topics, links):
	topic_ids = set()
	removed_links = list()
	link_ids = set()
	for topic in topics:
		if topic['_key'] in topic_ids:
			print(topic)
		topic_ids.add(topic['_key'])
	for link in links:
		if link['_key'] in link_ids:
			print(link)
		link_ids.add(link['_key'])
	removed_links = [link for link in links if (link['_from'] not in topic_ids or link['_to'] not in topic_ids)]
	links = [link for link in links if (link['_from'] in topic_ids and link['_to'] in topic_ids)]
	return topics, links, removed_links

def main():
	# Create list of topics
	new_topics = list()
	new_links = list()

	# Load and clean the data
	wos_data = pd.read_csv("wos_data.csv")
	wos_data = wos_data.fillna('')
	wos_data.drop_duplicates('DI')

	iss_data = pd.read_csv("iss_data.csv")
	iss_data = iss_data.fillna('')

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
	print("Splitting topic and links")
	df_topic, df_link = split_topic_link(df, link_key_val)
	print("Combining jsons")
	new_topics, new_links, topic_key_val,link_key_val = protocol_a_combine(df_topic, df_link, new_topics, new_links)
	
	# ---- ISS	----
	print("Converting investigations")
	# Step 1 - 3, 8, 21
	investigation_runner = Convert_Investigations()
	investigation_topics, investigation_links, topic_key_val, link_key_val = investigation_runner.convert_investigations(iss_data, topic_key_val, link_key_val, cluster_topics, article_topics)
	new_topics = add_new_topics(new_topics, investigation_topics)
	new_links = add_new_links(new_links, investigation_links)

	print("Converting Sponsoring Space Agencies")
	# Step 4
	ssa_runner = Convert_Sponsoring_Space_Agencies()
	sponsoring_space_agency_topics, sponsoring_space_agency_links, topic_key_val, link_key_val = ssa_runner.convert_sponsoring_space_agencies(iss_data, topic_key_val, link_key_val, investigation_topics)
	deleted_topics, deleted_links, new_nasa_links, topic_key_val, link_key_val = ssa_runner.post_process_space_agencies(sponsoring_space_agency_topics, sponsoring_space_agency_links, organization_topics, organization_links, topic_key_val, link_key_val)
	new_topics = delete_topics(new_topics, deleted_topics)
	new_links = delete_links(new_links, deleted_links)

	new_topics = add_new_topics(new_topics, sponsoring_space_agency_topics)
	new_links = add_new_links(new_links, sponsoring_space_agency_links)
	new_links = add_new_links(new_links, new_nasa_links)

	print("Converting Sponsoring Space Organizations")
	# Step 5 - 7
	sso_runner = Convert_Sponsoring_Space_Organizations()
	sponsoring_space_organization_topics, sponsoring_space_organization_links, topic_key_val, link_key_val = sso_runner.convert_sponsoring_space_organizations(iss_data, topic_key_val, link_key_val, investigation_topics, sponsoring_space_agency_topics)
	new_topics = add_new_topics(new_topics, sponsoring_space_organization_topics)
	new_links = add_new_links(new_links, sponsoring_space_organization_links)

	print("Converting principal investigators")
	# Step 9 - 20
	pi_runner = Convert_Principal_Investigators()
	principal_investigator_topics, principal_investigator_links, topic_key_val, link_key_val = pi_runner.convert_principal_investigators(iss_data, topic_key_val, link_key_val, investigation_topics)
	new_topics = add_new_topics(new_topics, principal_investigator_topics)
	new_links = add_new_links(new_links, principal_investigator_links)

	new_topics, new_links, missing_links = find_missing_links(new_topics, new_links)

	print("Outputting to files")
	# Output topics to file
	output_to_file(new_topics, 'output/topic_output.json')
	output_to_file(new_links, 'output/link_output.json')
	output_to_file(missing_links, 'output/links_removed.json')


if __name__ == '__main__':
	main()