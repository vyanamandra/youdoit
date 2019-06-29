import re
import urllib.parse
import urllib.request

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from ordered_set import OrderedSet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'promiseIdiChaalaPeddaSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youdoit.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    dtadded = db.Column(db.DateTime)


class VideoSearchForm(FlaskForm):
    searchThis = StringField('Search in youtube for this video: ',
                             validators=[InputRequired(message="Enter a text (eg., 'oke oka jeevitham')")])
    submit = SubmitField("Search")


vidIdsInMem = ['uuZE_IRwLNI', '8ELbX5CMomE']


def getSavedVids():
    """
    Will need to use a simple sqlite3 db to retrieve the list
    """
    savedInDB = []
    return vidIdsInMem + savedInDB


@app.route("/", methods=['GET', 'POST'])
@app.route("/<string:loopvidid>", methods=['GET', 'POST'])
def main(loopvidid=None):
    if loopvidid:
        return render_template("vidoptions.html", results=[loopvidid])
    else:
        form = VideoSearchForm()
        if form.validate_on_submit():
            query_string = urllib.parse.urlencode({"search_query": form.searchThis.data})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            ylist = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            # Use an OrderedSet since youtube search will possibly give the best match first.
            videos = list(OrderedSet(ylist[:50])) # Expectation is that the first 50 will contain duplicates resulting in at least 25 videos.
            results = zip([x for x in range(1, len(videos)+1)], videos)
            return render_template("vidoptions.html", results=results)
        return render_template("index.html", form=form)


app.run(host='0.0.0.0', port=8009, debug=True)
