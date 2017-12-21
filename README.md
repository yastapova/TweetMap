# TweetMap

TweetMap is a simple web app that analyzes the sentiment of tweets on a given topic. TweetMap allows the user to enter a search query, which it then passes to Twitter and returns a collection of tweets. The application then performs sentiment analysis on those tweets, and aggregates the data by US state. Finally, a map is displayed, showing the average sentiment in each US state on that topic.

TweetMap also allows the user to collect and save sentiment data on certain topics specified in the ```config.py``` file.

## Requirements

TweetMap requires the user to have [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip) installed. Python 3.4+ comes with pip, so you will not need to install it separately.

Other requirements that are addressed as part of **Set Up**:
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
2. Enter a topic in the search bar and hit enter. Short queries work best.
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
