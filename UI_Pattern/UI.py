# Import các thư viện cần thiết
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from ultralytics import YOLO
import cv2  # Thư viện OpenCV cho các tác vụ xử lý ảnh

# Định nghĩa lớp: Tạo danh sách nhãn lớp cho mô hình YOLOv8.
classes = ['Bearish-Engulfing', 'Bullish-Engulfing', 'Three Inside Up-Down', 'Three-Inside-Down', 'Three-Inside-Up']

# Tạo 1 hàm detect_objects truyền vào tham số image
def detect_objects(model, image):
    # Thực hiện phát hiện đối tượng trên hình ảnh đầu vào bằng cách sử dụng đối tượng model
    results = model.predict(source=image, conf=0.25, iou=0.45)
    # Lấy kết quả dự đoán từ YOLOv8
    predictions = results[0].boxes.data.cpu().numpy()
    # Tạo một bản sao của hình ảnh đầu vào sẽ được sửa đổi để vẽ các hộp giới hạn xung quanh các đối tượng được phát hiện.
    output_image = image.copy()
    confidences = []  # Tạo danh sách lưu trữ các giá trị conf
    detected_classes = []  # Tạo danh sách lưu trữ các nhãn lớp đã phát hiện
    rightmost_box = None  # Biến lưu trữ hộp giới hạn bên phải nhất

    # Lặp qua từng dự đoán trong mảng dự đoán.
    for pred in predictions:
        # Trích xuất ID lớp và điểm tin cậy từ dự đoán hiện tại.
        class_id, conf = int(pred[5]), pred[4]
        # Kiểm tra xem điểm tin cậy của dự đoán hiện tại có lớn hơn hoặc bằng 0.1 hay không. Nếu không, dự đoán sẽ bị bỏ qua.
        if conf >= 0.05:
            # Vẽ một bounding box xung quanh đối tượng được phát hiện trên tệp output_image.
            cv2.rectangle(output_image, (int(pred[0]), int(pred[1])), (int(pred[2]), int(pred[3])), (0, 255, 0), 2)
            # Thêm nhãn vào hộp giới hạn với tên của đối tượng được phát hiện.
            cv2.putText(output_image, classes[class_id], (int(pred[0]), int(pred[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            confidences.append(conf)  # Thêm giá trị conf vào danh sách
            detected_classes.append((classes[class_id], pred))  # Thêm nhãn lớp và vị trí hộp giới hạn vào danh sách

            # Kiểm tra và cập nhật hộp giới hạn bên phải nhất
            if rightmost_box is None or pred[2] > rightmost_box[1][2]:
                rightmost_box = (classes[class_id], pred)

    # Trả về phần đã sửa đổi output_image với các hộp giới hạn và nhãn được vẽ xung quanh các đối tượng được phát hiện.
    return output_image, confidences, rightmost_box

# Hàm app(): tạo ra ứng dụng Streamlit và định nghĩa luồng làm việc cho ứng dụng.
def app():
    # Tránh việc hiện lỗi đỏ lên UI
    with st.container():
        st.title('Bài toán nhận diện pattern nến với YOLOv8')

        # Tạo ra một trình tải lên tệp trong ứng dụng Streamlit
        uploaded_model = st.file_uploader("Vui lòng chọn model YOLOv8...", type=["pt"])
        if uploaded_model is not None:
            with open("selected_model.pt", "wb") as f:
                f.write(uploaded_model.getbuffer())
            model = YOLO("selected_model.pt")
            st.success("Model đã được tải lên thành công!")

            uploaded_file = st.file_uploader("Vui lòng chọn hình ảnh...", type=["jpg", "jpeg", "png"])
            
            # Thao tác này kiểm tra xem một tệp đã được tải lên chưa, nghĩa là uploaded_file không phải tệp None.
            if uploaded_file is not None:
                # Đọc hình ảnh từ tệp đã tải lên và chuyển đổi nó thành một mảng numpy
                image = Image.open(uploaded_file)
                image = np.array(image)

                # Gọi hàm detect_objects() có input image để thực hiện phát hiện đối tượng trên hình ảnh đã tải lên và lưu trữ đầu ra ở định dạng output_image.
                output_image, confidences, rightmost_box = detect_objects(model, image)
                
                # Hiển thị cả hình ảnh đầu vào ban đầu và hình ảnh có các đối tượng được phát hiện trong ứng dụng Streamlit bằng cách sử dụng st.image()
                st.image([image, output_image], caption=['Input Image', 'Output Image'], width=800)
                # Hiển thị giá trị conf
                st.write("Confidences:", confidences)

                # Kiểm tra xu hướng Bitcoin dựa trên pattern cuối cùng được phát hiện
                if rightmost_box:
                    last_pattern = rightmost_box[0]
                    if last_pattern in ['Bearish-Engulfing', 'Three-Inside-Down']:
                        st.write("Bitcoin có xu hướng giảm")
                    elif last_pattern in ['Bullish-Engulfing', 'Three-Inside-Up']:
                        st.write("Bitcoin có xu hướng tăng")
                    else:
                        st.write("Không xác định được xu hướng Bitcoin")

if __name__ == '__main__':
    app()
