import re
from .analyzer import make_requests_no_file

data_dir = 'data/'

def find_topic_file(topic):
	filename = re.sub(' ', '_', topic) + '.txt'
	filename = data_dir + filename

	try:
		f = open(filename, encoding='utf-8', mode='r')
		return filename
	except FileNotFoundError:
		return False

def get_data_from_file(topic):
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