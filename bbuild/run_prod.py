from pathlib import Path

PATH_BBUILD = Path("c:/bbuild")

import os
os.environ['BBUILD_DATA'] = str(PATH_BBUILD)
os.environ['BBUILD_REPOS'] = str(PATH_BBUILD / 'repos')

def main():
    from bbuild.app import app
    app.run('0.0.0.0')

if __name__ == "__main__":
    main()
