import pandas as pd
from load_and_prepare_data import load_and_prepare_data
from plot_moving_averages import plot_moving_averages
from plot_macd import plot_macd
from plot_rsi import plot_rsi
from forecast_future_trend import forecast_future_trend
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Hàm để tải dữ liệu bằng hộp thoại chọn tệp
def load_dataset():
    file_path = filedialog.askopenfilename(title="Chọn tệp CSV", filetypes=(("Tệp CSV", "*.csv"), ("Tất cả tệp", "*.*")))
    if not file_path:
        messagebox.showwarning("Không có tệp nào được chọn", "Vui lòng chọn một tệp CSV.")
        return None
    return file_path

def process_data():
    file_path = load_dataset()
    if not file_path:
        return

    data = load_and_prepare_data(file_path)

    # Vẽ các chỉ báo kỹ thuật và dự báo xu hướng
    plot_moving_averages(data, 7, 25)
    plot_macd(data)
    plot_rsi(data)

    # Dự báo xu hướng tương lai
    future_trend = forecast_future_trend(data)

    # In kết quả dự báo xu hướng tương lai
    forecast_text = "Dự báo xu hướng:\n"
    for timestamp, trend in future_trend[-10:]:
        forecast_text += f"{timestamp}: {trend}\n"
    
    messagebox.showinfo("Dự báo xu hướng", forecast_text)

def create_ui():
    root = tk.Tk()
    root.title("Bộ xử lý chỉ báo kỹ thuật Bitcoin")
    root.geometry("500x300")
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
