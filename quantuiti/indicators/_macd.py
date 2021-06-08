import numpy as np
def macd(self, short:int=12, long:int=26, return_series:bool=False, return_previous:bool=False):
    """
    MACD (Moving Average Convergence Divergence):
        MACD = (Short EMA) - (Long EMA)

    
    """
    name = f'macd_{short}_{long}'
    if return_series:
        return self.data[name]
    
    if return_previous:

        last_valid_macd = self.data[name].last_valid_index()
        if type(last_valid_macd) is not None:      #double logic cuz bruh
            if type(None) is not type(last_valid_macd):
                return self.data[name].iloc[last_valid_macd-1]
                
            
        
    if not self.backtest:
        if name in self.data.columns:
            if not np.isnan(self.data[name].iloc[-1]):
                macd = self.data[name].iloc[-1] 
                return macd
            

        long_ema = self.ema(long)
        short_ema = self.ema(short)
        diverge = short_ema - long_ema
        
        self.data.loc[self.index, name] = diverge
        return diverge

    elif self.backtest:
        pass