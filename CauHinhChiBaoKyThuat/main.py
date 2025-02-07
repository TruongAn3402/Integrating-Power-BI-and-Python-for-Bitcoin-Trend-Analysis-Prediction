import pandas as pd
from ma import calculate_ma
from ema import calculate_ema
from macd import calculate_macd
from rsi import calculate_rsi
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Hàm để tải dữ liệu bằng hộp thoại chọn tệp
def load_dataset():
    file_path = filedialog.askopenfilename(title="Chọn tệp CSV", filetypes=(("Tệp CSV", "*.csv"), ("Tất cả tệp", "*.*")))
    if not file_path:
        messagebox.showwarning("Không có tệp nào được chọn", "Vui lòng chọn một tệp CSV.")
        return None
    return pd.read_csv(file_path), file_path

def process_data():
    data, file_path = load_dataset()
    if data is None:
        return
    
    # Tính toán các chỉ báo kỹ thuật
    data['MA_7'] = calculate_ma(data, 7)
    data['MA_25'] = calculate_ma(data, 25)
    data['MA_99'] = calculate_ma(data, 99)
    data['EMA_7'] = calculate_ema(data, 7)
    data['EMA_30'] = calculate_ema(data, 30)
    data['MACD'], data['Signal_Line'] = calculate_macd(data)
    data['RSI_6'] = calculate_rsi(data, 6)
    data['RSI_14'] = calculate_rsi(data, 14)
    
    # Xử lý các giá trị thiếu bằng cách loại bỏ các hàng có giá trị thiếu
    data.dropna(inplace=True)
    
    # Lưu tập dữ liệu mới vào tệp CSV
    output_file_path = 'bitcoin_technical_indicators_cleaned.csv'
    data.to_csv(output_file_path, index=False)
    
    messagebox.showinfo("Hoàn thành xử lý", f"Tệp đã được lưu vào {output_file_path}")

def create_ui():
    root = tk.Tk()
    root.title("Bộ xử lý chỉ báo kỹ thuật Bitcoin")
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Thiết lập kiểu dáng để tăng tính thẩm mỹ
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 14))
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill="both")

    # Tạo nhãn
    label = ttk.Label(frame, text="Bộ xử lý chỉ báo kỹ thuật Bitcoin")
    label.pack(pady=10)
    
    # Tạo nút để tải và xử lý dữ liệu
    load_button = ttk.Button(frame, text="Tải và xử lý CSV", command=process_data)
    load_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
