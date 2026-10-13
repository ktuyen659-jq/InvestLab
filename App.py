import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import json
from pathlib import Path

st.set_page_config(page_title="InvestLab", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# ---- Calm blue visual system + subtle motion ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --ink:#16324f; --blue:#3977a8; --mint:#d9f0ec; --pale:#eef7fb; }
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: linear-gradient(135deg,#eaf5fb 0%,#f4f9fc 52%,#e1f1f3 100%); color:var(--ink); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#d7edf5,#e8f4f5 75%,#e3f2ec); border-right:1px solid #c7e1e9; }
h1,h2,h3 { color:#163b5b !important; letter-spacing:-.035em; }
[data-testid="stMetric"] { background:rgba(255,255,255,.78); padding:18px 20px; border:1px solid #d5e8ef; border-radius:18px; box-shadow:0 8px 28px #244e6510; animation: rise .55s ease both; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius:20px; }
.stButton>button, .stFormSubmitButton>button { border-radius:12px; border:0; background:linear-gradient(120deg,#3977a8,#4b9caa); color:white; font-weight:650; transition:transform .2s, box-shadow .2s; box-shadow:0 5px 16px #3977a822; }
.stButton>button:hover, .stFormSubmitButton>button:hover { transform:translateY(-2px); box-shadow:0 9px 22px #3977a833; color:white; }
.il-card { background:rgba(255,255,255,.72); border:1px solid #d5e8ef; border-radius:20px; padding:22px; box-shadow:0 10px 30px #214b6010; animation: rise .55s ease both; }
.hero { border-radius:24px; padding:28px; color:#143b55; background:radial-gradient(circle at 85% 20%,#b8e5e0 0,transparent 28%),linear-gradient(120deg,#d8edf8,#e9f7f4); border:1px solid #c9e4eb; position:relative; overflow:hidden; }
.hero:after { content:""; position:absolute; width:180px;height:180px;border-radius:50%;right:-45px;bottom:-100px;background:#83c9cb55; animation: floaty 7s ease-in-out infinite; }
.pill { display:inline-block;padding:5px 10px;border-radius:999px;background:#d8eee9;color:#226b69;font-size:12px;font-weight:700; }
.small-muted { color:#678194;font-size:13px; }
@keyframes rise { from {opacity:0;transform:translateY(9px)} to {opacity:1;transform:translateY(0)} }
@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-16px)} }
@media (prefers-reduced-motion: reduce) { * {animation:none!important;transition:none!important;} }
</style>
""", unsafe_allow_html=True)

USERS_FILE = Path("investlab_users.json")
def hash_pw(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
def load_users():
    if USERS_FILE.exists():
        try: return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except Exception: return {}
    return {}
def save_users(users):
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "Tổng quan"

def auth_screen():
    left, right = st.columns([1.05, 1], gap="large")
    with left:
        st.markdown("""
        <div class="hero" style="min-height:390px;margin-top:20px">
          <span class="pill">INVESTMENT ANALYTICS</span>
          <h1 style="font-size:42px;margin-top:24px">Đầu tư sáng suốt<br/>bắt đầu từ dữ liệu.</h1>
          <p style="font-size:17px;max-width:450px">Theo dõi lợi nhuận kỳ vọng, hiểu rủi ro và trò chuyện với trợ lý InvestLab — trong một không gian dịu mắt.</p>
          <div style="font-size:46px;margin-top:30px;letter-spacing:10px">📈 💧 🌱</div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("## 🔐 Chào mừng đến InvestLab")
        st.caption("Đăng nhập hoặc tạo tài khoản dùng trên ứng dụng này.")
        tab1, tab2 = st.tabs(["Đăng nhập", "Tạo tài khoản"])
        users = load_users()
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Tên đăng nhập", key="login_user")
                password = st.text_input("Mật khẩu", type="password", key="login_pw")
                submit = st.form_submit_button("Đăng nhập", use_container_width=True)
            if submit:
                record = users.get(username.strip())
                if record and record == hash_pw(password):
                    st.session_state.user = username.strip()
                    st.rerun()
                else: st.error("Tên đăng nhập hoặc mật khẩu chưa đúng.")
        with tab2:
            with st.form("signup_form"):
                new_user = st.text_input("Tên đăng nhập", key="signup_user")
                new_pw = st.text_input("Mật khẩu (tối thiểu 8 ký tự)", type="password", key="signup_pw")
                confirm = st.text_input("Nhập lại mật khẩu", type="password", key="signup_confirm")
                create = st.form_submit_button("Tạo tài khoản", use_container_width=True)
            if create:
                new_user = new_user.strip()
                if len(new_user) < 3: st.error("Tên đăng nhập cần ít nhất 3 ký tự.")
                elif len(new_pw) < 8: st.error("Mật khẩu cần ít nhất 8 ký tự.")
                elif new_pw != confirm: st.error("Hai mật khẩu không trùng khớp.")
                elif new_user in users: st.error("Tên đăng nhập đã tồn tại.")
                else:
                    users[new_user] = hash_pw(new_pw); save_users(users)
                    st.success("Tạo tài khoản thành công. Hãy đăng nhập.")
        st.info("Bản mẫu lưu tài khoản trong tệp cục bộ. Không dùng mật khẩu thật hoặc triển khai công khai nếu chưa tích hợp hệ thống xác thực an toàn.")
    st.stop()

if not st.session_state.user:
    auth_screen()

# sidebar navigation
with st.sidebar:
    st.markdown("## 📈 InvestLab")
    st.caption("INVESTMENT ANALYTICS")
    st.markdown(f"Xin chào, **{st.session_state.user}**")
    pages = ["Tổng quan", "Lợi nhuận kỳ vọng", "Phân tích rủi ro", "Danh mục đầu tư", "Trợ lý giọng nói", "Cài đặt"]
    page = st.radio("Điều hướng", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    st.session_state.page = page
    st.divider()
    st.caption("Dữ liệu mẫu chỉ phục vụ học tập, không phải khuyến nghị đầu tư.")
    if st.button("Đăng xuất", use_container_width=True):
        st.session_state.user = None
        st.rerun()

page = st.session_state.page
st.markdown(f"<div class='small-muted'>INVESTLAB / {page.upper()}</div>", unsafe_allow_html=True)

if page == "Tổng quan":
    st.markdown("""<div class="hero"><span class="pill">BẢNG ĐIỀU KHIỂN</span><h1 style="font-size:36px;margin-bottom:6px">Chào mừng trở lại 👋</h1><p>Theo dõi bức tranh đầu tư của bạn một cách rõ ràng và bình tĩnh.</p></div>""", unsafe_allow_html=True)
    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Vốn mô phỏng", "100.000.000 ₫", "+2,4%")
    c2.metric("Lợi nhuận kỳ vọng", "8,6%", "năm")
    c3.metric("Độ biến động", "12,8%", "ước tính")
    c4.metric("Mức rủi ro", "Trung bình", "mô phỏng")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="ME")
    vals = 100 * np.cumprod(1 + np.array([.012,.018,-.009,.025,.006,-.014,.021,.017,.004,.012,-.006,.024]))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates,y=vals,mode="lines",line=dict(color="#3b8ea5",width=3),fill="tozeroy",fillcolor="rgba(91,178,181,.14)",name="Hiệu suất mô phỏng"))
    fig.update_layout(height=330,margin=dict(l=10,r=10,t=25,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.55)",yaxis_title="Chỉ số (100 = ban đầu)",xaxis_title=None)
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Biểu đồ minh họa được tạo từ dữ liệu giả lập.")

elif page == "Lợi nhuận kỳ vọng":
    st.title("Lợi nhuận kỳ vọng")
    st.write("Điều chỉnh xác suất và lợi nhuận của từng kịch bản.")
    default = pd.DataFrame({"Kịch bản":["Tăng trưởng","Bình thường","Suy giảm"],"Xác suất (%)":[25,50,25],"Lợi nhuận (%)":[25,8,-15]})
    df = st.data_editor(default, num_rows="dynamic", use_container_width=True, key="scenario_editor")
    if len(df) and df["Xác suất (%)"].sum() > 0:
        probs = df["Xác suất (%)"].astype(float).to_numpy()/df["Xác suất (%)"].astype(float).sum()
        returns = df["Lợi nhuận (%)"].astype(float).to_numpy()
        expected = float(np.sum(probs*returns))
        variance = float(np.sum(probs*(returns-expected)**2))
        a,b,c = st.columns(3); a.metric("Lợi nhuận kỳ vọng",f"{expected:.2f}%"); b.metric("Phương sai",f"{variance:.2f}"); c.metric("Độ lệch chuẩn",f"{np.sqrt(variance):.2f}%")
        st.caption("Xác suất được chuẩn hóa về 100% khi tính toán.")

elif page == "Phân tích rủi ro":
    st.title("Phân tích rủi ro")
    df = pd.DataFrame({"Kịch bản":["Tăng trưởng","Bình thường","Suy giảm"],"Xác suất (%)":[25,50,25],"Lợi nhuận (%)":[25,8,-15]})
    df["Xác suất (%)"] = st.slider("Xác suất kịch bản suy giảm (%)",0,100,25)
    down = float(df.loc[2,"Xác suất (%)"])
    st.metric("Xác suất kịch bản suy giảm",f"{down:.0f}%")
    st.info("Đây là mô hình minh họa đơn giản, không dự báo thị trường thực tế.")
    fig = px.bar(pd.DataFrame({"Kịch bản":["Tăng trưởng","Bình thường","Suy giảm"],"Lợi nhuận (%)":[25,8,-15]}),x="Kịch bản",y="Lợi nhuận (%)",color="Lợi nhuận (%)",color_continuous_scale=["#d78383","#d7e9e7","#4c9b9a"])
    fig.update_layout(height=350,margin=dict(l=10,r=10,t=20,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,.5)")
    st.plotly_chart(fig,use_container_width=True)

elif page == "Danh mục đầu tư":
    st.title("Danh mục đầu tư")
    st.write("Thử thay đổi tỷ trọng để quan sát lợi nhuận kỳ vọng.")
    portfolio = pd.DataFrame({"Tài sản":["Cổ phiếu","Trái phiếu","Tiền mặt"],"Tỷ trọng (%)":[50,30,20],"Lợi nhuận kỳ vọng (%)":[12,5,2],"Độ lệch chuẩn (%)":[20,6,1]})
    edited = st.data_editor(portfolio,use_container_width=True,key="portfolio_editor")
    weights = edited["Tỷ trọng (%)"].astype(float).to_numpy()
    if weights.sum() > 0:
        w = weights/weights.sum()
        ret = float(np.sum(w*edited["Lợi nhuận kỳ vọng (%)"].astype(float).to_numpy()))
        risk = float(np.sqrt(np.sum((w*edited["Độ lệch chuẩn (%)"].astype(float).to_numpy())**2)))
        a,b = st.columns(2); a.metric("Lợi nhuận kỳ vọng",f"{ret:.2f}%"); b.metric("Rủi ro ước tính",f"{risk:.2f}%")
        st.caption("Rủi ro đang dùng giả định hiệp phương sai bằng 0 giữa các tài sản; đây chưa phải mô hình tối ưu danh mục.")

elif page == "Trợ lý giọng nói":
    st.title("💬 Trợ lý InvestLab")
    st.write("Nhập câu hỏi hoặc dùng nút micro để đọc câu hỏi bằng giọng nói. Trình duyệt cần cấp quyền microphone.")
    st.components.v1.html("""
    <div style="font-family:Inter,Arial;background:linear-gradient(135deg,#e4f4f8,#edf8f3);border:1px solid #cde5e9;border-radius:18px;padding:18px;color:#163b5b">
      <div style="display:flex;align-items:center;gap:12px">
        <div id="orb" style="width:58px;height:58px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#d7ffff,#66b8c1 60%,#3977a8);box-shadow:0 0 0 8px #9bd8d344;animation:pulse 2.4s infinite"></div>
        <div><b>InvestLab Voice</b><div style="font-size:13px;color:#678194">Trợ lý hỏi đáp • thử nghiệm trên trình duyệt</div></div>
      </div>
      <style>@keyframes pulse{0%,100%{transform:scale(1);box-shadow:0 0 0 7px #9bd8d344}50%{transform:scale(1.07);box-shadow:0 0 0 13px #9bd8d322}}</style>
      <p style="margin-top:18px">Bấm micro để nói. Văn bản nhận diện sẽ xuất hiện bên dưới.</p>
      <button onclick="listen()" style="background:#3977a8;color:white;border:0;border-radius:10px;padding:10px 16px;cursor:pointer">🎙️ Bắt đầu nói</button>
      <button onclick="speakAnswer()" style="background:#d3ebe8;color:#164b60;border:0;border-radius:10px;padding:10px 16px;margin-left:6px;cursor:pointer">🔊 Đọc câu trả lời</button>
      <p id="status" style="color:#3977a8;font-size:13px">Sẵn sàng</p>
      <textarea id="heard" placeholder="Câu hỏi được nhận diện sẽ hiện ở đây..." style="box-sizing:border-box;width:100%;min-height:75px;border:1px solid #cde0e8;border-radius:10px;padding:10px;background:white;color:#163b5b"></textarea>
      <p style="font-size:12px;color:#678194">Nhận diện giọng nói tùy trình duyệt/ngôn ngữ hỗ trợ. Nếu micro không hoạt động, hãy nhập câu hỏi ở ô bên dưới ứng dụng.</p>
    </div>
    <script>
    let lastText='';
    function listen(){
      const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
      if(!SR){document.getElementById('status').innerText='Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Hãy thử Chrome.';return;}
      const rec=new SR(); rec.lang='vi-VN'; rec.interimResults=false; rec.maxAlternatives=1;
      document.getElementById('status').innerText='Đang nghe...';
      rec.onresult=e=>{lastText=e.results[0][0].transcript;document.getElementById('heard').value=lastText;document.getElementById('status').innerText='Đã nhận diện: '+lastText;};
      rec.onerror=e=>document.getElementById('status').innerText='Không thể dùng micro: '+e.error;
      rec.onend=()=>{if(document.getElementById('status').innerText==='Đang nghe...')document.getElementById('status').innerText='Đã dừng nghe';};
      rec.start();
    }
    function speakAnswer(){
      const text=document.getElementById('heard').value||'Xin chào, tôi là trợ lý InvestLab. Bạn có thể hỏi về lợi nhuận kỳ vọng, độ lệch chuẩn và rủi ro đầu tư.';
      if(!('speechSynthesis' in window)){document.getElementById('status').innerText='Trình duyệt chưa hỗ trợ đọc văn bản.';return;}
      const u=new SpeechSynthesisUtterance(text);u.lang='vi-VN';speechSynthesis.cancel();speechSynthesis.speak(u);
    }
    </script>
    """, height=330)
    question = st.text_input("Hoặc nhập câu hỏi", placeholder="Ví dụ: Lợi nhuận kỳ vọng là gì?")
    if st.button("Gửi câu hỏi"):
        q = question.lower()
        if not question.strip(): st.warning("Hãy nhập câu hỏi trước.")
        elif "kỳ vọng" in q or "lợi nhuận" in q:
            st.success("Lợi nhuận kỳ vọng là trung bình có trọng số của các mức lợi nhuận theo xác suất xảy ra từng kịch bản: E(R) = Σ pᵢRᵢ.")
        elif "rủi ro" in q or "độ lệch chuẩn" in q or "phương sai" in q:
            st.success("Phương sai đo mức phân tán của lợi nhuận quanh giá trị kỳ vọng; độ lệch chuẩn là căn bậc hai của phương sai. Giá trị cao thường biểu thị biến động lớn hơn.")
        elif "danh mục" in q or "tỷ trọng" in q:
            st.success("Lợi nhuận kỳ vọng danh mục bằng tổng tỷ trọng từng tài sản nhân với lợi nhuận kỳ vọng tương ứng. Rủi ro còn phụ thuộc vào tương quan giữa các tài sản.")
        else:
            st.info("Tôi có thể giải thích các khái niệm lợi nhuận kỳ vọng, phương sai, độ lệch chuẩn và danh mục đầu tư. Hãy thử hỏi cụ thể hơn.")

elif page == "Cài đặt":
    st.title("Cài đặt")
    st.write("Tùy chỉnh vốn giả định và thông tin hiển thị.")
    capital = st.number_input("Vốn đầu tư giả định (VNĐ)",min_value=0,step=1000000,value=100000000)
    st.metric("Vốn đang chọn",f"{capital:,.0f} ₫")
    st.caption("Giá trị này hiện dùng để mô phỏng và chưa kết nối tài khoản ngân hàng hay dữ liệu thị trường.")
