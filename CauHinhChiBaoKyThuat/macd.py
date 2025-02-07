import pandas as pd

def calculate_macd(data):
    ema_12 = data['close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['close'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal_line = macd.ewm(span=9, adjust=False).mean()
    return macd, signal_line
