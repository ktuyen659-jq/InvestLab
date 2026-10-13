# InvestLab - Nền tảng Tối ưu hóa Danh mục Đầu tư 📈

InvestLab là một ứng dụng web tương tác được xây dựng bằng Python và Streamlit, giúp nhà đầu tư cá nhân mô phỏng, đánh giá rủi ro và tối ưu hóa danh mục đầu tư dựa trên các công cụ thống kê tài chính (Lợi nhuận kỳ vọng, Phương sai, Phân phối chuẩn, và Đường biên hiệu quả Markowitz).

## 🚀 Tính năng nổi bật

* **Tổng quan (Dashboard):** Theo dõi tổng tài sản, tỷ suất sinh lời, điểm đa dạng hóa và tỷ lệ Sharpe theo thời gian thực.
* **Lợi nhuận kỳ vọng:** Bảng dự phóng chi tiết lợi nhuận từng năm và tác động của lạm phát.
* **Phân tích rủi ro:** Đánh giá rủi ro danh mục bằng mô phỏng Monte Carlo, chỉ số VaR (Value at Risk) và kiểm tra sức chịu đựng (Stress Test) qua các chu kỳ khủng hoảng lịch sử.
* **Danh mục đầu tư (Tối ưu hóa):** Cho phép điều chỉnh tỷ trọng tài sản trực quan bằng thanh trượt. Biểu đồ Đường biên hiệu quả (Efficient Frontier) cập nhật tức thời để tìm ra điểm cân bằng Risk-Return tối ưu.
* **Trợ lý giọng nói AI:** Tích hợp không gian hỏi đáp nhanh về tình trạng danh mục.
* **Chế độ Dark/Light:** Giao diện hiện đại sử dụng font chữ Manrope.

## 🛠 Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.9+
* **Framework giao diện:** Streamlit
* **Xử lý dữ liệu:** Pandas, NumPy
* **Trực quan hóa biểu đồ:** Plotly (Plotly Express, Plotly Graph Objects)

## ⚙️ Hướng dẫn cài đặt và chạy dự án

**Bước 1: Clone dự án về máy**
```bash
git clone [https://github.com/your-username/investlab.git](https://github.com/your-username/investlab.git)
cd investlab