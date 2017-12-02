import re
import twitter
import urllib
import keys

api = twitter.Api(consumer_key=keys.CONSUMER_KEY,
                  consumer_secret=keys.CONSUMER_SECRET,
                  access_token_key=keys.ACCESS_TOKEN_KEY,
                  access_token_secret=keys.ACCESS_TOKEN_SECRET)

def filter_data(query):
	query = urllib.parse.quote(query)
	query = 'l=en&count=100&q=' + query
	print(query)
	return query

def request_data(query):
	query = filter_data(query)
	print(query)
	results = api.GetSearch(raw_query=query)
	print("*****************************")
	print(results[0])
	return results