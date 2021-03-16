# import required packages 
import matplotlib.pyplot as plt 
import mplfinance as mpf
import pandas as pd 
import matplotlib.dates as mpdates 

def graph(self):
    df = self.data[['Open', 'High', 'Low', 'Close', 'Volume', 'ema_10']]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})
    fig = mpf.figure(figsize=(10, 7), style=s) # pass in the self defined style to the whole canvas
    ax = fig.add_subplot(2,1,1) # main candle stick chart subplot, you can also pass in the self defined style here only for this subplot
    av = fig.add_subplot(2,1,2, sharex=ax)  # volume chart subplot
    ema10_plot = mpf.make_addplot(self.data['ema_10'], panel=2, ylabel='ema_10', ax=ax)
    ema20_plot = mpf.make_addplot(self.data['ema_20'], panel=2, ylabel='ema_20', ax=ax)
    mpf.plot(df, type='candle', ax=ax, volume=av, addplot=[ema10_plot, ema20_plot])
    mpf.show()
    