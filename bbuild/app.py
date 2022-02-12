import os

from flask import Flask, render_template
from bbuild.api import api as api_blueprint

app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', 'localhost:5000')
app.register_blueprint(api_blueprint, subdomain="api")


@app.route('/')
def index():
    return render_template('index.html')
