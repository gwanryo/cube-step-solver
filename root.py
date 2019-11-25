from flask import Blueprint, render_template
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube-recognizer')

root = Blueprint('root', __name__)

@root.route("/")
def roots():
    try:
        cubeInfo = recognizer.recognize()
    except:
        cubeInfo = {}
    
    return render_template(
        "cube-simulator/index.html",
        cube = cubeInfo
    )
