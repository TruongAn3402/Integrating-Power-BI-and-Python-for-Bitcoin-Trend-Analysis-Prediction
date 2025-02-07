def detect_patterns(df):
    patterns = {
        'Bullish Engulfing': [],
        'Bearish Engulfing': [],
        'Three Inside Up': [],
        'Three Inside Down': []
    }
    
    for i in range(2, len(df)-1):
        # Bullish Engulfing
        if (df['close'].iloc[i] > df['open'].iloc[i] and df['close'].iloc[i-1] < df['open'].iloc[i-1] and
            df['open'].iloc[i] < df['close'].iloc[i-1] and df['close'].iloc[i] > df['open'].iloc[i-1]):
            patterns['Bullish Engulfing'].append(df.index[i])
        
        # Bearish Engulfing
        if (df['close'].iloc[i] < df['open'].iloc[i] and df['close'].iloc[i-1] > df['open'].iloc[i-1] and
            df['open'].iloc[i] > df['close'].iloc[i-1] and df['close'].iloc[i] < df['open'].iloc[i-1]):
            patterns['Bearish Engulfing'].append(df.index[i])
        
        # Three Inside Up
        if (df['close'].iloc[i-2] < df['open'].iloc[i-2] and  # Cây nến đầu tiên phải là nến giảm
            df['close'].iloc[i-1] > df['open'].iloc[i-1] and  # Cây nến thứ hai phải là nến tăng
            df['close'].iloc[i-1] > (df['open'].iloc[i-2] + df['close'].iloc[i-2]) / 2 and  # Giá đóng cửa của cây nến thứ hai phải nằm trên mức 50% của thân nến đầu tiên
            df['close'].iloc[i-1] <= df['open'].iloc[i-2] and  # Giá đóng cửa của cây nến thứ hai không được cao hơn giá mở cửa của cây nến đầu tiên
            df['close'].iloc[i] > df['open'].iloc[i] and  # Cây nến thứ ba phải là nến tăng
            df['close'].iloc[i] > df['open'].iloc[i-2]):  # Giá đóng cửa của cây nến thứ ba phải cao hơn giá mở cửa của cây nến đầu tiên
            patterns['Three Inside Up'].append(df.index[i])
        
        # Three Inside Down
        if (df['close'].iloc[i-2] > df['open'].iloc[i-2] and  # Cây nến đầu tiên phải là nến tăng
            df['close'].iloc[i-1] < df['open'].iloc[i-1] and  # Cây nến thứ hai phải là nến giảm
            df['close'].iloc[i-1] < (df['open'].iloc[i-2] + df['close'].iloc[i-2]) / 2 and  # Giá đóng cửa của cây nến thứ hai phải nằm dưới mức 50% của thân nến đầu tiên
            df['close'].iloc[i-1] >= df['open'].iloc[i-2] and  # Giá đóng cửa của cây nến thứ hai không được thấp hơn giá mở cửa của cây nến đầu tiên
            df['close'].iloc[i] < df['open'].iloc[i] and  # Cây nến thứ ba phải là nến giảm
            df['close'].iloc[i] < df['open'].iloc[i-2]):  # Giá đóng cửa của cây nến thứ ba phải thấp hơn giá mở cửa của cây nến đầu tiên
            patterns['Three Inside Down'].append(df.index[i])
    
    return patterns
