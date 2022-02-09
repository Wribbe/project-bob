from flask import Flask, render_template
from bbuild.api import api as api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="/api")


@app.route('/')
def index():
    return render_template('index.html')
