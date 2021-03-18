from quantuiti import Engine

Engine = Engine()

@Engine.algorithm
def algo():
    if self.ema(20) > self.ema(100):
        self.buy()
    else:
        self.sell()