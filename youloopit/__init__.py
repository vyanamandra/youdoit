from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('youloopit.config')
db = SQLAlchemy(app)
Bootstrap(app)

from youloopit.views.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8092, debug=True)
