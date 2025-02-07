import matplotlib.pyplot as plt

def plot_moving_averages(data, short_window, long_window):
    timestamps = data['timestamp']
    close_prices = data['close']
    short_ma = data[f'MA_{short_window}']
    long_ma = data[f'MA_{long_window}']
    
    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, close_prices, label='Close Prices', color='blue', linewidth=1)
    plt.plot(timestamps, short_ma, label=f'MA {short_window}', color='orange', linewidth=1)
    plt.plot(timestamps, long_ma, label=f'MA {long_window}', color='green', linewidth=1)
    
    for i in range(1, len(close_prices)):
        if short_ma.iloc[i] > long_ma.iloc[i] and short_ma.iloc[i-1] <= long_ma.iloc[i-1]:
            plt.scatter(timestamps.iloc[i], close_prices.iloc[i], color='green', marker='^', s=100)
        if short_ma.iloc[i] < long_ma.iloc[i] and short_ma.iloc[i-1] >= long_ma.iloc[i-1]:
            plt.scatter(timestamps.iloc[i], close_prices.iloc[i], color='red', marker='v', s=100)
    
    plt.title('Bitcoin Close Prices with Moving Averages and Crossovers')
    plt.xlabel('Timestamp')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
