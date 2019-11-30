from flask import Blueprint, url_for, abort, Response, stream_with_context
import requests

video = Blueprint('video', __name__)

VIDEO_URL = [
    'http://localhost:8080/?action=stream',
    'http://localhost:8081/?action=stream'
]

@video.route('/<int:id>')
def videos(id):
    if id < len(VIDEO_URL):
        r = requests.get(VIDEO_URL[id], stream=True)
        return Response(r.iter_content(chunk_size=100*1024),
                        content_type=r.headers['Content-Type'])
    else:
        abort(404)
