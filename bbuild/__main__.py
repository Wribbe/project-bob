import os
from bbuild.app import app

def run():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)
