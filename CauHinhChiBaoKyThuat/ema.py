import pandas as pd

def calculate_ema(data, window):
    return data['close'].ewm(span=window, adjust=False).mean()
