from flask import Blueprint, render_template
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube_recognizer')

root = Blueprint('root', __name__)

@root.route("/")
def roots():
    return render_template(
        "cube-simulator/index.html"
    )
