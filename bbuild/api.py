import os
import shlex
import shutil
import subprocess

from flask import Blueprint, request, jsonify
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


def response(code, items=None, error=None):
    return jsonify({
        'items': items,
        'status-code': code,
        'error': error,
    }), code


@api.route('/repos', defaults={'name': None}, methods=['GET', 'POST'])
@api.route('/repos/<string:name>', methods=['PATCH', 'DELETE'])
def repos(name):

    def get():
        return response(200, items=repos_list())

    def post():
        payload = request.json

        if not payload or 'name' not in payload:
            return response(400, error="Missing required 'name' field.")

        try:
            return response(200, repos_create(payload['name']))
        except OSError as e:
            return response(409, error=str(e))

    def delete():
        try:
            repos_remove(name)
            return response(200)
        except OSError as e:
            return response(409, error=str(e))

    def patch():
        pass

    return locals()[request.method.lower()]()


def repos_list():
    return [p.name for p in PATH_REPOS.iterdir() if p.is_dir()]


def repos_create(name):
    name = Path(name).name
    to_init = PATH_REPOS / name
    if to_init.is_dir():
        raise OSError(f"Repository name already taken: {name}")
    call(f"git init --bare --shared {to_init}")
    call(f"git --git-dir={to_init} config receive.denyNonFastForwards false")


def repos_remove(name):
    name = Path(name).name
    path_to_remove = PATH_REPOS / name
    if not path_to_remove.is_dir():
        raise OSError(f"Repository does not exist: {name}")
    shutil.rmtree(path_to_remove)
