from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchArtistForm(FlaskForm):
    artist = StringField('Full Artist Name')
    submit = SubmitField('Search')
