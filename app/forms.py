from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
	"""Represents the form used on the home page to search for tweets."""
	query = StringField('query', validators=[DataRequired()])