import re, urllib, random
import twitter
import geopy, us
from textblob import TextBlob

import keys
from locations import locations
from config import SAMPLE_QUERIES

"""Twitter API object used for search queries."""
api = twitter.Api(consumer_key=keys.CONSUMER_KEY,
                  consumer_secret=keys.CONSUMER_SECRET,
                  access_token_key=keys.ACCESS_TOKEN_KEY,
                  access_token_secret=keys.ACCESS_TOKEN_SECRET)

"""Geocoder object used for finding US state based on coordinates."""
geoloc = geopy.geocoders.Nominatim()

# # #  UTILS  # # #

def append_to_file(filename, data):
	"""Appends a line to a file.

	Args:
		filename (str): name of the file to write to
		data (str): string to write
	"""
	with open(filename, encoding="utf-8", mode="a") as f:
		f.write(data)

def clean_data(data):
	"""Processes a tuple containing data about a tweet. The tuple has two
	elements: (location, sentiment). This function joins them with a tab
	character and adds a newline character to the end.

	Args:
		data (tuple of str): (state abbreviation, sentiment value)

	Returns:
		str: data in the form of a one-line string
	"""
	loc = data[0]
	sent = data[1]

	data = (loc, sent)
	data = '\t'.join(data)
	data = data + '\n'
	return data

def process_tweet(tweet):
	"""Gets the location and sentiment of a given tweet. If no location is
	found, returns None.

	Args:
		tweet (dict): all tweet data in the form of a dictionary

	Returns:
		tuple (str, str): the location and sentiment of the tweet
		None: if the location of the tweet is not found
	"""
	loc = get_location(tweet)
	if(loc == '' or loc == None):
		return None

	text = tweet['text']
	sent = get_sentiment(text)
	sent = str(sent)

	return (loc, sent)

def make_requests(topic):
	"""Sends a request to the Twitter API to search for tweets on a given topic.
	Writes the data it pulls out into a file of the same name as the topic (with
	spaces replaced by underscores and .txt at the end.)

	Args:
		topic (str): topic string to get tweets about

	Returns:
		int: total number of tweets retrieved on this topic
	"""
	filename = re.sub(' ', '_', topic) + '.txt'
	data = request_data(topic)

	if(data == None or len(data) == 0):
		return

	total = 0

	for tweet in data:
		info = process_tweet(tweet.AsDict())
		if(info == None):
			continue

		info = clean_data(info)
		append_to_file('data\\' + filename, info)
		total += 1

	return total

def make_requests_no_file(topic):
	"""Sends a request to the Twitter API to search for tweets on a given topic.
	Does not write the data to a file, but instead returns a list of all the 
	strings.

	Args:
		topic (str): topic string to get tweets about

	Returns:
		list of str: data in the form "location\\tsentiment\\n"
	"""
	result = []
	data = request_data(topic)

	if(data == None or len(data) == 0):
		return

	for tweet in data:
		info = process_tweet(tweet.AsDict())
		if(info == None):
			continue

		result.append(info)

	return result

# # #  TWITTER API  # # #

def create_query(query):
	"""Create a query string from a topic to pass to a request to Twitter.

	Args:
		query (str): topic string to search with

	Return:
		str: topic turned into a query string
	"""
	query = urllib.parse.quote(query)
	query = 'l=en&count=100&q=' + query
	return query

def request_data(query):
	"""Passes a query to the Twitter API and returns the search tweets.

	Args:
		query (str): query containing search string and other parameters

	Returns:
		list of Status objects: tweets returned by the Twitter API wrapper
	"""
	query = create_query(query)
	results = api.GetSearch(raw_query=query)
	return results


# # #  LOCATIONS  # # #

def get_coord_location(coords):
	"""Gets a state abbreviation based on geo coordinates.

	Args:
		coords (list of str): coordinates of the tweet

	Returns:
		str: state abbreviation
		None: if state not found
	"""
	global geoloc
	coords = coords['coordinates']
	coords = geopy.point.Point(coords[1], coords[0])

	loc = geoloc.reverse(coords)
	if(loc is None):
		return ''

	loc = loc.raw
	if('address' not in loc):
		return ''

	loc = loc['address']
	if(loc['country_code'] != 'us'):
		return ''

	state = loc['state'].lower()
	if(state is None):
		return 'XX'

	state = us.states.lookup(state)
	if(state is None):
		return 'XX'

	state = state.abbr.upper()
	return state

def get_text_location(text):
	"""Checks if user input location data can tell you the state.
	Compares the text in the location blurb with a list containing
	the top 5 most populated cities in every state.

	Args:
		text (str): user input location text

	Returns:
		str: State abbreviation if found
		None: if not found
	"""
	text = text.lower()
	for s in locations.keys():
		if(s in text):
			return locations[s]

def get_location(tweet):
	"""Looks for a location in the tweet data, based on both coordinates 
	(if available) and user-input location text.

	Args:
		tweet (dict): tweet information

	Returns:
		str: State abbreviation if location is found
		None: if not found
	"""
	if('coordinates' in tweet):
		coords = tweet['coordinates']
	else:
		coords = ''
	result = ''

	if(coords != None and coords != ''):
		coords = get_coord_location(coords)

		if(coords != None):
			result = coords

	if(coords == None or coords == '' or coords == 'XX'):
		user = tweet['user']

		if(user == None or len(user) == 0):
			return result

		loc = ''
		if('location' in user):
			loc = user['location']
		if(loc == None or loc == ''):
			return result

		loc = get_text_location(loc)
		if(loc == ''):
			return result

		return loc

	return result


# # #  SENTIMENT  # # #

def get_sentiment(text):
	"""Uses TextBlob to get the sentiment of the given text.

	Args:
		text (str): text on which to perform sentiment analysis

	Returns:
		float: the sentiment value of the text
	"""
	blob = TextBlob(text)
	sent = blob.sentiment.polarity
	return sent


# # #  DATA COLLECTION  # # #

def auto_make_query(index):
	"""Automatically run a query on the sample query of the given index.
	Used for the data collection portion of the app.

	Args:
		index (int): index of a topic in the SAMPLE_QUERIES list

	Returns:
		tuple: (topic (str), number of tweets collected (int))
	"""
	query = SAMPLE_QUERIES[index]
	print('Running search on: ' + query)
	num_collected = make_requests(query)

	return (query, num_collected)

def auto_make_queries():
	"""Run the data collector on all of the topics in SAMPLE_QUERIES.

	Returns:
		int: total number of tweets retrieved and processed
	"""
	tweets_found = {}
	for i in range(0,len(SAMPLE_QUERIES)):
		topic, num = auto_make_query(i)
		tweets_found[topic] = num

	return tweets_found
