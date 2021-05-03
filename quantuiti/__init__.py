import inspect
import os
import pandas as pd
import random
import matplotlib.pyplot as plt
from .__about__ import *
import glob
class Engine():
    """
    CompuTradeEngine helps you reliabley backtest your trading algorithms faster than ever.
    
        Parameters:
            backtest (bool): CompuTradeEngine will backtest your algorithm.
            build    (bool): CompuTradeEngine will build you algorithm in python and output it to a build directory in your current working directory.

    """

    from .core import algorithm, BuildPythonFile, graph, backtest_algorithm, build_indicator

    from .indicators import cci, ema, emv, roc, sma

    def __init__(self, backtest=True, build=False, graph=False, symbols=['AAPL'], stop_loss=-2):
        self.constuctors()
        self.symbols = symbols
        self.stop_loss = stop_loss
        # next block gets the callee's working directory
        frame_info = inspect.stack()[1]
        filepath = frame_info[1]
        filename=filepath
        del frame_info
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(f'/{filename}', '')
        self.path = filepath

        self.backtest = backtest
        self.build = build
        self.graph = graph

    def constuctors(self):
        self.algorithmFunc = None
        self.interval = 'd'
        self.symbols = ['AAPL']
        self.stop_loss = -5 # stop loss is a percentage default is -2%
        self.position = False
        self.shares = 0
        self.startBalance = 10000
        self.balance = self.startBalance
        self.rating = 0
        self.trades = []
        self.sells = []

    def buy(self):
        if self.shares == 0 and self.balance > 0 :
            self.shares = self.balance / self.data['Close'][self.index]
            self.balance = 0
            self.trades.append(tuple([self.shares, self.data['Close'][self.index]])) 
    
    def sell(self):
        if self.shares != 0:
            profit = ( self.data['Close'][self.index]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.sells.append(profit) 
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            self.shares = 0
    