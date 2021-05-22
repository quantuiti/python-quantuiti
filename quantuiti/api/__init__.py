from flask import Flask, render_template, request
import webbrowser
from flask_socketio import SocketIO, join_room, leave_room, send
import logging

from termcolor import colored

from datetime import datetime

def run_api():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    clients = []
    servers = []

    @socketio.on('join')
    def on_join(data):
        if data.get('room') == 'client':
            client = data['client']
            if request.sid not in clients:
                clients.append(request.sid)
            join_room('client')
            join_room(request.sid)
            return 'ack', 200
        if 'server' in data.get('room'):
            servers.append(data.get('room'))
            join_room(data.get('room'))
            return 'ack', 200

    @socketio.on('buy')
    def buy(data):
        """
            recieves data when algorithm sends a buy signal.
        """
        if not data.get('buy'):
            
            print(
                colored((f'[*] { datetime.now().strftime("%H:%M:%S")} -- malformed data sent to ', buy), 'red')
            )

        elif data['buy'].get('shares') is None or data['buy'].get('balance') is None or data['buy'].get('price') is None:
            print(
                colored((f'[*] { datetime.now().strftime("%H:%M:%S")} -- malformed data sent to ', buy), 'red')
            )
        else:
            socketio.emit('client_data', 
            {'buy': {
                'shares': data['buy'].get('shares'),
                'balance':data['buy'].get('balance'),
                'price':  data['buy'].get('price')
            }}, 
            room=data.get('client'))
    @socketio.on('sell')
    def sell(data):
        """
            recieves data when algorithm sends a sell signal.
        """
        if not data.get('sell'):
            print(
                colored((f'[*] { datetime.now().strftime("%H:%M:%S")} -- malformed data sent to ', sell), 'red')
            )
        elif data['sell'].get('shares') is None or data['sell'].get('balance') is None or data['sell'].get('price') is None:
            print(
                colored((f'[*] { datetime.now().strftime("%H:%M:%S")} -- malformed data sent to ', sell), 'red')
            )
        else:
            socketio.emit('client_data', 
            {'sell': {
                'shares': data['sell'].get('shares'),
                'balance':data['sell'].get('balance'),
                'price':  data['sell'].get('price')
            }}, 
            room=data.get('client'))                


            

    @socketio.on('message')
    def handle_message(data):
        if data.get('Close'):
            socketio.emit('message', {'Close': data["Close"]}, room='client')
            # print(f'BTC-USDT Price: {data["Close"]}')
        else:
            print(data)

    @socketio.on('command')
    def route_command(data):
        if request.sid in clients:
            if data.get('command'):
                socketio.emit('command', {'command': data['command'], 'client': request.sid}, room='server')
                
            else:
                return 'no command sent', 400

        if data.get('response') and data.get('client'):
            response = data.get('response')
            try:
                socketio.emit('return_command', {'response': response}, room=data.get('client'))                
            except Exception as error:
                print(error)   

    @app.route('/')
    def index():
        return render_template('index.html')

    print('API STARTED !!')
    # webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app)

if __name__ == "__main__":
    run_api()
    