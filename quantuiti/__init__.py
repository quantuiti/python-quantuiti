import inspect
import os
import pandas as pd
import random
import matplotlib.pyplot as plt
import glob

from .api import run_api
from .__about__ import *

class Engine():
    """
    CompuTradeEngine helps you reliabley backtest your trading algorithms faster than ever.
    
        Parameters:
            backtest (bool): CompuTradeEngine will backtest your algorithm.
            build    (bool): CompuTradeEngine will build you algorithm in python and output it to a build directory in your current working directory.

    """

    from .core import algorithm, BuildPythonFile, graph, backtest_algorithm, build_indicator, livetest_algorithm

    from .indicators import cci, ema, emv, roc, sma, macd

    def __init__(self, config=False, backtest=True ):
        self.constuctors()
        # next block gets the callee's working directory
        frame_info = inspect.stack()[1]
        filepath = frame_info[1]
        filename=filepath
        del frame_info
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(f'/{filename}', '')
        self.path = filepath
        if config:
            self.config(config=config)
        self.backtest = backtest

    def constuctors(self):
        self.algorithmFunc = None
        self.build = False
        self.interval = 'd'
        self.symbols = ['AAPL']
        self.bot_type = None
        self.stop_loss = -5 # stop loss is a percentage default is -2%
        self.position = False
        self.shares = 0
        self.startBalance = 10000
        self.balance = self.startBalance
        self.rating = 0
        self.trades = []
        self.sells = []
        self.client = {}
        self._algorithm = None
    async def buy(self):
        if self.shares == 0 and self.balance > 0 :
            self.shares = self.balance / self.data['Close'][self.index]
            self.balance = 0
            self.trades.append(tuple([self.shares, self.data['Close'][self.index]]))
            if getattr(self, 'sio') is not None:
                await self.sio.emit('buy', {
                    'buy': {
                        'shares': self.shares,
                        'balance': self.balance,
                        'price': self.close 

                    }
                })
         
    
    async def sell(self):
        if self.shares != 0:
            profit = ( self.data['Close'][self.index]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.sells.append(profit) 
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            if getattr(self, 'sio') is not None:
                await self.sio.emit('sell', {
                    'sell': {
                        'shares': self.shares,
                        'balance': self.balance,
                        'price': self.close 
                    }
                })
            self.shares = 0
    
    def config(self, config: dict):
        
        bot_type_check = ['crypto', 'Crypto', 'stock', 'Stock']
        symbols_check = ['symbols', 'Symbols']
        client_check = ['client', 'Client']
        client_name_check = ['kucoin']

        for bot_type in bot_type_check:
            if config.get(bot_type):
                for symbol in symbols_check:
                    if config.get(bot_type).get(symbol):
                        if type( config.get(bot_type).get(symbol)) == list:
                            self.symbols = config.get(bot_type).get(symbol)
                            break
                        else:
                            print('symbols provided in config is not of type', list)
                            exit()
                        print(config.get(bot_type).get(symbol))
                        
                            
                    if symbol == symbols_check[-1]:
                        print('no symbols supplied in config')
                        exit()
                
                for client in client_check:
                    if config.get(bot_type).get(client):
                        for client_name in client_name_check:
                            if config.get(bot_type).get(client).get('name') == client_name:
                                
                                if client_name == 'kucoin':
                                    if config.get(bot_type).get(client).get('api_key'):
                                        self.client['api_key'] = config.get(bot_type).get(client).get('api_key')
                                    else:
                                        print('api_key not supplied')
                                        exit()

                                    if config.get(bot_type).get(client).get('api_secret'):
                                        self.client['api_secret'] = config.get(bot_type).get(client).get('api_secret')
                                    else:
                                        print('api_secret not supplied')
                                        exit()
                                    
                                    if config.get(bot_type).get(client).get('api_passphrase'):
                                        self.client['api_passphrase'] = config.get(bot_type).get(client).get('api_passphrase')
                                    else:
                                        print('api_passphrase not supplied')
                                        exit()

                                    if config.get(bot_type).get(client).get('api_url'):
                                        self.client['api_url'] = config.get(bot_type).get(client).get('api_url')
                                    else:
                                        print('api_url not supplied')
                                        exit()
                                else:
                                    exit()

                                self.client['type'] = bot_type.lower()
                                print(self.client['type'])
                                break

                            if client_name == client_name_check[-1]:
                                print( config.get(bot_type).get(client).get('name'), 'is not supported' )
                    break
                break

                
            if bot_type == bot_type_check[-1]:
                print('config not supplied correctly')
                exit()
                """
                    todo:
                        link to browser source that shows how to input config correctly
                """

        
                