import os
from bbuild.app import app

def run_dev():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)


def run():
    import socket
    os.environ['SERVER_NAME'] = socket.gethostname()
    app.run('0.0.0.0')
