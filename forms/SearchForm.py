from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    site = StringField("Site", validators=[DataRequired()])
    subdomain = StringField("Subdomain", validators=[DataRequired()])
    search_terms = StringField("Search terms (separate with a comma)", validators=[DataRequired()])
    limit = StringField("Limit: results per search term", validators=[DataRequired()])
    submit = SubmitField("Submit")