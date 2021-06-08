import socketio
import asyncio
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient
import kucoin.client as kucoin

from datetime import datetime
import pandas as pd
import csv


from time import sleep
from os import name as osName, path
from sys import getsizeof as memSize
from traceback import print_exc

from ._WindowsInhibitor import WindowsInhibitor

from io import StringIO
from contextlib import redirect_stdout

def livetest_algorithm(self):
    """
    this function live tests algorithms 
    """
    api_key = self.client['api_key']
    api_secret = self.client['api_secret']
    api_passphrase = self.client['api_passphrase']
    api_url = self.client['api_url']

    if osName == 'nt':
        osSleep = WindowsInhibitor()
        osSleep.inhibit()

    if 'sandbox' in api_url:
        api_sandbox = True
    else:
        api_sandbox = False

    if self.client['type'] == 'crypto':
        self.sio = socketio.AsyncClient()

        async def append_to_csv(df, file):
            if path.exists(file):
                with open(file, 'r') as f:
                    header = next(csv.reader(f))
                columns = df.columns
                for column in set(header) - set(columns):
                    df[column] = ''
                df = df[header]
                df.to_csv(file, index = False, header = False, mode = 'a')
            else:
                df.to_csv(file, index=False, header=True)
                

        @self.sio.event
        async def message(data):
            print(data)

        @self.sio.event
        async def command(data,self=self):
            if data.get('command'):
                command = data.get('command')
            
                _func_template = 'async def __ex(self): \n' + '\t ' + command
                exec(_func_template)
                f = StringIO()
                with redirect_stdout(f):
                    await locals()['__ex'](self=self)
                to_return = f.getvalue()

                await self.sio.emit('command', {'response': to_return, 'client': data.get('client')})
        
        @self.sio.event
        async def connect():
            print('i am connected')
            await self.sio.emit('join', {'room': 'server'})

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

                            temp = {
                                'Date':   datetime.fromtimestamp(time).strftime('%Y-%M-%d %H-%M-%S'),
                                'High':   float(candles[3]),
                                'Low':    float(candles[4]),
                                'Open':   float(candles[1]),
                                'Close':  float(candles[2]),
                                'Volume': float(candles[6])
                            }

                            if time > self.prevtime:
                                
                                self.close = temp['Close']
                                self.data = self.data.append(temp, ignore_index=True)
                                self.index += 1 
                                

                                await self._algorithm(self)


                                # caches dataframe to preserve memory
                                
                                if len(self.data) % self.mem_cache_size == 0:
                                    frame_cache_size = int(self.mem_cache_size / 2)
                                    dump_frame = self.data[0:frame_cache_size]
                                    _datetime = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
                                    _filename = f'{_datetime}.csv'
                                    _temp_filename = 'data.csv'
                                    _full_path = f'{self.data_path}{_temp_filename}'

                                    await append_to_csv(dump_frame, _full_path)
                                    print('cached dataframe')

                                    self.data = self.data.drop(range(0,frame_cache_size))
                                    self.data = self.data.reset_index(drop=True)
                                    self.index=len(self.data)-1

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

            if api_sandbox:
                client = WsToken(key=api_key, secret=api_secret, passphrase=api_passphrase, is_sandbox=api_sandbox, url=api_url) # websockets stuff 
            else:
                client = WsToken(key=api_key, secret=api_secret, passphrase=api_passphrase) # websockets stuff 

            self.ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)                              #
            await self.ws_client.subscribe('/market/candles:BTC-USDT_1min')  
            try:
                await self.sio.connect('http://127.0.0.1:5000')   
            except socketio.exceptions.ConnectionError as error:
                print('flask not connected')
            print('connected to kucoin socket')
            
            
            while True:
                await asyncio.sleep(60, loop=loop)

                    
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