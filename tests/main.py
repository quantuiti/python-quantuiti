import sys
import os
sys.path.insert(1, '/home/dylan/Desktop/quantuiti/python-quantuiti')
print(os.getcwd())
from quantuiti import Engine

Engine = Engine(backtest=False)

Engine.config({
    'crypto': {
        'symbols': ['BTC-USDT'],
        'client': {
            'name': 'kucoin',
            'api_key': '60943b2e365ac600068a1356',
            'api_secret': 'ee810109-9b22-4f59-9966-71b2d219352f' ,
            'api_passphrase': 'passphrase',
            'api_url': 'https://openapi-sandbox.kucoin.com'
        }
    }
})

@Engine.algorithm
def algo():
    # print('BTC-USDT price average', self.ema(5))
    self.ema(5)
    print(self.close)

