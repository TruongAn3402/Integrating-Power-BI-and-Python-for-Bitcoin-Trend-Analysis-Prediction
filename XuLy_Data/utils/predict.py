import joblib
import numpy as np
import xgboost as xgb
from keras.models import model_from_json

def load_model_and_predict(model_file, X_scaled, time_steps=1, model_type="traditional"):
    if model_type == "traditional":
        if model_file.endswith(".json"):
            model = xgb.Booster()
            model.load_model(model_file)
            dmatrix = xgb.DMatrix(X_scaled)
            predictions = model.predict(dmatrix)
            predictions = (predictions > 0.5).astype("int32")
        else:
            model = joblib.load(model_file)
            predictions = model.predict(X_scaled)
    else:
        X_seq = create_sequences(X_scaled, time_steps)
        with open(model_file.replace(".h5", ".json"), "r") as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json)
        model.load_weights(model_file)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
        predictions = model.predict(X_seq)
        predictions = (predictions > 0.5).astype("int32").flatten()
        predictions = np.pad(predictions, (time_steps, 0), mode='constant', constant_values=0)
    return predictions

def create_sequences(X, time_steps=1):
    Xs = []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
    return np.array(Xs)
