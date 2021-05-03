from quantuiti import Engine

engine = Engine()

@Engine.build_indicator
def indicate(self):


@Engine.algorithm
def algo():
    if self.ema(20) > self.ema(100):
        self.buy()
    else:
        self.sell()