# -*- coding: utf-8 -*-

import requests
import re
import json

def extract_entry(entry):
	new_entry = dict()
	for key in entry.keys():
		if key == 'timestamp':
			new_entry['timestamp'] = entry[key]
		elif ('(qc)' in key):
			new_entry['clusters'] = entry[key]
		elif ('(qfn)' in key):
			new_entry['first_name'] = entry[key]
		elif ('(qln)' in key):
			new_entry['last_name'] = entry[key]
		elif ('(qk1)' in key):
			new_entry['c1Type'] = entry[key]
		elif ('(qk2)' in key):
			new_entry['c2Type'] = entry[key]
		elif ('(qk3)' in key):
			new_entry['c3Type'] = entry[key]
		elif ('(qk4)' in key):
			new_entry['c4Type'] = entry[key]
		elif ('(qk5)' in key):
			new_entry['c5Type'] = entry[key]
		elif ('(qg)' in key):
			new_entry['graph_name_def_url'] = entry[key]
		elif ('(qe)' in key):
			new_entry['person_email'] = entry[key]
		elif ('(qt1)' in key):
			new_entry['c1Topics'] = entry[key]
		elif ('(qt2)' in key):
			new_entry['c2Topics'] = entry[key]
		elif ('(qt3)' in key):
			new_entry['c3Topics'] = entry[key]
		elif ('(qt4)' in key):
			new_entry['c4Topics'] = entry[key]
		elif ('(qt5)' in key):
			new_entry['c5Topics'] = entry[key]
		elif ('(qp)' in key):
			new_entry['properties'] = entry[key]
		elif ('(qlt)' in key):
			new_entry['topics_to_topics'] = entry[key]
		elif ('(qlp)' in key):
			new_entry['topics_to_properties'] = entry[key]
		else:
			print(key)

	if new_entry['last_name'] != None:
		new_entry['person_name'] = new_entry['first_name'] + ' ' + new_entry['last_name']
	else:
		new_entry['person_name'] = new_entry['first_name']
	return new_entry

def extract_graph_data(str):
	# Name - definition - reference. Assuming no - in name
	graph_name = str[0 : str.find(' - ')].strip()
	str = str[str.find(graph_name + ' - ') + len(graph_name) + 3 : ]

	reference = str[str.rindex(' - ') + 3 :].strip()
	str = str[ : str.find(reference) - 3].strip()
	definition = str

	return graph_name, definition, reference

def extract_clusters(str, type1, type2, type3, type4, type5):
	# Title - <definition>, Title - <definition>
	# Regex gets a list of the titles
	expected_clusters = 1
	if type2 != 'None':
		expected_clusters += 1
	if type3 != 'None':
		expected_clusters += 1
	if type4 != 'None':
		expected_clusters += 1
	if type5 != 'None':
		expected_clusters += 1
		
	# Assume Title - <definition>
	p = re.compile(r'[A-Za-z 0-9]+ - <')
	c_titles_temp = (p.findall(str))
	if (len(c_titles_temp) != expected_clusters):
		# Try Title- <definition>
		p = re.compile(r'[A-Za-z 0-9]+- <')
		c_titles_temp = (p.findall(str))
		if (len(c_titles_temp) != expected_clusters):
			# Try Title -<definition>
			p = re.compile(r'[A-Za-z 0-9]+ -<')
			c_titles_temp = (p.findall(str))
			if (len(c_titles_temp) != expected_clusters):
				# Try Title-<definition> (errors may occur)
				p = re.compile(r'[A-Za-z 0-9]+-<')
				c_titles_temp = (p.findall(str))
				print("Potential issue with extracting clusters from " + str)


	clusters = dict()
	for idx, val in enumerate(c_titles_temp):
		props = dict()
		c_title = val[:-3].strip()
		if idx != len(c_titles_temp) - 1:
			definition = str[str.find(val) + len(val) - 1: str.find(c_titles_temp[idx + 1]) - 1]
			str = str.replace(definition + ',', '')
			str = str.replace(val[:-1].strip(), '').strip()
		else:
			str = str.replace(val[:-1].strip(), '').strip()
			definition = str
		# Remove < and > 
		definition = definition[1:-1]
		props['definition'] = definition

		if idx == 0:
			props['cluster_type'] = type1
		elif idx == 1:
			props['cluster_type'] = type2
		elif idx == 2:
			props['cluster_type'] = type3
		elif idx == 3:
			props['cluster_type'] = type4
		elif idx == 4:
			props['cluster_type'] = type5

		clusters[c_title] = props

	return clusters

def extract_properties(str):
	properties = dict()
	vals = str.split(',')
	for val in vals:
		val = val.strip()
		if '(' in val and ')' in val:
			valueType = val[val.find('(') + 1 : val.find(')')]
			val = val[ : val.find(valueType) - 2]
		else:
			valueType = 'string'

		properties[val] = valueType

	return properties

def extract_topics(str):
	topics = dict()

	p = re.compile(r'[A-Za-z 0-9]+ - <')
	t_titles_temp = (p.findall(str))
	for idx, val in enumerate(t_titles_temp):
		props = dict()
		t_title = val[:-4].strip()
		if idx != len(t_titles_temp) - 1:
			definition = str[str.find(val) + len(val) - 1: str.find(t_titles_temp[idx + 1]) - 1]
			str = str.replace(definition + ',', '')
			str = str.replace(val[:-1].strip(), '').strip()
		else:
			str = str.replace(val[:-1].strip(), '').strip()
			definition = str
		# Remove < and > 
		definition = definition[1:-1]
		topics[t_title] = definition

	return topics

def extract_t2t_links(str, topic_title_to_key):
	links = list()
	for title, key, in topic_title_to_key.items():
		str = str.replace(title, key[0])

	for link in str.split(';'):
		link = link.strip()
		from_ = link[ : link.find(',')].strip()
		to_ = link[link.find(',') + 1 :].strip()
		links.append([from_, to_])

	return links

def determine_link_name(t1_type, t2_type):
	if t1_type == 'People':
		if t2_type == 'People':
			return 'knows'
		elif t2_type == 'Organisations':
			return 'is employed by'
		elif t2_type == 'Skills':
			return 'specialises in'
		elif t2_type == 'Projects':
			return 'develops'
		elif t2_type == 'Locations':
			return 'is located in'
	elif t1_type == 'Organisations':
		if t2_type == 'People':
			return 'employs'
		elif t2_type == 'Skills':
			return 'specialises in'
		elif t2_type == 'Projects':
			return 'develops'
		elif t2_type == 'Locations':
			return 'is located in'
	elif t1_type == 'Skills':
		if t2_type == 'People':
			return 'is the speciality of'
		elif t2_type == 'Organisations':
			return 'is the speciality of'
		elif t2_type == 'Projects':
			return 'is required by'
	elif t1_type == 'Projects':
		if t2_type == 'People':
			return 'is developed by'
		elif t2_type == 'Organisations':
			return 'is developed by'
		elif t2_type == 'Skills':
			return 'requires'
		elif t2_type == 'Locations':
			return 'is located in'
	elif t1_type == 'Locations':
		if t2_type == 'People':
			return 'is the location of'
		elif t2_type == 'Organisations':
			return 'is the location of'
		elif t2_type == 'Projects':
			return 'is the location of'
		elif t2_type == 'Locations':
			return 'is located in'

	return ''

def extract_t2p_links(str, property_title_to_key, topic_title_to_key):
	links = list()
	lines = str.split(';')
	for line in lines:
		line = line.strip()
		for title, key, in topic_title_to_key.items():
			line = line.replace(title, key[0])

		for title, key in property_title_to_key.items():
			line = line.replace(title, key)

		attribs = line.split(' - ')
		if (len(attribs) < 3):
			continue
		else:
			from_ = attribs[0].strip()
			to_ = attribs[1].strip()
			value = attribs[2].strip()
			if (len(attribs) > 3):
				for a in attribs[3:]:
					value += a
			links.append([from_, to_, value])

	return links

def new_topic_key(topic_key_val):
	return 'T' + str(topic_key_val), topic_key_val + 1

def new_link_key(link_key_val):
	return 'L' + str(link_key_val), link_key_val + 1

def create_topic(properties):
	topic_json_struct = {}
	for prop, value in properties.items():
		if value != None:
			topic_json_struct[prop] = value
	return topic_json_struct
def create_link(properties):
	return create_topic(properties)

def output_to_file(info, file):
	with open(file, 'w', encoding='utf-8') as f:
		f.write('[')
		i = 0
		for topic in info:
			f.write(json.dumps(topic, ensure_ascii=False))
			if i != len(info) - 1:
				f.write(",\n")
			else:
				f.write('\n')
			i = i + 1
		f.write(']')


def main():
	form_api_url = 'https://v2-api.sheety.co/d065448ba1539c7a59b5a8aa995d4ee2/braneSheetConversion/formResponses1'
	data = requests.get(form_api_url).json()

	topic_key_val = 1
	link_key_val = 1
	new_topics = list()
	new_links = list()

	data_entries = list()
	graph_num = 0
	for entry in data['formResponses1']:
		graph_num += 1
		cluster_title_to_key = dict()
		cluster_num_to_key = dict()
		cluster_key_to_type = dict()

		property_title_to_key = dict()
		topic_title_to_key = dict()
		topic_key_to_type = dict()

		new_entry = extract_entry(entry)

		graph_title, definition, reference = extract_graph_data(new_entry['graph_name_def_url'])
		graph_creator = new_entry['person_name']
		graph_creator_email = new_entry['person_email']

		system_key, topic_key_val = new_topic_key(topic_key_val)
		topic_params = {'_key': system_key, '_type': 'system', 'title': graph_title, 'definition': definition, 'reference': reference, 'Graph creator': graph_creator, 'Email address': graph_creator_email, 'timestamp': entry['timestamp']}
		new_topics.append(create_topic(topic_params))

		clusters = extract_clusters(new_entry['clusters'], new_entry['c1Type'], new_entry['c2Type'], new_entry['c3Type'], new_entry['c4Type'], new_entry['c5Type'])
		idx = 1
		for cluster_title, cluster_props in clusters.items():
			cluster_def = cluster_props['definition']
			cluster_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': cluster_key, '_type': 'cluster', 'title': cluster_title, 'definition': cluster_def}
			new_topics.append(create_topic(topic_params))
			cluster_title_to_key[cluster_title] = cluster_key
			cluster_num_to_key[idx] = cluster_key
			cluster_key_to_type[cluster_key] = cluster_props['cluster_type']
			idx += 1

			# Link cluster to system
			link_key, link_key_val = new_link_key(link_key_val)
			link_params = {'_key': link_key,'_type': 'encompasses', '_from': system_key, '_to': cluster_key}
			new_links.append(create_link(link_params))

		properties = extract_properties(new_entry['properties'])
		for prop_title, prop_type in properties.items():
			property_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': property_key, '_type': 'property', 'title': prop_title, 'valueType': prop_type}
			new_topics.append(create_topic(topic_params))
			property_title_to_key[prop_title] = property_key

			# Link property to system
			link_key, link_key_val = new_link_key(link_key_val)
			link_params = {'_key': link_key,'_type': 'encompasses', '_from': system_key, '_to': property_key}
			new_links.append(create_link(link_params))
		
		t1_topics = extract_topics(new_entry['c1Topics'])
		t2_topics = extract_topics(new_entry['c2Topics'])
		t3_topics = extract_topics(new_entry['c3Topics'])
		t4_topics = extract_topics(new_entry['c4Topics'])
		t5_topics = extract_topics(new_entry['c5Topics'])

		for topic_title, topic_def in t1_topics.items():
			topic_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': topic_key, '_type': 'topic', 'title': topic_title, 'definition': topic_def}
			new_topics.append(create_topic(topic_params))

			# Link topic to cluster
			cluster_key = cluster_num_to_key.get(1)
			if cluster_key == None:
				print("Error getting cluster number 1 key")
			else:
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'hasInstance', '_from': cluster_key, '_to': topic_key}
				new_links.append(create_link(link_params))

				topic_key_to_type[topic_key] = cluster_key_to_type[cluster_key]
			topic_title_to_key[topic_title] = [topic_key, cluster_key]

		for topic_title, topic_def in t2_topics.items():
			topic_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': topic_key, '_type': 'topic', 'title': topic_title, 'definition': topic_def}
			new_topics.append(create_topic(topic_params))

			# Link topic to cluster
			cluster_key = cluster_num_to_key.get(2)
			if cluster_key == None:
				print("Error getting cluster number 2 key")
			else:
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'hasInstance', '_from': cluster_key, '_to': topic_key}
				new_links.append(create_link(link_params))
	
				topic_key_to_type[topic_key] = cluster_key_to_type[cluster_key]
			topic_title_to_key[topic_title] = [topic_key, cluster_key]
	
		for topic_title, topic_def in t3_topics.items():
			topic_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': topic_key, '_type': 'topic', 'title': topic_title, 'definition': topic_def}
			new_topics.append(create_topic(topic_params))

			# Link topic to cluster
			cluster_key = cluster_num_to_key.get(3)
			if cluster_key == None:
				print("Error getting cluster number 3 key")
			else:
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'hasInstance', '_from': cluster_key, '_to': topic_key}
				new_links.append(create_link(link_params))
				topic_key_to_type[topic_key] = cluster_key_to_type[cluster_key]

			topic_title_to_key[topic_title] = [topic_key, cluster_key]
	
		for topic_title, topic_def in t4_topics.items():
			topic_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': topic_key, '_type': 'topic', 'title': topic_title, 'definition': topic_def}
			new_topics.append(create_topic(topic_params))

			# Link topic to cluster
			cluster_key = cluster_num_to_key.get(4)
			if cluster_key != None:
				print("error getting cluster number 4 key")
			else:
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'hasInstance', '_from': cluster_key, '_to': topic_key}
				new_links.append(create_link(link_params))
				topic_key_to_type[topic_key] = cluster_key_to_type[cluster_key]

			topic_title_to_key[topic_title] = [topic_key, cluster_key]

		for topic_title, topic_def in t5_topics.items():
			topic_key, topic_key_val = new_topic_key(topic_key_val)
			topic_params = {'_key': topic_key, '_type': 'topic', 'title': topic_title, 'definition': topic_def}
			new_topics.append(create_topic(topic_params))

			# Link topic to cluster
			cluster_key = cluster_num_to_key.get(5)
			if cluster_key != None:
				print("error getting cluster number 5 key")
			else:
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'hasInstance', '_from': cluster_key, '_to': topic_key}
				new_links.append(create_link(link_params))
				topic_key_to_type[topic_key] = cluster_key_to_type[cluster_key]

			topic_title_to_key[topic_title] = [topic_key, cluster_key]

		topic_to_topic_links = extract_t2t_links(new_entry['topics_to_topics'], topic_title_to_key)
		for t2t_link in topic_to_topic_links:
			from_ = t2t_link[0]
			to_ = t2t_link[1]
			link_type = determine_link_name(topic_key_to_type.get(from_), topic_key_to_type.get(to_))
			if link_type != "":
				link_key, link_key_val = new_link_key(link_key_val)
				link_params = {'_key': link_key,'_type': 'link', '_from': from_, '_to': to_, 'name': link_type}
				new_links.append(create_link(link_params))

		topic_to_property_links = extract_t2p_links(new_entry['topics_to_properties'], property_title_to_key, topic_title_to_key)
		for t2p_link in topic_to_property_links:
			from_ = t2p_link[0]
			to_ = t2p_link[1]
			value = t2p_link[2]
			link_key, link_key_val = new_link_key(link_key_val)
			link_params = {'_key': link_key,'_type': 'has', '_from': from_, '_to': to_, 'value': value}
			new_links.append(create_link(link_params))

		print("Outputting to files")
		# Output topics to file
		topic_filename = 'output/form_topics' + str(graph_num) + '.json'
		link_filename = 'output/form_links' + str(graph_num) + '.json'
		output_to_file(new_topics, topic_filename)
		output_to_file(new_links, link_filename)
	

if __name__ == '__main__':
	main()