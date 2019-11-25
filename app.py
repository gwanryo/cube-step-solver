from flask import Flask, render_template
from root import root
from cube import cube

app = Flask(__name__)
app.register_blueprint(root)
app.register_blueprint(cube, url_prefix='/cube')

if __name__ == '__main__':
    app.run()
