import sys
import os
from dotenv import load_dotenv
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, dir_path)
from quantuiti import Engine

Engine = Engine(backtest=False)

load_dotenv()
Engine.config({
    'crypto': {
        'symbols': ['BTC-USDT'],
        'client': {
            'name': 'kucoin',
            'api_key': os.getenv('api_key'),
            'api_secret':  os.getenv('api_secret'),
            'api_passphrase': os.getenv('api_passphrase'),
            'api_url': os.getenv('api_url')
        }
    }
})

@Engine.algorithm
async def algo(weiners):
    if self.macd() > 0 :
        if self.macd() > self.macd(return_previous=True):
            await self.buy()
    elif self.macd() < self.macd(return_previous=True):
        await self.sell()  
