from pandas_datareader import data as pdr
def backtest_algorithm(self):
    symbols = self.symbols
    for symbol in symbols:
        self.CurrentSymbol = symbol
        self.index=0
        self.data = pdr.get_data_yahoo(symbols=symbol, interval=self.interval, start='JAN-01-2020', end='DEC-28-2020') # iterates over symbols by symbol to backtest algorithm on symbol data
        self.close = self.data['Close']
        for index, rows in self.data.iterrows():
            if self.shares != 0:
                self.investment_gain = ((self.data['Close'][self.index] - self.trades[-1][1]) / self.trades[-1][1]) * 100
                if self.investment_gain < self.stop_loss:
                    self.sell()
            self.algo(self)


            self.index+=1

        if self.shares != 0:
            profit = ( self.data['Close'][-1]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.sells.append(profit) 
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            self.shares = 0

              
        roi = ((self.balance - self.startBalance) / self.startBalance) * 100
        self.success = [0,0]
        self.success[1] = self.success[1] + len(self.sells)
        for i in range(len(self.sells)):
            if self.sells[i] > 0:
                self.success[0] = self.success[0] + 1




        self.balance = 10000
        self.shares = 0

        self.rating += roi
        if self.graph:
            self.graph()

    success = [(self.success[0] / self.success[1]) * 100, self.success[1]]
    print(f'trade success: %{success[0]} out of {success[1]} trades')
    print(f'rating: %{self.rating}')
