import numpy as np
import pandas as pd

def forecast_future_trend(data):
    future_trend = []

    macd = data['MACD']
    signal_line = data['Signal_Line']
    timestamps = data['timestamp']

    for i in range(1, len(macd)):
        if macd.iloc[i] > signal_line.iloc[i] and macd.iloc[i-1] <= signal_line.iloc[i-1]:
            future_trend.append((timestamps.iloc[i], 'Uptrend'))
        elif macd.iloc[i] < signal_line.iloc[i] and macd.iloc[i-1] >= signal_line.iloc[i-1]:
            future_trend.append((timestamps.iloc[i], 'Downtrend'))
    
    return future_trend

# Test the function
if __name__ == "__main__":
    file_path = 'bitcoin_data_with_indicators.csv'
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    future_trend = forecast_future_trend(data)
    
    print("Future Trend Forecast:")
    for timestamp, trend in future_trend[-10:]:
        print(f"{timestamp}: {trend}")
