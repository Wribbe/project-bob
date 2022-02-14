import os
import requests

from flask import Flask, render_template, request, url_for, redirect
from bbuild.api import api as api_blueprint

app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'localhost:5000')
app.register_blueprint(api_blueprint, subdomain="api")


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        payload = request.form.to_dict()
        resp = requests.post(
            url_for('api.repos_route'),
            json=payload,
        )
        return redirect(url_for('index'))

    return render_template('index.html')
