from youloopit import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    dtadded = db.Column(db.DateTime)

