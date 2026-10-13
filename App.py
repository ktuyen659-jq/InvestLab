import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Cấu hình trang
st.set_page_config(page_title="InvestLab", layout="wide", initial_sidebar_state="expanded")

# Tùy chỉnh CSS để sử dụng font Manrope và màu nền sáng
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Manrope', sans-serif;
        background-color: #F8F9FA; /* Màu nền sáng từ ảnh cuối */
    }
    
    .stSidebar {
        background-color: #FFFFFF;
    }
    
    h1, h2, h3 {
        color: #1E1E2D;
    }
    
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Trạng thái đăng nhập (giả lập)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Hàm vẽ biểu đồ (có thể chuyển động nhờ Plotly)
def plot_portfolio_performance():
    dates = pd.date_range(start='2026-05-01', periods=60)
    portfolio_values = np.random.normal(1000, 20, 60).cumsum() + 100000
    sp500_values = np.random.normal(500, 15, 60).cumsum() + 90000
    
    df = pd.DataFrame({'Date': dates, 'Your Portfolio': portfolio_values, 'S&P 500 Index': sp500_values})
    
    fig = px.line(df, x='Date', y=['Your Portfolio', 'S&P 500 Index'], 
                  title="Performance Chart",
                  color_discrete_sequence=['#6366F1', '#F59E0B'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    return fig

# Hàm tính toán Efficient Frontier
def calculate_efficient_frontier():
    np.random.seed(42)
    returns = np.random.randn(4)
    volatility = np.random.rand(4)
    weights = np.random.random(4)
    weights /= np.sum(weights)
    
    port_returns = []
    port_volatility = []
    
    for _ in range(1000):
        w = np.random.random(4)
        w /= np.sum(w)
        port_returns.append(np.sum(returns * w))
        port_volatility.append(np.sqrt(np.dot(w.T, np.dot(np.diag(volatility), w))))
        
    fig = px.scatter(x=port_volatility, y=port_returns, 
                     labels={'x': 'Portfolio Risk (σ)', 'y': 'Expected Return'},
                     title="Efficient Frontier",
                     color=port_returns, color_continuous_scale='Viridis')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    return fig

# Giao diện Đăng nhập
if not st.session_state['logged_in']:
    st.title("Đăng nhập vào InvestLab")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập"):
        if username and password: # Giả lập đăng nhập thành công
            st.session_state['logged_in'] = True
            st.rerun()

# Giao diện chính sau khi đăng nhập
else:
    # Thanh bên (Sidebar)
    with st.sidebar:
        st.title("📈 InvestLab")
        st.write("INVESTMENT ANALYTICS")
        
        # Profile người dùng
        st.write("---")
        st.write("**Xin chào, Jin**")
        language = st.selectbox("Ngôn ngữ", ["Tiếng Việt", "English"])
        st.write("---")
        
        # Điều hướng
        menu_options = [
            "Tổng quan", 
            "Lợi nhuận kỳ vọng", 
            "Phân tích rủi ro", 
            "Danh mục đầu tư", 
            "So sánh phương án",
            "Trợ lý giọng nói", 
            "Cài đặt"
        ]
        choice = st.radio("Điều hướng", menu_options)
        
        st.write("---")
        st.caption("Dữ liệu mẫu chỉ phục vụ học tập, không phải khuyến nghị đầu tư.")
        if st.button("Đăng xuất"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Nội dung chính (Main Content)
    if choice == "Tổng quan":
        st.header("Dashboard Tổng Quan")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Assets", "$126,450.00", "+15.5%")
        col2.metric("Portfolio Return", "18.64%", "+2.10%")
        col3.metric("Diversification Score", "35/100")
        col4.metric("Sharpe Ratio", "1.18", "+0.3")
        
        st.plotly_chart(plot_portfolio_performance(), use_container_width=True)
        
        st.subheader("Holdings Detail")
        st.dataframe(pd.DataFrame({
            'Asset': ['AAPL', 'BTC', 'NVDA', 'USDC'],
            'QTY': [52, 0.55, 10, '-'],
            'Avg. Buy Price': ['$148.20', '$58,200.00', '$845.00', '-'],
            'Current Price': ['$172.30', '$69,200.00', '$950.10', '$3,200.00'],
            'Gain/Loss': ['+$1,251.60', '+$6,050.00', '+$1,051.00', '+$3,200.00']
        }), use_container_width=True)

    elif choice == "Lợi nhuận kỳ vọng":
        st.header("Dự phóng Lợi nhuận Kỳ vọng")
        st.write("Dự phóng tài sản theo từng năm (Year-by-Year Projection)")
        st.dataframe(pd.DataFrame({
            'YEAR': [2027, 2028, 2029, 2030, 2031],
            'PORTFOLIO VALUE': ['$219,750', '$240,957', '$263,727', '$288,177', '$314,430'],
            'CONTRIBUTIONS': ['$205,000', '$210,000', '$215,000', '$220,000', '$225,000'],
            'PROFIT': ['$14,750', '$30,957', '$48,727', '$68,177', '$89,430'],
            'ASSUMED ANNUAL RETURN': ['7.38%', '7.38%', '7.38%', '7.38%', '7.38%']
        }), use_container_width=True)

    elif choice == "Phân tích rủi ro":
        st.header("Phân tích Rủi ro & VaR")
        st.write("Monte Carlo VaR Calculator")
        
        # Mô phỏng biểu đồ phân phối chuẩn
        x = np.linspace(-15, 15, 100)
        y = (1 / (np.sqrt(2 * np.pi * 3**2))) * np.exp(-0.5 * ((x - 2) / 3)**2)
        fig_var = go.Figure()
        fig_var.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Simulated P&L'))
        fig_var.add_vline(x=-5, line_dash="dash", line_color="orange", annotation_text="VaR (95%)")
        st.plotly_chart(fig_var, use_container_width=True)
        
        st.subheader("Portfolio Stress Test")
        cols = st.columns(3)
        cols[0].error("2008 Financial Crisis: -44.8%")
        cols[1].warning("COVID-19 Crash (2020): -26.9%")
        cols[2].info("2022 Inflation Surge: -16.5%")

    elif choice == "Danh mục đầu tư":
        st.header("Tối ưu hóa Danh mục")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Điều chỉnh Tỷ trọng")
            us_large_cap = st.slider("US Large Cap", 0, 100, 30)
            us_small_cap = st.slider("US Small Cap", 0, 100, 15)
            intl = st.slider("International", 0, 100, 15)
            bonds = st.slider("Bonds", 0, 100, 30)
            reits = st.slider("REITs", 0, 100, 10)
            
            st.metric("Total Weight", f"{us_large_cap + us_small_cap + intl + bonds + reits}%")
            
        with col2:
            st.plotly_chart(calculate_efficient_frontier(), use_container_width=True)

    elif choice == "So sánh phương án":
        st.header("So sánh Phương án Đầu tư")
        st.write("So sánh danh mục tối ưu với Benchmark.")
        
        fig = plot_portfolio_performance()
        fig.data[0].name = 'Optimized Portfolio'
        fig.data[1].name = 'Benchmark Portfolio'
        st.plotly_chart(fig, use_container_width=True)

    elif choice == "Trợ lý giọng nói":
        st.header("Trợ lý Giọng nói InvestLab AI")
        st.info("🎤 Tính năng nhận diện giọng nói đang được phát triển. Vui lòng sử dụng hộp thoại bên dưới.")
        user_input = st.text_input("Bạn muốn hỏi gì về danh mục của mình?")
        if user_input:
            st.write(f"**AI InvestLab:** Tôi đang phân tích câu hỏi '{user_input}' của bạn...")

    elif choice == "Cài đặt":
        st.header("Cài đặt Hệ thống")
        st.subheader("Các thông số giả lập")
        risk_free_rate = st.number_input("Risk-Free Rate (%)", value=4.5)
        mc_simulations = st.number_input("Monte Carlo Simulations", value=5000)
        time_horizon = st.number_input("Time Horizon (years)", value=10)
        
        st.success("Đã lưu cấu hình!")