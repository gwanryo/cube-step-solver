from flask import Blueprint, request, url_for
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube_recognizer')
light = importlib.import_module('lib.cube-recognizer.cube_light.cube_light')

cube = Blueprint('cube', __name__)

@cube.route('/', methods = ['POST'])
def cubes():
    tryCount = 5

    try:
        data = request.get_json(silent=True)
        tryCount = int(data['count'])
        lightBright = int(data['light'])
    except:
        pass

    cubeInfo = recognizer.recognize(tryCount, lightBright)
    return cubeInfo

@cube.route('/light', methods = ['POST'])
def lights():
    try:
        data = request.get_json(silent=True)
        lightBright = int(data['light'])
    except:
        return {"success": 0, "brightness": lightBright}

    if light.setBrightness(lightBright):
        return {"success": 1, "brightness": lightBright}
    else:
        return {"success": 0, "brightness": lightBright}
