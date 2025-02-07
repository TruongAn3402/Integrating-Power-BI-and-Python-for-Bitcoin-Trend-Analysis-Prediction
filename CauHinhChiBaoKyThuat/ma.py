import pandas as pd

def calculate_ma(data, window):
    return data['close'].rolling(window=window).mean()
