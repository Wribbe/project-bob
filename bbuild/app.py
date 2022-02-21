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


app = Flask(__name__)
app.secret_key = PATH_SECRET.read_text()
app.register_blueprint(api_blueprint, url_prefix="/api")


@app.route('/', methods=["GET", "POST"])
def index():

    URL_API = url_for('api.repos', _external=True)

    if request.method == "POST":
        payload = request.form.to_dict()

        if payload.get('method', "").upper() == "DELETE":
            to_be_deleted = payload['target']
            resp = requests.delete(f"{URL_API}/{to_be_deleted}")
            if resp.status_code == 409:
                flash(
                    "Deletion failed, repository with name "
                    f"{payload['target']} does not exist."
                )
            else:
                flash(f"Successfully deleted repository: {payload['target']}.")
        else:
            data = {
                'name': payload['target'],
            }
            resp = requests.post(URL_API, json=data)
            if resp.status_code == 409:
                flash(
                    "Creation failed, repository with name "
                    f"{payload['target']} already exists."
                )
            elif not resp.ok:
                flash(
                    f"Couldn't create repository, unknown error: {resp.json()}"
                )
            else:
                flash(f"Successfully created repository: {payload['target']}.")

        return redirect(url_for('index'))

    repos = sorted(requests.get(URL_API).json()['items'])
    return render_template('index.html', repositories=repos)


@app.route('/confirm', methods=["POST", "GET"])
def confirm():
    if request.method == "POST":
        payload = request.form.to_dict()
        return redirect(url_for('confirm', **payload))

    payload = request.args.to_dict()
    return render_template('confirm.html', payload=payload)
