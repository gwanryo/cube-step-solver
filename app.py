from flask import Flask, render_template
from .lib.cube-recognizer import cube-recognizer
app = Flask(__name__)

@app.route('/')
def main():
    return 


if __name__ == '__main__':
    app.run()