import math
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="InvestLab", page_icon="📈", layout="wide")
st.markdown("""
<style>
.stApp{background:#f4f7fb}
[data-testid="stSidebar"]{background:#101d33}
[data-testid="stSidebar"] *{color:#e8eef8}
.hero{font-size:2rem;font-weight:800;color:#17263e}
.eyebrow{font-size:.72rem;letter-spacing:.14em;color:#7e8ba0;font-weight:700}
div[data-testid="stMetric"]{background:white;border:1px solid #e7edf4;padding:1rem;border-radius:13px}
</style>
""", unsafe_allow_html=True)

SCENARIOS = pd.DataFrame({"Kịch bản":["Tích cực","Cơ sở","Tiêu cực"],"Xác suất (%)":[25.,50.,25.],"Tỷ suất sinh lời (%)":[30.,10.,-20.]})
ASSETS = pd.DataFrame({"Mã tài sản":["FPT","VNM","VCB","Tiền mặt"],"Tỷ trọng (%)":[35.,25.,25.,15.],"Lợi nhuận kỳ vọng (%)":[16.5,10.2,13.4,4.],"Độ lệch chuẩn riêng (%)":[23.,16.,19.,1.]})
if "scenarios" not in st.session_state: st.session_state.scenarios=SCENARIOS.copy()
if "assets" not in st.session_state: st.session_state.assets=ASSETS.copy()
if "capital" not in st.session_state: st.session_state.capital=100.

def pct(x, n=2):
    return f"{x:,.{n}f}%".replace(",", "X").replace(".", ",").replace("X", ".")
def scenario_stats(df):
    if df.empty: return 0.,0.,0.
    p=df["Xác suất (%)"].astype(float).to_numpy()/100
    r=df["Tỷ suất sinh lời (%)"].astype(float).to_numpy()
    e=float((p*r).sum()); v=float((p*(r-e)**2).sum())
    return e,v,math.sqrt(max(v,0))
def portfolio_stats(df):
    if df.empty: return 0.,0.,0.
    w=df["Tỷ trọng (%)"].astype(float).to_numpy()/100
    r=df["Lợi nhuận kỳ vọng (%)"].astype(float).to_numpy()
    s=df["Độ lệch chuẩn riêng (%)"].astype(float).to_numpy()
    return float((w*r).sum()),float(math.sqrt(((w*s)**2).sum())),float(w.sum()*100)

with st.sidebar:
    st.markdown("## 📈 InvestLab")
    st.caption("INVESTMENT ANALYTICS")
    page=st.radio("Điều hướng",["Tổng quan","Lợi nhuận kỳ vọng","Phân tích rủi ro","Danh mục đầu tư","Kiến thức","Cài đặt"])
    st.divider()
    st.info("Dữ liệu mẫu chỉ phục vụ học tập, không phải khuyến nghị đầu tư.")

sc=st.session_state.scenarios.copy()
assets=st.session_state.assets.copy()
e,v,sigma=scenario_stats(sc)
ep,risk,total=portfolio_stats(assets)
capital=float(st.session_state.capital)

if page=="Tổng quan":
    st.markdown('<div class="eyebrow">INVESTMENT WORKSPACE</div><div class="hero">Tổng quan đầu tư ✳</div>',unsafe_allow_html=True)
    st.write("Theo dõi hiệu suất giả lập và hiểu rõ rủi ro trong danh mục.")
    st.info("Không gian mô phỏng — số liệu minh họa, không phải giá thị trường thực tế.")
    a,b,c,d=st.columns(4)
    a.metric("Vốn đầu tư giả định",f"{capital:,.1f} triệu VND")
    b.metric("Lợi nhuận kỳ vọng danh mục",pct(ep))
    c.metric("Rủi ro danh mục ước tính",pct(risk))
    d.metric("Số tài sản",len(assets),f"Tổng tỷ trọng {total:.0f}%")
    left,right=st.columns([1.6,1])
    with left:
        st.subheader("Hiệu suất danh mục")
        perf=pd.DataFrame({"Tháng":["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12"],"Danh mục":[2,-1,4,3,8,6,11,9,14,12,16,18],"Chỉ số tham chiếu":[1,0,2,4,5,6,8,7,10,11,13,14]})
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=perf["Tháng"],y=perf["Danh mục"],name="Danh mục",mode="lines",line=dict(color="#16a36a",width=3),fill="tozeroy",fillcolor="rgba(22,163,106,.09)"))
        fig.add_trace(go.Scatter(x=perf["Tháng"],y=perf["Chỉ số tham chiếu"],name="Chỉ số tham chiếu",mode="lines",line=dict(color="#4778e8",width=2)))
        fig.update_layout(height=340,margin=dict(l=10,r=10,t=20,b=10),paper_bgcolor="white",plot_bgcolor="white",yaxis_title="Tỷ suất (%)")
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Phân bổ tài sản")
        fig=px.pie(assets,names="Mã tài sản",values="Tỷ trọng (%)",hole=.62,color_discrete_sequence=["#4778e8","#16a36a","#e6a23c","#8b75c9"])
        fig.update_layout(height=340,margin=dict(l=0,r=0,t=20,b=10),paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    st.subheader("Tài sản trong danh mục")
    table=assets.copy()
    table["Giá trị giả định"]=table["Tỷ trọng (%)"].apply(lambda w:f"{capital*w/100:,.1f} triệu VND")
    st.dataframe(table,use_container_width=True,hide_index=True)
    if abs(total-100)>1e-6: st.warning(f"Tổng tỷ trọng hiện là {total:.1f}%, cần điều chỉnh về 100%.")

elif page=="Lợi nhuận kỳ vọng":
    st.markdown('<div class="eyebrow">STATISTICAL CALCULATOR</div>',unsafe_allow_html=True)
    st.title("Máy tính lợi nhuận kỳ vọng")
    st.write("Chỉnh sửa xác suất và tỷ suất sinh lời; các chỉ số sẽ tự cập nhật.")
    edited=st.data_editor(st.session_state.scenarios,use_container_width=True,hide_index=True,num_rows="dynamic",key="scenario_editor",column_config={
        "Kịch bản":st.column_config.TextColumn(required=True),
        "Xác suất (%)":st.column_config.NumberColumn(min_value=0,max_value=100,step=5,format="%.1f"),
        "Tỷ suất sinh lời (%)":st.column_config.NumberColumn(step=1,format="%.2f")})
    st.session_state.scenarios=edited
    e,v,sigma=scenario_stats(edited)
    totalp=float(edited["Xác suất (%)"].sum()) if not edited.empty else 0
    if abs(totalp-100)>1e-6: st.warning(f"Tổng xác suất hiện là {totalp:.1f}%. Hãy điều chỉnh về 100%.")
    a,b,c=st.columns(3); a.metric("Lợi nhuận kỳ vọng E(X)",pct(e)); b.metric("Phương sai Var(X)",f"{v:.3f} %²"); c.metric("Độ lệch chuẩn σ",pct(sigma))
    st.subheader("Đóng góp vào lợi nhuận kỳ vọng")
    chart=edited.copy()
    if not chart.empty:
        chart["Đóng góp (%)"]=chart["Xác suất (%)"]/100*chart["Tỷ suất sinh lời (%)"]
        fig=px.bar(chart,x="Kịch bản",y="Đóng góp (%)",color="Kịch bản",color_discrete_sequence=["#16a36a","#4778e8","#e45757"])
        fig.update_layout(showlegend=False,height=320,margin=dict(l=10,r=10,t=20,b=10),paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with st.expander("Xem công thức"):
        st.latex(r"E(X)=\sum_{i=1}^{n}p_i x_i")
        st.latex(r"\mathrm{Var}(X)=\sum_{i=1}^{n}p_i(x_i-E(X))^2")
        st.latex(r"\sigma=\sqrt{\mathrm{Var}(X)}")
        st.write("pᵢ là xác suất dạng thập phân; xᵢ là tỷ suất sinh lời của kịch bản.")

elif page=="Phân tích rủi ro":
    st.markdown('<div class="eyebrow">RISK ANALYTICS</div>',unsafe_allow_html=True)
    st.title("Phân tích rủi ro")
    neg=sc[sc["Tỷ suất sinh lời (%)"]<0]
    prob=float(neg["Xác suất (%)"].sum()) if not neg.empty else 0.
    a,b,c,d=st.columns(4)
    a.metric("Độ lệch chuẩn",pct(sigma)); b.metric("Phương sai",f"{v:.3f} %²"); c.metric("Số kịch bản âm",len(neg)); d.metric("Xác suất kịch bản âm",pct(prob,1))
    left,right=st.columns(2)
    with left:
        st.subheader("Xác suất theo kịch bản")
        fig=px.bar(sc,x="Kịch bản",y="Xác suất (%)",color="Kịch bản",color_discrete_sequence=["#16a36a","#4778e8","#e45757"])
        fig.update_layout(showlegend=False,height=320,paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Diễn giải nhanh")
        st.success(f"Lợi nhuận kỳ vọng hiện tại là {pct(e)}.")
        st.info(f"Độ lệch chuẩn là {pct(sigma)}; đây không phải xác suất thua lỗ.")
        st.warning(f"Xác suất các kịch bản có lợi nhuận âm: {pct(prob,1)}.")
    st.warning("Các kịch bản rời rạc không đủ để kết luận lợi nhuận tuân theo phân phối chuẩn. Độ lệch chuẩn không phản ánh toàn bộ rủi ro đuôi hoặc thanh khoản.")

elif page=="Danh mục đầu tư":
    st.markdown('<div class="eyebrow">PORTFOLIO BUILDER</div>',unsafe_allow_html=True)
    st.title("Xây dựng danh mục")
    st.write("Điều chỉnh tỷ trọng và giả định lợi nhuận/rủi ro của từng tài sản.")
    edited=st.data_editor(st.session_state.assets,use_container_width=True,hide_index=True,num_rows="dynamic",key="asset_editor",column_config={
        "Mã tài sản":st.column_config.TextColumn(required=True),
        "Tỷ trọng (%)":st.column_config.NumberColumn(min_value=0,max_value=100,step=5,format="%.1f"),
        "Lợi nhuận kỳ vọng (%)":st.column_config.NumberColumn(step=.5,format="%.2f"),
        "Độ lệch chuẩn riêng (%)":st.column_config.NumberColumn(min_value=0,step=.5,format="%.2f")})
    st.session_state.assets=edited
    ep,risk,total=portfolio_stats(edited)
    a,b,c=st.columns(3); a.metric("Lợi nhuận kỳ vọng danh mục",pct(ep)); b.metric("Rủi ro xấp xỉ",pct(risk)); c.metric("Tổng tỷ trọng",pct(total,1),delta="Hợp lệ" if abs(total-100)<1e-6 else "Cần bằng 100%")
    left,right=st.columns(2)
    with left:
        st.subheader("Cơ cấu phân bổ")
        if not edited.empty:
            fig=px.pie(edited,names="Mã tài sản",values="Tỷ trọng (%)",hole=.6,color_discrete_sequence=["#4778e8","#16a36a","#e6a23c","#8b75c9","#e45757"])
            fig.update_layout(height=340,paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Lợi nhuận và rủi ro riêng")
        if not edited.empty:
            fig=px.scatter(edited,x="Độ lệch chuẩn riêng (%)",y="Lợi nhuận kỳ vọng (%)",text="Mã tài sản",size="Tỷ trọng (%)",color="Mã tài sản")
            fig.update_traces(textposition="top center"); fig.update_layout(height=340,paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    st.info("Ước tính rủi ro đang giả định hiệp phương sai giữa các tài sản bằng 0. Muốn tính sát thực tế hơn, cần ma trận hiệp phương sai hoặc dữ liệu lợi nhuận lịch sử.")

elif page=="Kiến thức":
    st.markdown('<div class="eyebrow">LEARNING CENTER</div>',unsafe_allow_html=True)
    st.title("Kiến thức thống kê đầu tư")
    with st.container(border=True):
        st.subheader("1. Lợi nhuận kỳ vọng"); st.latex(r"E(X)=\sum_{i=1}^{n}p_i x_i")
        st.write("Trung bình có trọng số của các kết quả có thể xảy ra theo xác suất.")
        st.caption("Ví dụ: 25% × 30% + 50% × 10% + 25% × (−20%) = 7,5%.")
    with st.container(border=True):
        st.subheader("2. Phương sai"); st.latex(r"\mathrm{Var}(X)=E[(X-\mu)^2]")
        st.write("Đo mức phân tán quanh lợi nhuận kỳ vọng. Phương sai có đơn vị bình phương.")
    with st.container(border=True):
        st.subheader("3. Độ lệch chuẩn"); st.latex(r"\sigma=\sqrt{\mathrm{Var}(X)}")
        st.write("Căn bậc hai của phương sai và có cùng đơn vị với tỷ suất sinh lời.")
    with st.container(border=True):
        st.subheader("4. Phân phối chuẩn"); st.latex(r"X\sim\mathcal{N}(\mu,\sigma^2)")
        st.write("Mô hình xác suất liên tục dạng hình chuông. Không nên mặc định lợi nhuận tài chính luôn tuân theo phân phối chuẩn.")

elif page=="Cài đặt":
    st.markdown('<div class="eyebrow">PREFERENCES</div>',unsafe_allow_html=True)
    st.title("Cài đặt")
    with st.form("settings"):
        value=st.number_input("Vốn đầu tư giả định (triệu VND)",min_value=0.,value=float(st.session_state.capital),step=10.)
        if st.form_submit_button("Lưu cài đặt",type="primary"):
            st.session_state.capital=value; st.success("Đã cập nhật vốn giả định.")
    st.info("Bản demo chưa kết nối cơ sở dữ liệu; dữ liệu chỉ được giữ trong phiên hiện tại.")

st.divider()
st.caption("InvestLab · Bản demo học tập · Dữ liệu giả lập, không phải khuyến nghị đầu tư.")
