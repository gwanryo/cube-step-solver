from flask import Blueprint, url_for, abort, Response, stream_with_context
import requests
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube_recognizer')

video = Blueprint('video', __name__)

VIDEO_URL = None
VIDEO_CHUNK_SIZE = 10 * 1024 # 10KB

@video.route('/<int:id>')
def videos(id):
    global VIDEO_URL
    if not VIDEO_URL:
        recognizer.readConfig(recognizer.CONFIG_FILE)
        VIDEO_URL = recognizer.CAMERA_URL

    if id < len(VIDEO_URL):
        r = requests.get(VIDEO_URL[id], stream=True)
        return Response(r.iter_content(chunk_size=VIDEO_CHUNK_SIZE),
                        content_type=r.headers['Content-Type'])
    else:
        abort(404)
