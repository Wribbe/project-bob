import os
from bbuild.app import app

os.environ['FLASK_ENV'] = 'development'
app.run('0.0.0.0', debug=True)
