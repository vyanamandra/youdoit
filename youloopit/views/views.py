import os
from flask import render_template, request, jsonify
from youloopit.formmodels.VideoSearch import VideoSearchForm
from youloopit.tools.youtube import YouTube
from youloopit import app


@app.route("/youtubedl", methods=['GET'])
def youtubedl():
    vid = request.args.get('vid', None)
    download_type = request.args.get('type', 'avio')
    # TODO: Need to perform the right type of download as requested. Currently,
    #  only 'Complete Audio/Video of the best resolution is being downlaoded'
    _ = download_type  # Just a way to ignore this unused warning.
    return YouTube.download(videoId=vid)


@app.route("/", methods=['GET', 'POST'])
@app.route("/loop/<string:loopvidid>", methods=['GET', 'POST'])
def main(loopvidid=None):
    yplayers = {}
    if loopvidid:
        yplayers['res'] = [{"id": str(1), "pid": "player1", "vid": loopvidid}]
        return render_template("vidoptions.html", yplayers=yplayers)
    else:
        form = VideoSearchForm()
        if form.validate_on_submit():
            yt = YouTube(form.searchThis.data)
            videos = yt.search(20)
            yp = []
            for vid in range(len(videos)):
                yp.append({"id": str(vid + 1), "pid": "player{}".format(vid + 1), "vid": videos[vid]})
            yplayers['res'] = yp
            return render_template("vidoptions.html", yplayers=yplayers)
        return render_template("index.html", form=form)
