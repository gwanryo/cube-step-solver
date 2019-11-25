from flask import Blueprint, request, url_for
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube-recognizer')

cube = Blueprint('cube', __name__)

@cube.route('/')
def cubes():
    cubeInfo = recognizer.recognize()
    return cubeInfo

@cube.route('/light', methods = ['POST'])
def light():
    data = request.get_json(silent=True)
    recognizer.recognize(data['light'])
