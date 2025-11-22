from flask import Flask
from infrastructure.controllers.carta_controller import carta_controller
from infrastructure.controllers.productos_controller import productos_controller

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"

app.register_blueprint(carta_controller)
app.register_blueprint(productos_controller)

