# TweetMap

TweetMap is a simple web app that analyzes the sentiment of tweets on a given topic. TweetMap allows the user to enter a search query, which it then passes to Twitter and returns a collection of tweets. The application then performs sentiment analysis on those tweets, and aggregates the data by US state. Finally, a map is displayed, showing the average sentiment in each US state on that topic.

TweetMap also allows the user to collect and save sentiment data on certain topics specified in the ```config.py``` file.

This project is built mostly in [Python 3](https://www.python.org/), with some JavaScript using the [D3.js](https://d3js.org/) library for the map visualization. It also uses the [Twitter API](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets) to retrieve the data that it analyzes.

## Requirements

TweetMap requires the user to have [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip) installed. Python 3.4+ comes with pip, so you will not need to install it separately.

Other requirements that are addressed as part of **Set Up**:
- [flask](http://flask.pocoo.org/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [python-twitter](http://python-twitter.readthedocs.io/en/latest/index.html)
- [geopy](http://geopy.readthedocs.io/en/latest/)
- [us](https://pypi.python.org/pypi/us)
- [textblob](http://textblob.readthedocs.io/en/dev/index.html)

## Set Up

1. Ensure you have the python libraries ```flask``` and ```virtualenv```. If not, install them using ```pip install flask``` and ```pip install virtualenv```.
2. Clone this repository.
3. In the root directory of the cloned repository, run ```python -m venv flask```. This will create a virtual python environment in which to run the app. If it executes successfully, you should see a folder named ```flask``` in the root directory now.
4. Run the following commands. These will install all of the required libraries in the virtual environment we have just set up.
```
flask\Scripts\pip install flask
flask\Scripts\pip install flask-wtf
flask\Scripts\pip install python-twitter
flask\Scripts\pip install geopy
flask\Scripts\pip install textblob
flask\Scripts\pip install us
```
5. Enter your Twitter API keys in appropriate variables in the ```keys.py``` file. Make sure the keys are inside the quotes. A tutorial on how to get the API keys can be found [here](http://python-twitter.readthedocs.io/en/latest/getting_started.html).
6. Run ```flask\Scripts\python run.py``` from the root directory of the repository.
7. Go to ```localhost:5000``` in a browser, and enjoy!

## Functionality

TweetMap allows the user to do two things: display the sentiment map and collect data.

### Show Sentiment Map

To search for a topic and display sentiment:
1. Stay on the "Home" screen (the one the app starts on) or navigate to it using the menu at the top of the page.
2. Enter a topic in the search bar and hit the Search button (or Enter). Short queries work best.
3. The map will then be displayed.

**Notes**
- If you can't think of anything to search for, try clicking on ```Sample Queries``` to auto-populate the search bar with a topic. These topics have some amount of sentiment data pre-processed and saved, and will result in a more interesting map.
- You can see a detailed sentiment value for each state in the tooltip displayed on mouseover.
- Sentiment ranges from -1 (Negative) to 0 (Neutral) to +1 (Positive).

### Collect Data

To collect, pre-process, and save data on a small selection of topics:
1. Click on the ```Collect Data``` link in the top menu bar.
2. The data will be automatically collected, and it will display how many tweets were found for each topic.

**Notes**
- The topics for which to collect data can be changed in the ```config.py``` file.
- These are also the same topics that are populated using the "Sample Queries" button on the Home page.
- The collected data will be saved to a file in the ```data``` folder, with the name ```{topic}.txt```, where "topic" is the topic string entered in ```SAMPLE_QUERIES``` in the ```config.py``` file, with spaces replaced with underscores. (Ex: "potato chips" --> "potato_chips.txt").

## Implementation

This section describes exactly how TweetMap works, and what steps are taken to retrieve, process, and visualize data.

### Web App

At its core, TweetMap is a web app that runs on Python Flask. Flask is used to create the web app structure, handle routing, and handle creating/loading the requested views. The app only has two pages and two corresponding views: index and collect. The "index" view holds the search form and the map visualization, while the "collect" view displays information about the automated data collection.

### Search

When the search query is entered into the box, the app cleans up the input, puts it into a nice query format, and sends the search request off to Twitter using a python wrapper for the Twitter API. All of this can be found in the ```analyzer.py``` file. Note that the keys are loaded into the API object ahead of time, and they are obtained from the ```keys.py``` file, which is included in the repository, but starts off with empty variables for the keys.

### Analysis

#### Location

Once tweets are returned from the search, the real work begins. First, not all tweets have location data. Since location data is vital to TweetMap, all of the tweets without a location are filtered out. There are two ways we can get location data: coordinates or a user-defined location. If coordinates are provided, great! We will use those. The coordinates are passed into a geocoder object from geopy, which figures out where in the world this tweet was. If the location is found to be within the United States, we save the state abbreviation and move on.

However, if there are no coordinates, we have to look at the user input location. Since users can write whatever they like in this field, we have to make sure this is a real location. To this end, we check if the location is one of the top 5 most populous cities in the state. If it is, we save the state abbreviation. Otherwise, we throw the tweet away.

#### Sentiment

After we find the location, we move on to the sentiment of the tweet. For this, a TextBlob object is created and the text of the tweet is passed into it. TextBlob uses a pre-trained sentiment analyzer to provide a sentiment score for the given text. This allows for a relatively speedy off-the-shelf way to perform sentiment analysis.

Once we have the sentiment score, we can do one of two things with it, depending on what the app is supposed to be doing. If we are currently running the data collector, the location (state abbreviation) and sentiment score will be written to a file, and we stop there. If instead we are trying to display the map, the data is simply returned to from the function, and we move on aggregation.

#### Aggregation

Now that we have a bunch of data composed of the state abbreviation and sentiment score of each tweet, we need to aggregate this data so that we can display it on the map. We first check if we have a file containing saved data on the given topic. If so, that data is also incorporated in the aggregation along with the fresh data. To aggregate, we simply take an average of all the sentiment scores for a given state. This data is saved to a csv file that will be read by the JavaScript code that visualizes it into a map.

### Visualization

Now we have data, and we have to display it. I chose to use D3 for the visualization portion of this project because I have some prior experience with it and I found it to be pretty flexible. The states on the map are created from a json file containing data that defines how they should be drawn. Then, the aggregated data is assigned to each state object. Each state is then colored based on a scale of -1 (red) to 0 (white) to +1 (blue). (Note: Red and Green might be more intuitive for showing negative/positive, but that presents difficulties to many people with colorblindness. Red and blue is fine anyway.) Finally, tooltips are assigned to each state, and the legend is created. Thus, the map is complete.

## Future Improvements

There are several things I have in mind as potential improvements to the app:
- More detailed location filtering (No doubt many tweets are currently lost because they are not in one of 5 cities per state. This should be generalized further.)
- More accurate sentiment analysis (An off-the-shelf classifier is alright, but it would be better to have one trained specifically on tweets. However, this would require compiling a dataset to train on.
- Run several searches on Twitter for a given topic to get more fresh data
- Differentiate emotions, rather than just positive/negative
