# TweetMap

TweetMap is a simple web app that analyzes the sentiment of tweets on a given topic. TweetMap allows the user to enter a search query, which it then passes to Twitter and returns a collection of tweets. The application then performs sentiment analysis on those tweets, and aggregates the data by US state. Finally, a map is displayed, showing the average sentiment in each US state on that topic.

TweetMap also allows the user to collect and save sentiment data on certain topics specified in the ```config.py``` file.

## Requirements

TweetMap requires the user to have Python 3 and pip installed.

## Set Up

1. Ensure you have the python libraries ```flask``` and ```virtualenv```. If not, install them using ```pip install flask``` and ```pip install virtualenv```.
2. Clone this repository.
3. In the root directory of the cloned repository, run ```python -m venv flask```. If it executes successfully, you should see a folder named ```flask``` in the root directory now.
4. Run the following commands:
```
flask\Scripts\pip install flask
flask\Scripts\pip install flask-wtf
flask\Scripts\pip install python-twitter
flask\Scripts\pip install geopy
flask\Scripts\pip install textblob
flask\Scripts\pip install us
```
5. Enter your Twitter API keys in appropriate variables in the ```keys.py``` file. Make sure the keys are inside the quotes.
6. Run ```flask\Scripts\python run.py``` from the root directory of the repository.
7. Go to ```localhost:5000``` in a browser, and enjoy!
