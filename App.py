import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# CẤU HÌNH & CSS (Dựa trên Ảnh 6 & 7)
# ==========================================
st.set_page_config(page_title="InvestLab", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Manrope', sans-serif; background-color: #F8F9FA; }
    .stSidebar { background-color: #EBF4F6; } /* Màu xanh nhạt từ Ảnh 6 */
    .metric-value { font-size: 24px; font-weight: 700; color: #1E1E2D; }
    .metric-label { font-size: 14px; color: #6B7280; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MODULE 1: TỔNG QUAN (Dựa trên Ảnh 1)
# ==========================================
def render_overview():
    st.title("Tổng quan")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Total Assets")
        st.markdown('<div class="metric-value">$126,450.00</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label" style="color: green;">▲ 15.5% this year</div>', unsafe_allow_html=True)
        st.progress(0.42, text="Stocks 42% ($53,109.00)")
        st.progress(0.28, text="Crypto 28% ($35,406.00)")
        st.button("Adjust Portfolio")
        
    with col2:
        # Performance Chart
        dates = pd.date_range(start='2026-05-17', periods=30)
        df = pd.DataFrame({'Date': dates, 'Your Portfolio': np.random.normal(120000, 2000, 30).cumsum(), 'S&P 500 Index': np.random.normal(100000, 1500, 30).cumsum()})
        fig = px.line(df, x='Date', y=['Your Portfolio', 'S&P 500 Index'], title="Performance Chart")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Holdings Detail")
    data = {'Asset': ['AAPL', 'BTC', 'NVDA', 'USDC'], 'QTY': [52, 0.55, 10, '-'], 'Current Price': ['$172.30', '$69,200.00', '$950.10', '$3,200.00'], 'Gain/Loss': ['+$1,251.60', '+$6,050.00', '+$1,051.00', '+$3,200.00']}
    st.dataframe(pd.DataFrame(data), use_container_width=True)

# ==========================================
# MODULE 2: LỢI NHUẬN KỲ VỌNG (Dựa trên Ảnh 2)
# ==========================================
def render_expected_return():
    st.title("Lợi nhuận kỳ vọng")
    st.subheader("Year-by-Year Projection")
    
    data = {
        'YEAR': [2027, 2028, 2029, 2030, 2031],
        'PORTFOLIO VALUE': ['$219,750', '$240,957', '$263,727', '$288,177', '$314,430'],
        'CONTRIBUTIONS': ['$205,000', '$210,000', '$215,000', '$220,000', '$225,000'],
        'PROFIT': ['$14,750', '$30,957', '$48,727', '$68,177', '$89,430']
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Contribution Breakdown")
        st.progress(0.21, text="Total Contributions: $325,000")
        st.progress(0.78, text="Total Profit: $1.19M")
        
    with col2:
        st.subheader("Portfolio Stress Test")
        c1, c2 = st.columns(2)
        c1.error("📉 2008 Financial Crisis: -44.8%")
        c2.warning("🦠 COVID-19 Crash (2020): -26.9%")

# ==========================================
# MODULE 3: PHÂN TÍCH RỦI RO (Dựa trên Ảnh 3)
# ==========================================
def render_risk_analysis():
    st.title("Phân tích rủi ro")
    st.subheader("Monte Carlo VaR Calculator")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Simulated P&L Distribution
        x = np.random.normal(0, 5, 1000)
        fig = px.histogram(x, nbins=30, title="Simulated P&L Distribution")
        fig.add_vline(x=-8.2, line_color="orange", annotation_text="VaR (95%)")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Correlation Matrix")
        z = [[1, 0.3, 0.1], [0.3, 1, 0.4], [0.1, 0.4, 1]]
        fig2 = px.imshow(z, x=['A', 'B', 'C'], y=['A', 'B', 'C'], color_continuous_scale='RdBu_r')
        st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# MODULE 4: DANH MỤC ĐẦU TƯ (Dựa trên Ảnh 4)
# ==========================================
def render_portfolio_optimization():
    st.title("Danh mục đầu tư (Tối ưu hóa)")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("**Portfolio Inputs**")
        w1 = st.slider("US Large Cap", 0, 100, 30)
        w2 = st.slider("US Small Cap", 0, 100, 15)
        w3 = st.slider("International", 0, 100, 15)
        st.metric("Total Weight", f"{w1+w2+w3}%")
        st.button("Generate Frontier")
        
    with col2:
        st.write("**Risk-Return Space (Efficient Frontier)**")
        returns = np.random.normal(10, 2, 500)
        risks = np.random.normal(15, 3, 500)
        fig = px.scatter(x=risks, y=returns, color=returns, labels={'x': 'Portfolio Risk (σ)', 'y': 'Expected Return'})
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULE 5: SO SÁNH PHƯƠNG ÁN (Dựa trên Ảnh 5)
# ==========================================
def render_comparison():
    st.title("So sánh phương án")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Sharpe Ratio", "1.18", "+0.3 vs. benchmark")
    c2.metric("Return", "14.2%", "+1.2% vs. benchmark")
    c3.metric("Volatility", "12.8%", "-2.5% vs. benchmark")
    
    df = pd.DataFrame({
        'Date': pd.date_range('2020-01-01', periods=20, freq='M'),
        'Optimized Portfolio': np.random.normal(1, 0.05, 20).cumsum(),
        'Benchmark Portfolio': np.random.normal(1, 0.04, 20).cumsum()
    })
    fig = px.line(df, x='Date', y=['Optimized Portfolio', 'Benchmark Portfolio'], title="Cumulative Return")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MAIN APP & SIDEBAR (Dựa trên Ảnh 6)
# ==========================================
def main():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2933/2933116.png", width=40) # Logo giả lập
        st.markdown("### InvestLab")
        st.caption("INVESTMENT ANALYTICS")
        st.write("**Xin chào, jin**")
        st.write("---")
        
        # Menu giống hệt Ảnh 6
        menu = ["Tổng quan", "Lợi nhuận kỳ vọng", "Phân tích rủi ro", "Danh mục đầu tư", "So sánh phương án", "Trợ lý giọng nói", "Cài đặt"]
        choice = st.radio("Điều hướng", menu)
        
        st.write("---")
        st.caption("Dữ liệu mẫu chỉ phục vụ học tập, không phải khuyến nghị đầu tư.")
        st.button("Đăng xuất")

    # Routing logic
    if choice == "Tổng quan":
        render_overview()
    elif choice == "Lợi nhuận kỳ vọng":
        render_expected_return()
    elif choice == "Phân tích rủi ro":
        render_risk_analysis()
    elif choice == "Danh mục đầu tư":
        render_portfolio_optimization()
    elif choice == "So sánh phương án":
        render_comparison()
    elif choice == "Trợ lý giọng nói":
        st.title("Trợ lý giọng nói")
        st.info("Tính năng Voice AI đang được tích hợp...")
    elif choice == "Cài đặt":
        st.title("Cài đặt")
        st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])

if __name__ == "__main__":
    main()
