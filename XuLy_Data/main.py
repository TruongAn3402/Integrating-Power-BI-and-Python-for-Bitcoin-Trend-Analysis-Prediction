import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils.load_data import load_dataset
from utils.preprocess import standardize_features
from utils.predict import load_model_and_predict
from utils.plot import plot_predictions

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def run_prediction():
    file_path = entry_file_path.get()
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File không tồn tại. Vui lòng kiểm tra đường dẫn và thử lại.")
        return

    model_choice = model_var.get()
    time_steps = 10  # Số bước thời gian cho các mô hình LSTM/GRU

    if model_choice == 1:
        model_file = "models/random_forest_model.pkl"
        output_file = 'data/bitcoin_technical_indicators_with_predictions_rf.csv'
        model_type = "traditional"
        model_name = "Random Forest"
    elif model_choice == 2:
        model_file = "models/gb_model.pkl"
        output_file = 'data/bitcoin_technical_indicators_with_predictions_gb.csv'
        model_type = "traditional"
        model_name = "Gradient Boosting"
    elif model_choice == 3:
        model_file = "models/xgb_model.json"
        output_file = 'data/bitcoin_technical_indicators_with_predictions_xgb.csv'
        model_type = "traditional"
        model_name = "XGBoost"
    elif model_choice == 4:
        model_file = "models/lstm_model.h5"
        output_file = 'data/bitcoin_technical_indicators_with_predictions_lstm.csv'
        model_type = "lstm_gru"
        model_name = "LSTM"
    elif model_choice == 5:
        model_file = "models/gru_model.h5"
        output_file = 'data/bitcoin_technical_indicators_with_predictions_gru.csv'
        model_type = "lstm_gru"
        model_name = "GRU"
    else:
        messagebox.showerror("Error", "Lựa chọn mô hình không hợp lệ. Vui lòng chọn một mô hình hợp lệ.")
        return

    df = load_dataset(file_path)
    features = ['close', 'MA_7', 'MA_25', 'MA_99', 'EMA_7', 'EMA_30', 'MACD', 'Signal_Line', 'RSI_6', 'RSI_14']
    X_scaled = standardize_features(df, features)
    predictions = load_model_and_predict(model_file, X_scaled, time_steps, model_type)
    df['predicted_trend'] = predictions
    df.to_csv(output_file, index=False)
    messagebox.showinfo("Success", f"Dự đoán đã được thêm vào file và lưu dưới tên {output_file}")

def plot_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    df = load_dataset(file_path)
    if 'predicted_trend' not in df.columns:
        messagebox.showerror("Error", "File đã chọn không có cột 'predicted_trend'. Vui lòng chọn file hợp lệ.")
        return
    model_name = file_path.split('_')[-1].split('.')[0].upper()
    plot_predictions(df, model_name)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Dự đoán xu hướng Bitcoin")

# Tạo và đặt các widget
tk.Label(root, text="Chọn file CSV:").grid(row=0, column=0, padx=10, pady=10)
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Chọn mô hình:").grid(row=1, column=0, padx=10, pady=10)
model_var = tk.IntVar()
tk.Radiobutton(root, text="Random Forest", variable=model_var, value=1).grid(row=1, column=1, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Gradient Boosting", variable=model_var, value=2).grid(row=2, column=1, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="XGBoost", variable=model_var, value=3).grid(row=3, column=1, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="LSTM", variable=model_var, value=4).grid(row=4, column=1, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="GRU", variable=model_var, value=5).grid(row=5, column=1, padx=10, pady=5, sticky="w")

tk.Button(root, text="Chạy dự đoán", command=run_prediction).grid(row=6, column=0, columnspan=3, padx=10, pady=10)
tk.Button(root, text="Vẽ biểu đồ từ CSV", command=plot_from_csv).grid(row=7, column=0, columnspan=3, padx=10, pady=10)

# Chạy vòng lặp chính
root.mainloop()
