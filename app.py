from flask import Flask
from root import root
from cube import cube

app = Flask(__name__, static_folder='templates/cube-simulator/static')
app.register_blueprint(root)
app.register_blueprint(cube, url_prefix='/cube')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
