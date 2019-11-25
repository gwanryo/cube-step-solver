from flask import Flask, render_template
import importlib
recognizer = importlib.import_module('lib.cube-recognizer.cube-recognizer')


app = Flask(__name__)

@app.route('/')
def main():
    return "Hello world!"


if __name__ == '__main__':
    app.run()