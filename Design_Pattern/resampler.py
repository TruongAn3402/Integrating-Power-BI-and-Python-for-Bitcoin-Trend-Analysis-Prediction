def resample_data(df, period):
    resampled_data = df.resample(period).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })
    return resampled_data
