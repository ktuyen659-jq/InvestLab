# InvestLab — Python + Streamlit

## Chạy trên máy tính
Yêu cầu Python 3.10 trở lên.

1. Giải nén thư mục dự án.
2. Mở Terminal tại thư mục `investlab-streamlit`.
3. Cài thư viện:

```bash
pip install -r requirements.txt
```

4. Chạy ứng dụng:

```bash
streamlit run App.py
```

Mở URL local mà Streamlit in ra, thường là http://localhost:8501.

## Nếu dùng Streamlit Community Cloud
Đưa `App.py` và `requirements.txt` lên GitHub, sau đó vào https://share.streamlit.io/, chọn repository và file chính `App.py`, rồi Deploy.

## Các màn hình
- Tổng quan dashboard và biểu đồ
- Máy tính E(X), Var(X), độ lệch chuẩn
- Phân tích xác suất kịch bản âm
- Chỉnh sửa danh mục đầu tư
- Kiến thức thống kê
- Cài đặt vốn giả định

## Lưu ý
Dữ liệu là giả lập. Ước tính rủi ro danh mục đang giả định hiệp phương sai giữa các tài sản bằng 0; không dùng làm cơ sở giao dịch thực tế.
