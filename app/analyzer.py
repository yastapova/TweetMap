import re, urllib
import twitter
import geopy, us
from textblob import TextBlob

import keys
from locations import locations

api = twitter.Api(consumer_key=keys.CONSUMER_KEY,
                  consumer_secret=keys.CONSUMER_SECRET,
                  access_token_key=keys.ACCESS_TOKEN_KEY,
                  access_token_secret=keys.ACCESS_TOKEN_SECRET)

geoloc = geopy.geocoders.Nominatim()

# # #  UTILS  # # #

def append_to_file(filename, data):
	with open(filename, "a") as f:
		f.write('\t'.join(data))

def process_tweet(tweet):
	loc = get_location(tweet)
	if(loc == ''):
		return None

	text = tweet['text']
	sent = get_sentiment(text)

	return (text, loc, sent)

def make_requests(topic):
	filename = re.sub(' ', '_', topic)
	data = request_data(topic)

	if(data == None or len(data) == 0):
		return

	for tweet in data:
		info = process_tweet(tweet)
		append_to_file(filename, info)


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
	text = text.lower()
	for s in locations.keys():
		if(s in text):
			return locations[s]

def get_location(tweet):
	coords = tweet['coordinates']
	result = ''

	if(coords != None and coords != ''):
		coords = get_coord_location(coords)

		if(coords != None):
			result = coords

	if(coords == None or coords == '' or coords == 'XX'):
		user = tweet['user']

		if(user == None or len(user) == 0):
			return result

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
	return sen


# # #  DATA COLLECTION  # # #

def auto_make_query():
