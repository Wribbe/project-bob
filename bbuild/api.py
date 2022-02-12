import subprocess

from flask import Blueprint, request
from pathlib import Path


api = Blueprint('api', __name__)

ROUTES = """
    /repos/<string:name> | GET, DELETE, PATCH
    /repos               | GET, POST
"""


def call(command):
    command = command.split() if type(command) == str else command
    print(f"Calling: {' '.join(command)}")
    return subprocess.call(command)


def repos(name):

    def get():
        return f"name: {name}"

    def post():
        return f"name: {name}"

    def delete():
        return f"name: {name}"

    def patch():
        return f"name: {name}"

    return locals()[request.method.lower()]()


_routes = {}
for line in [l for l in ROUTES.splitlines() if l.strip()]:
    route, methods = [t.strip() for t in line.split('|')]
    methods = [m.strip() for m in methods.split(',')]
    root, *rest = [t.strip() for t in route[1:].split('/')]
    _routes.setdefault(root, {})
    params = [r for r in rest if r.startswith('<')]
    _routes[root][','.join(params)] = methods


for route, route_data in _routes.items():
    for attribute, methods in route_data.items():
        kwargs = {'methods': methods, 'view_func': locals()[route]}
        if not attribute:
            kwargs['defaults'] = {
                a[1:-1].split(':')[-1]: None for a in route_data if a.strip()
            }
        rule = f"/{route}/{attribute}" if attribute else f"/{route}"
        api.add_url_rule(rule, **kwargs)
