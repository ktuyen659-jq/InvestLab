# InvestLab — Streamlit

## Chạy trên máy tính
1. Cài Python 3.10 trở lên.
2. Mở Terminal/CMD trong thư mục dự án.
3. Cài thư viện: `pip install -r requirements.txt`
4. Chạy ứng dụng: `streamlit run App.py`
5. Mở địa chỉ localhost được in trong terminal (thường là http://localhost:8501).

## Tính năng
- Đăng nhập và tạo tài khoản mẫu (lưu hash mật khẩu cục bộ trong `investlab_users.json`).
- Dashboard, lợi nhuận kỳ vọng, phân tích rủi ro và danh mục đầu tư.
- Trợ lý hỏi đáp theo chủ đề đầu tư, nhập câu hỏi bằng chữ, nhận diện giọng nói trên trình duyệt hỗ trợ và đọc văn bản bằng giọng nói.
- Giao diện xanh dịu mắt, thẻ bo tròn và chuyển động nhẹ.
- Đã bỏ mục Kiến thức khỏi điều hướng.

## Lưu ý quan trọng
Đăng nhập chỉ phục vụ bản demo chạy cục bộ. Không triển khai công khai hoặc dùng mật khẩu thật khi chưa thay bằng hệ thống xác thực an toàn (ví dụ OAuth hoặc backend có quản lý phiên, chống brute-force và lưu trữ bảo mật). Tính năng giọng nói dùng API của trình duyệt, thường hoạt động tốt hơn trên Chrome và có thể yêu cầu HTTPS/quyền microphone. Trợ lý hiện dùng câu trả lời mẫu theo từ khóa, chưa kết nối mô hình AI hoặc dịch vụ nhận diện giọng nói bên ngoài. Mọi dữ liệu đầu tư là giả lập, không phải khuyến nghị đầu tư.
