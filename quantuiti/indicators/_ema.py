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
        if len(self.data) <= N:
            self.sma(N)

            temp=[]
            for index, row in self.data.iterrows():
                self.sma(N)
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

        elif len(self.data) > N: # uses less compute power as dataset gets bigger

            # if already exists send existing data to save computation
            if not np.isnan(self.data[name].iloc[-1]):
                ema = self.data[name].iloc[-1]
                return ema

            else:
                try:
                    prev_ema = self.data[name].iloc[self.index-1]

                except Exception:
                    last_valid_index = self.data[name].last_valid_index()
                    prev_ema = self.data[name].iloc[last_valid_index]
                    print('last valid index', last_valid_index)
                    exit()
                last_valid_close = self.data['Close'].last_valid_index()
                ema = (self.data['Close'].iloc[last_valid_close] - prev_ema) * (2 / (N + 1)) + prev_ema
                if np.isnan(ema):
                    print(self.data)
                    print(name, prev_ema)
                    print(self.index)
                    exit()

                self.data.at[self.index, name] = ema    #fecling buggggugig

                # self.data[name][self.index] = ema
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
