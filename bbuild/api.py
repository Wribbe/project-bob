import subprocess

from flask import Blueprint, request
from pathlib import Path


api = Blueprint('api', __name__, template_folder="templates")


def call(command):
    command = command.split() if type(command) == str else command
    print(f"Calling: {' '.join(command)}")
    return subprocess.call(command)


@api.route('/repo', methods=['GET','POST','DELETE'])
def repo():

    if request.method == "POST":
        return "POST RESPONSE"

    if request.method == "DELETE":
        return "DELETE RESPONSE"

    return "GET RESPONSE"
