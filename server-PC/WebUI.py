from flask import Flask, render_template, g, request
import SimpleRF
from logging import getLogger
from datetime import datetime
import os

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
_log = getLogger('SimpleRF')

'''
@app.before_request
def before_request():
    g.db = Database.Database()
'''

@app.template_filter('timestamp2date')
def timestamp2date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    print SimpleRF.db.get()
    return render_template('index.html', data=SimpleRF.db.get().values())

@app.route('/act/<node>/<sensor>', methods=['POST'])
def act(node, sensor):
    val = request.form['val']
    _log.info("web action: {0}-{1} := {2}".format(node, sensor, val))
    SimpleRF.action(node, sensor, val)
    return "0|OK"

@app.route('/upload', methods=['POST'])
def upload():
    code = request.form['code']
    filename = os.path.dirname(os.path.realpath(__file__)) + "/userLogic.py"
    print filename
    print code
    with open(filename, 'w') as fp:
        fp.write(code)
    return "0|OK"