import matplotlib.pyplot as plt
import pandas as pd

def plot_rsi(data):
    timestamps = data['timestamp']
    rsi = data['RSI_14']
    
    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, rsi, label='RSI 14', color='purple', linewidth=1)
    plt.axhline(70, color='red', linestyle='--', linewidth=1)
    plt.axhline(30, color='green', linestyle='--', linewidth=1)
    
    plt.title('RSI 14')
    plt.xlabel('Timestamp')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
