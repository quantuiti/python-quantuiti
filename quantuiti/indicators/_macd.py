def macd(self, short:int=12, long:int=26, return_series:bool=False):
    """
    MACD (Moving Average Convergence Divergence):
        MACD = (Short EMA) - (Long EMA)

    
    """
    name = f'macd_{short}_{long}'
    if return_series:
        return self.data[name]
        
    if not self.backtest:
        long_ema = self.ema(long)
        short_ema = self.ema(short)
        diverge = self.ema(26) - self.ema(12)
        self.data.loc[self.index, name] = diverge
        return diverge

    elif self.backtest:
        pass