from flask import Blueprint, request, url_for, abort
from requests import get

video = Blueprint('video', __name__)

VIDEO_URL = [
    'http://localhost:8080/?action=stream',
    'http://localhost:8081/?action=stream'
]

@video.route('/<id>')
def videos(order):
    if order < len(VIDEO_URL):
        return get(f'{VIDEO_URL[order]}').content
    else:
        abort(404)
