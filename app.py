from flask import Flask
from flask_slowloger import SlowLogger
from logging.config import dictConfig
import  time

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
app.debug = True
app.config["slowlogger_enable"] = True
slowlogger = SlowLogger(app)

@app.route('/index', methods = ["get"])
def index():
    return "nihao"

@app.route("/slow", methods=["get"])
@slowlogger.log_entry
def slow():
    time.sleep(2)
    return "slow"

if __name__ == '__main__':
    app.run("0.0.0.0", 8081)