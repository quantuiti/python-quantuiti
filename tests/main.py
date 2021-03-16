import sys
sys.path.insert(1, '/home/dylan/Desktop/python-quantuiti')
from Quantuiti import Engine

Engine = Engine()
Engine.config()

@Engine.algorithm
def algo():
    if self.ema(10) > self.ema(20):
        self.buy()
    else:
        self.sell()