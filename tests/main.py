import sys
sys.path.insert(1, '/home/dylan/Desktop/python-quantuiti')
from quantuiti import Engine

Engine = Engine(symbols=['AMD', 'GME', 'RIOT'], stop_loss=-3)


@Engine.algorithm
def algo():
    self.ema(10)
    if self.ema(50) > self.ema(100) :
        self.buy()
    else:
        self.sell()
