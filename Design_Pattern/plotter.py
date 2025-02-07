import mplfinance as mpf

def plot_candlestick(data, title):
    if 'volume' in data.columns:
        mpf.plot(data, type='candle', style='charles', title=title, ylabel='Price')
