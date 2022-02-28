import os
from bbuild.app import app

os.environ['FLASK_ENV'] = 'development'

def main():
    app.run('0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
