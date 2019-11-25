from flask import Blueprint, request, url_for
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube_recognizer')
light = importlib.import_module('lib.cube-recognizer.cube_light')

cube = Blueprint('cube', __name__)

@cube.route('/')
def cubes():
    cubeInfo = recognizer.recognize(5)
    return cubeInfo

@cube.route('/light', methods = ['POST'])
def light():
    try:
        data = request.get_json(silent=True)
        lightBright = int(data['light'])
        light.setBrightness(lightBright)
        return {"success": 1, "brightness": lightBright}
    except:
        return {"success": 0, "brightness": lightBright}
