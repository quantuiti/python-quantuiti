import numpy as np
def ema(self, N):
    """
    Simple Moving Average = (N - PeriodSum) / N

    N = number of days in a given period

    PeriodSum = sum of stock closing prices in that period
    """
    name = 'ema_' + str(N)
    dependent = 'sma_' + str(N)

    if not self.backtest:
        if N < len(self.data):
            self.sma(N)
            temp=[]
            for index, row in self.data.iterrows():
                if np.isnan(row[dependent]):
                    temp.append(row[dependent])
                else:
                    if np.isnan(temp[-1]):
                        ema = (self.data['Close'][index] - self.data[dependent][index]) * (2 / (N + 1)) + self.data[dependent][index]
                    else:
                        ema = (self.data['Close'][index] - temp[-1]) * (2 / (N + 1)) + temp[-1]
                    
                    temp.append(ema)
            
            self.data[name] = temp
            return temp[self.index]
        elif len(self.data) > N:
            ema = (self.data['Close'][self.index-1] - self.data[name][self.index-1]) * (2 / (N + 1)) + self.data[name][self.index-1]

            temp = self.data[name].append(ema)
            self.data[name] = temp
            return ema

    elif self.backtest:
        try:
            return self.data[name][self.index]
                
        except Exception as error:
            self.sma(N)
            temp=[]
            for index, row in self.data.iterrows():
                if np.isnan(row[dependent]):
                    temp.append(row[dependent])
                else:
                    if np.isnan(temp[-1]):
                        ema = (self.data['Close'][index] - self.data[dependent][index]) * (2 / (N + 1)) + self.data[dependent][index]
                    else:
                        ema = (self.data['Close'][index] - temp[-1]) * (2 / (N + 1)) + temp[-1]
                    
                    temp.append(ema)
            
            self.data[name] = temp
            return self.data[name][self.index]
                    
                    
            # setattr(self, name, [sma])
