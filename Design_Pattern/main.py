import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, StringVar
import os
from data_loader import load_data
from pattern_detector import detect_patterns

def select_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_var.set(file_path)

def load_data_from_files():
    file_path_daily = daily_file_path.get()
    file_path_minutes = minutes_file_path.get()
    
    if not file_path_daily or not file_path_minutes:
        messagebox.showerror("LỖI!", "Hãy chọn cả hai tệp CSV.")
        return
    
    try:
        global df_daily, df_minutes
        df_daily = load_data(file_path_daily)
        df_minutes = load_data(file_path_minutes)
        messagebox.showinfo("Thành công", "Dữ liệu đã được tải thành công.")
    except Exception as e:
        messagebox.showerror("LỖI!", str(e))

def plot_candlestick(data, title):
    mpf.plot(data, type='candle', style='charles', title=title, ylabel='Price')

def plot_patterns(data, patterns, title):
    # Vẽ biểu đồ nến
    fig, axlist = mpf.plot(data, type='candle', style='charles', ylabel='Price', title=title, returnfig=True, figsize=(15, 10))

    ax = axlist[0]  # Lấy trục đầu tiên (chính)

    # Thêm các marker vào biểu đồ
    colors = {'Bullish Engulfing': 'green', 'Bearish Engulfing': 'red', 'Three Inside Up': 'blue', 'Three Inside Down': 'purple'}
    markers = {'Bullish Engulfing': '^', 'Bearish Engulfing': 'v', 'Three Inside Up': 's', 'Three Inside Down': 'p'}
    
    for pattern_name, pattern_indices in patterns.items():
        for index in pattern_indices:
            y_value = data.loc[index, 'close']  # Lấy giá trị close tương ứng
            x_value = data.index.get_loc(index)  # Chuyển đổi Timestamp thành giá trị số
            
            # Vẽ marker tại vị trí của pattern
            ax.scatter(x_value, y_value, color=colors[pattern_name], marker=markers[pattern_name], s=100, label=pattern_name)
    
    # Lọc trùng lặp trong phần chú giải
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')

    # Điều chỉnh khoảng cách giữa các nhãn trục x
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Giảm số lượng nhãn trục x để có khoảng cách rộng hơn
    plt.xticks(rotation=45)  # Xoay nhãn trục x để dễ đọc hơn

    # Sử dụng subplots_adjust để điều chỉnh khoảng cách các thành phần
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    plt.show()

def process_data():
    start_date_str = start_entry.get()
    end_date_str = end_entry.get()
    
    try:
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)
        
        if start_date >= end_date:
            messagebox.showerror("LỖI!", "Ngày kết thúc phải sau ngày bắt đầu.")
            return
        
        specific_period_minutes = df_minutes[(df_minutes.index >= start_date) & (df_minutes.index <= end_date)]
        if specific_period_minutes.empty:
            messagebox.showerror("LỖI!", "Không có dữ liệu có sẵn trong khoảng thời gian nhất định.")
            return
        
        # Nhận diện các pattern trong dữ liệu từng phút
        patterns_minutes = detect_patterns(specific_period_minutes)
        
        # Vẽ biểu đồ nến và nhận diện pattern cho dữ liệu từng phút
        plot_patterns(specific_period_minutes, patterns_minutes, 'Pattern Biểu đồ nến - Khoảng thời gian cụ thể')
    except Exception as e:
        messagebox.showerror("LỖI!", str(e))

def plot_daily_data():
    # Xử lý dữ liệu hàng ngày
    end_date_daily = df_daily.index.max()
    start_date_daily = end_date_daily - pd.DateOffset(days=30)
    specific_period_daily = df_daily[(df_daily.index >= start_date_daily) & (df_daily.index <= end_date_daily)]
    
    # Vẽ biểu đồ nến cho dữ liệu hàng ngày (30 ngày trước ngày cuối cùng)
    plot_candlestick(specific_period_daily, 'Biểu đồ nến - 30 ngày trước ngày cuối cùng')

# Tạo giao diện người dùng
root = Tk()
root.title("Bitcoin Data Analyzer")

daily_file_path = StringVar()
minutes_file_path = StringVar()

Label(root, text="File CSV hàng ngày:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=daily_file_path, width=40).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=lambda: select_file(daily_file_path)).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="File CSV từng phút:").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=minutes_file_path, width=40).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=lambda: select_file(minutes_file_path)).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Load Data", command=load_data_from_files).grid(row=2, column=0, columnspan=3, pady=10)

Label(root, text="Start Date (YYYY-MM-DD HH:MM)").grid(row=3, column=0, padx=10, pady=10)
Label(root, text="End Date (YYYY-MM-DD HH:MM)").grid(row=4, column=0, padx=10, pady=10)

start_entry = Entry(root)
end_entry = Entry(root)

start_entry.grid(row=3, column=1, padx=10, pady=10)
end_entry.grid(row=4, column=1, padx=10, pady=10)

Button(root, text="Nhận Diện", command=process_data).grid(row=5, column=0, columnspan=2, pady=10)
Button(root, text="Biểu đồ nến (Tháng)", command=plot_daily_data).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
