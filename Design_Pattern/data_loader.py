import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    required_columns = ['timestamp', 'open', 'high', 'low', 'close']
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột {col} trong file CSV")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    return df
