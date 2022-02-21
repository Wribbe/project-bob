import os
from bbuild.app import app

def run_dev():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)


def run():
    app.run('0.0.0.0')
