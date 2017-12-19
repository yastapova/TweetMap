from flask import render_template, flash, redirect
from app import app
from .forms import QueryForm
from .analyzer import request_data, auto_make_queries
from .mapper import get_state_sentiments

query_topic = ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = QueryForm()
	if form.validate_on_submit():
		flash('Search requested for keywords="%s"' % form.query.data)
		query_topic = form.query.data
		result = get_state_sentiments(query_topic)
		print(result)
		return render_template('form.html',
							title='TweetMap',
							form=form,
							samples=app.config['SAMPLE_QUERIES'],
							sent_data=result)
	return render_template('form.html',
							title='TweetMap',
							form=form,
							samples=app.config['SAMPLE_QUERIES'],
							sent_data={})

@app.route('/collect', methods=['GET'])
def collect():
	topics = auto_make_queries()
	return render_template('collect.html',
							topics=topics)
