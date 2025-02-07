import numpy as np
from sklearn.preprocessing import StandardScaler

def standardize_features(df, features):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    return X_scaled

def create_sequences(X, time_steps=1):
    Xs = []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
    return np.array(Xs)
