from pathlib import Path

PATH_BBUILD = Path("c:/bbuild")

import os
os.environ['BBUILD_DATA'] = PATH_BBUILD
os.environ['BBUILD_REPOS'] = PATH_BBUILD / 'repos'

from bbuild.app import app
app.run('0.0.0.0')
