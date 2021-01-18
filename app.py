from flask import Flask
from flask_slowloger import SlowLogger
import  time

app = Flask(__name__)
slowlogger = SlowLogger(app)

@app.route('/index', methods = ["get"])
def index():
    time.sleep(1)
    return "nihao"


if __name__ == '__main__':
    app.run("0.0.0.0", 8081)