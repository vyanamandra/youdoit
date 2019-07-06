import sys
import os
cur_wd = os.getcwd()
sys.path.insert(0, cur_wd)
activate_this = (os.path.sep).join([cur_wd, 'venv', 'bin', 'activate_this.py'])
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from youloopit import app as application

