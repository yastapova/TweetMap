from flask import render_template, flash, redirect
from app import app
from .forms import QueryForm
from .analyzer import request_data

query_topic = ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = QueryForm()
	if form.validate_on_submit():
		flash('Search requested for keywords="%s"' % form.query.data)
		query_topic = form.query.data
		result = request_data(query_topic)
		print(len(result))
		return redirect('/index')
	return render_template('form.html',
							title='TweetMap',
							form=form,
							samples=app.config['SAMPLE_QUERIES'])
