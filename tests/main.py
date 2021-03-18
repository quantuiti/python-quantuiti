import sys
sys.path.insert(1, '/home/dylan/Desktop/python-quantuiti')
from Quantuiti import Engine

Engine = Engine()

@Engine.algorithm
def algo():
    self.ema(10)
    if self.ema(50) > self.ema(100) :
        self.buy()
    else:
        self.sell()