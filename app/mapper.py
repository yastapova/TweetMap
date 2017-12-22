import re
from .analyzer import make_requests_no_file

"""Directory in which to find data files on pre-processed topics."""
data_dir = 'data/'

def find_topic_file(topic):
	"""Determine if there exists a file with pre-processed data on the topic.

	Args:
		topic (str): topic for which to find a file

	Returns:
		str: filename if found
		False: if not found
	"""
	filename = re.sub(' ', '_', topic) + '.txt'
	filename = data_dir + filename

	try:
		f = open(filename, encoding='utf-8', mode='r')
		return filename
	except FileNotFoundError:
		return False

def get_data_from_file(topic):
	"""Get pre-processed data from a file on the given topic, if such
	a file exists.

	Args:
		topic (str): topic being searched

	Returns:
		dict: (str : list of float) list of data for each state
	"""
	data = {}
	filename = find_topic_file(topic)
	if not filename:
		return data

	with open(filename, encoding='utf-8', mode='r') as f:
		lines = f.readlines()

		for line in lines:
			abbrev, sent = line.split('\t')
			if(abbrev in data):
				data[abbrev].append(float(sent.strip()))
			else:
				data[abbrev] = [float(sent.strip())]

	return data

def get_fresh_data(topic, data):
	"""Performs a new search on Twitter for the given topic, and 
	incorporates it into any pre-processed data found.

	Args:
		topic (str): topic searched for on Twitter
		data (dict): (str : list of float) any pre-processed data found

	Returns:
		dict (str : list of float): data per state, including fresh data
	"""
	result = make_requests_no_file(topic)

	for tweet in result:
		state = tweet[0]
		sent = tweet[1]

		if(state in data):
			data[state].append(float(sent.strip()))
		else:
			data[state] = [float(sent.strip())]

	return data

def aggregate_data(data):
	"""Aggregates data by state by taking the average of sentiment scores.

	Args:
		data (dict): sentiment data list for each state

	Returns:
		dict (str : float): average sentiment per state
	"""
	total_sum = 0
	total_num = 0

	for state in data:
		state_sum = sum(data[state])
		state_num = len(data[state])

		total_sum += state_sum
		total_num += state_num

		if(state_num == 0):
			data[state] = 0
		else:
			data[state] = state_sum/state_num

	return data

def get_state_sentiments(topic):
	"""Get sentiment data per state and put it in a csv file to be read
	when the visualization is being created.

	Args:
		topic (str): topic to search for

	Returns:
		dict: average sentiment per state
	"""
	print('Getting tweets for: ' + topic)
	data = get_data_from_file(topic)
	print('Getting fresh data')
	data = get_fresh_data(topic, data)
	print('Aggregating data')
	data = aggregate_data(data)

	with open('app/static/map_data.csv', encoding='utf-8', mode='w') as f:
		f.write('state' + ',' + 'sentiment' + '\n')
		for d in data:
			f.write(d + ',' + str(data[d]) + '\n')

	return data