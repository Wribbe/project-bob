import os
import secrets
import requests

from flask import Flask, render_template, request, url_for, redirect, flash
from bbuild.api import api as api_blueprint
from pathlib import Path

PATH_ROOT = Path(__file__).parent.parent
PATH_DATA = os.getenv('BBUILD_DATA', PATH_ROOT / 'data')
PATH_SECRET =  PATH_DATA / 'secret.txt'

if not PATH_DATA.is_dir():
    PATH_DATA.mkdir()

if not PATH_SECRET.is_file():
    PATH_SECRET.write_text(secrets.token_hex())


app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', 'localhost:5000')
app.register_blueprint(api_blueprint, subdomain="api")
app.secret_key = PATH_SECRET.read_text()


@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        payload = request.form.to_dict()
        resp = requests.post(
            url_for('api.repos'),
            json=payload,
        )
        if resp.status_code == 409:
            flash(
                "Creation failed, repository with name "
                f"{payload['name']} already exists."
            )
        else:
            flash(f"Successfully created repository: {payload['name']}.")
        return redirect(url_for('index'))

    return render_template('index.html')
