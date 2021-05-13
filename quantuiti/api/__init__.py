from flask import Flask
import webbrowser
from flask_socketio import SocketIO
import logging

def run_api():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @socketio.on('message')
    def handle_message(data):
        print('received message: ', data['Close'])

    @app.route('/')
    def index():
        return 'hello', 200

    webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app)
    