from flask import Flask
from controllers.carta_controller import carta_controller

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"

app.register_blueprint(carta_controller)

