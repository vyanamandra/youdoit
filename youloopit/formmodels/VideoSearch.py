from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class VideoSearchForm(FlaskForm):
    searchThis = StringField('Search in youtube for this video: ',
                             validators=[InputRequired(message="Enter a text (eg., 'oke oka jeevitham')")])
    submit = SubmitField("Search")