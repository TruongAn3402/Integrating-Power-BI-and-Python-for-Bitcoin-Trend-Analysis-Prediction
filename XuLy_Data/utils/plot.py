import matplotlib.pyplot as plt
import numpy as np

def plot_predictions(df, model_name):
    close_prices = df['close']
    predictions = df['predicted_trend']
    timestamps = df['timestamp']

    trend_x = [0]
    trend_y = [close_prices[0]]

    for i in range(1, len(predictions)):
        if predictions[i] != predictions[i-1]:
            trend_x.append(i)
            trend_y.append(close_prices[i])

    trend_x.append(len(predictions) - 1)
    trend_y.append(close_prices[len(predictions) - 1])

    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, close_prices, label='Close Prices', color='blue', linewidth=1)

    for i in range(1, len(trend_x)):
        segment_x = np.array(timestamps)[[trend_x[i-1], trend_x[i]]]
        segment_y = [trend_y[i-1], trend_y[i]]
        if predictions[trend_x[i-1]] == 1:
            plt.plot(segment_x, segment_y, color='green', linewidth=2, linestyle='-')
        else:
            plt.plot(segment_x, segment_y, color='red', linewidth=2, linestyle='-')

    plt.xlabel('Timestamp')
    plt.ylabel('Close Price')
    plt.title(f'Bitcoin Close Prices with Trend Lines - {model_name}')
    plt.legend()
    plt.xticks(np.arange(0, len(timestamps), step=30), rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
