import os
import shlex
import shutil
import subprocess

from flask import Blueprint, request
from pathlib import Path


PATH_ROOT = Path(__file__).parent.parent
PATH_REPOS = os.getenv('BBUILD_REPOS', PATH_ROOT / 'repos')


if not PATH_REPOS.is_dir():
    PATH_REPOS.mkdir()


api = Blueprint('api', __name__)


def call(command):
    command = shlex.split(command) if type(command) == str else command
    print(f"Calling: {' '.join(command)}")
    return subprocess.call(command)


@api.route('/repos', defaults={'name': None}, methods=['GET', 'POST'])
@api.route('/repos/<string:name>', methods=['PATCH', 'DELETE'])
def repos_route(name):

    def get():
        return f"name: {name}"

    def post():
        return f"name: {name}"

    def delete():
        return f"name: {name}"

    def patch():
        return f"name: {name}"

    return locals()[request.method.lower()]()
