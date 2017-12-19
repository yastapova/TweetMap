import re, urllib, random
import twitter
import geopy, us
from textblob import TextBlob

import keys
from locations import locations
from config import SAMPLE_QUERIES

api = twitter.Api(consumer_key=keys.CONSUMER_KEY,
                  consumer_secret=keys.CONSUMER_SECRET,
                  access_token_key=keys.ACCESS_TOKEN_KEY,
                  access_token_secret=keys.ACCESS_TOKEN_SECRET)

geoloc = geopy.geocoders.Nominatim()

# # #  UTILS  # # #

def append_to_file(filename, data):
	with open(filename, encoding="utf-8", mode="a") as f:
		f.write(data)

def clean_data(data):
	text = data[0]
	loc = data[1]
	sent = data[2]

	text = '%r' % text
	data = (text, loc, sent)
	data = '\t'.join(data)
	data = data + '\n'
	return data

def process_tweet(tweet):
	loc = get_location(tweet)
	if(loc == '' or loc == None):
		return None

	text = tweet['text']
	sent = get_sentiment(text)
	sent = str(sent)

	return (text, loc, sent)

def make_requests(topic):
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


# # #  TWITTER API  # # #

def create_query(query):
	query = urllib.parse.quote(query)
	query = 'l=en&count=100&q=' + query
	return query

def request_data(query):
	query = create_query(query)
	results = api.GetSearch(raw_query=query)
	return results


# # #  LOCATIONS  # # #

def get_coord_location(coords):
	global geoloc
	coords = coords['coordinates']
	coords = geopy.point.Point(coords[1], coords[0])

	loc = geoloc.reverse(coords)
	if(loc is None):
		print("none")
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
	text = text.lower()
	for s in locations.keys():
		if(s in text):
			return locations[s]

def get_location(tweet):
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
	blob = TextBlob(text)
	sent = blob.sentiment.polarity
	return sent


# # #  DATA COLLECTION  # # #

def auto_make_query(index):
	query = SAMPLE_QUERIES[index]
	print('Running search on: ' + query)
	num_collected = make_requests(query)

	return (query, num_collected)

def auto_make_queries():
	tweets_found = {}
	for i in range(0,len(SAMPLE_QUERIES)):
		topic, num = auto_make_query(i)
		tweets_found[topic] = num

	return tweets_found
