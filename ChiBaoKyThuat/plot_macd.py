import matplotlib.pyplot as plt

def plot_macd(data):
    timestamps = data['timestamp']
    macd = data['MACD']
    signal_line = data['Signal_Line']
    
    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, macd, label='MACD', color='blue', linewidth=1)
    plt.plot(timestamps, signal_line, label='Signal Line', color='red', linewidth=1)
    
    for i in range(1, len(macd)):
        if macd.iloc[i] > signal_line.iloc[i] and macd.iloc[i-1] <= signal_line.iloc[i-1]:
            plt.scatter(timestamps.iloc[i], macd.iloc[i], color='green', marker='^', s=100)
        if macd.iloc[i] < signal_line.iloc[i] and macd.iloc[i-1] >= signal_line.iloc[i-1]:
            plt.scatter(timestamps.iloc[i], macd.iloc[i], color='red', marker='v', s=100)
    
    plt.title('MACD and Signal Line with Crossovers')
    plt.xlabel('Timestamp')
    plt.ylabel('MACD')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
