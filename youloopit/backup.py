import os
import re
import urllib.parse
import urllib.request
from typing import Dict, List, Any

from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField
from wtforms.validators import InputRequired, DataRequired
from ordered_set import OrderedSet
import youtube_dl

app = Flask(__name__)
app.config.from_pyfile('youloopit.config')
db = SQLAlchemy(app)
Bootstrap(app)

from views import

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

@app.route("/youtubedl", methods=['GET'])
def youtubedl():
    vid = request.args.get('vid', None)
    type = request.args.get('type', 'avio')
    res = {}
    res['status'] = 'success'
    video_url = 'https://www.youtube.com/watch?v=' + vid
    res['savedpath'] = os.getcwd() + os.path.sep + "downloads/"
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        os.chdir(res['savedpath'])
        ydl.download([video_url])
    return (jsonify(res))


@app.route("/", methods=['GET', 'POST'])
@app.route("/<string:loopvidid>", methods=['GET', 'POST'])
def main(loopvidid=None):
    yplayers = {}
    results = None
    if loopvidid:
        yplayers['res'] = {"id": loopvidid, "videoId": loopvidid}
        return render_template("vidoptions.html", yplayers=yplayers)
    else:
        form = VideoSearchForm()
        if form.validate_on_submit():
            query_string = urllib.parse.urlencode({"search_query": form.searchThis.data})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            ylist = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            # Use an OrderedSet since youtube search will possibly give the best match first.
            videos = list(OrderedSet(ylist[
                                     :20]))  # Expectation is that the first 50 will contain duplicates resulting in at least 25 videos.
            results = zip([x + 1 for x in range(len(videos))], videos)
            yp = []
            for vid in range(len(videos)):
                yp.append({"id": str(vid + 1), "pid": "player{}".format(vid + 1), "vid": videos[vid]})
            yplayers['res'] = yp
            return render_template("vidoptions.html", yplayers=yplayers)
        return render_template("index.html", form=form)


app.run(host='0.0.0.0', port=8009, debug=True)
