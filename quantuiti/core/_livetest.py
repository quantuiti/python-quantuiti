import socketio
import asyncio
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient
import kucoin.client as kucoin

from datetime import datetime
import pandas as pd


from time import sleep
import os
from traceback import print_exc

from ._WindowsInhibitor import WindowsInhibitor

def livetest_algorithm(self):
    """
    this function live tests algorithms 
    """
    api_key = self.client['api_key']
    api_secret = self.client['api_secret']
    api_passphrase = self.client['api_passphrase']
    api_url = self.client['api_url']

    if os.name == 'nt':
        osSleep = WindowsInhibitor()
        osSleep.inhibit()

    if 'sandbox' in api_url:
        api_sandbox = True

    if self.client['type'] == 'crypto':
        self.sio = socketio.AsyncClient()

        @self.sio.event
        async def message(data):
            print(data)
        @self.sio.event
        async def connect():
            print('i am connected')
        @self.sio.event
        async def connect_error(data):
            print('The connection Failed')


        async  def commands():
            while True:
                user_input = input('enter command: ')
                print(self.data)

        async def main():
            async def deal_msg(msg):
                if msg['topic'] == '/market/candles:BTC-USDT_1min':
                    try:
                        candles = msg['data']['candles']
                        time = int(candles[0])
                        if hasattr(self, 'prevtime'):

                            
                            if time >= self.prevtime:
                                temp = {
                                    'Date':   datetime.fromtimestamp(time).strftime('%Y-%M-%d %H-%M-%S'),
                                    'High':   float(candles[3]),
                                    'Low':    float(candles[4]),
                                    'Open':   float(candles[1]),
                                    'Close':  float(candles[2]),
                                    'Volume': float(candles[6])
                                }
                                self.close = temp['Close']
                                self.data = self.data.append(temp, ignore_index=True)
                                self.index += 1
                                self.algo(self)
                                await self.sio.emit('message', temp)
                                
                        elif not hasattr(self, 'prevtime'):
                            temp = {
                                'Date':   [datetime.fromtimestamp(time).strftime('%Y-%M-%d %H-%M-%S')],
                                'High':   [float(candles[3])],
                                'Low':    [float(candles[4])],
                                'Open':   [float(candles[1])],
                                'Close':  [float(candles[2])],
                                'Volume': [float(candles[6])]
                            }
                        
                            self.index = 0
                            self.data = pd.DataFrame(temp)

                        self.prevtime = time
                    except Exception as error:
                        print(error)
                        print_exc()

            client = WsToken(key=api_key, secret=api_secret, passphrase=api_passphrase, is_sandbox=api_sandbox, url=api_url) # websockets stuff 
            self.ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)                              #
            await self.ws_client.subscribe('/market/candles:BTC-USDT_1min')                                                  #
            await self.sio.connect('http://127.0.0.1:5000')   
            print('connected to kucoin socket')
            await self.sio.sleep(1.0)                                                               #
            
            while True:
                await asyncio.sleep(5, loop=loop)

                    
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt: # if keyboard interrupt in websockets handle closeing of program
            for task in asyncio.Task.all_tasks():
                task.cancel()
                print('stopping loop')
            loop.stop()
            loop.close()
            """
                handle keyboard interupt here
                executing sell orders so positions from bot don't remain open
            """
            try:
                exit()
            except RuntimeError as error:
                print(error)
                

    if self.bot_type == 'stock':
        pass