from flask import Flask, render_template
import webbrowser
from flask_socketio import SocketIO, join_room, leave_room, send
import logging

def run_api():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @socketio.on('join')
    def on_join(data):
        client = data['client']
        if data.get('room') == 'client':
            join_room('client')
            send('ack', to='client')
            

    @socketio.on('message')
    def handle_message(data):
        if data.get('Close'):
            socketio.emit('message', {'Close': data["Close"]}, room='client')
            # print(f'BTC-USDT Price: {data["Close"]}')
        else:
            print(data)

    @app.route('/')
    def index():
        return render_template('index.html')

    print('API STARTED !!')
    # webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app)

if __name__ == "__main__":
    run_api()
    