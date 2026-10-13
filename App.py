import React, { useMemo, useState } from "react";
import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Legend, Line,
  LineChart, Pie, PieChart, ResponsiveContainer, Scatter, ScatterChart,
  Tooltip, XAxis, YAxis, ZAxis
} from "recharts";
import {
  Activity, ArrowDownRight, ArrowUpRight, BarChart3, BookOpen, BriefcaseBusiness,
  Calculator, ChevronDown, CircleHelp, LayoutDashboard, Menu, Search, Settings,
  ShieldAlert, SlidersHorizontal, Wallet, X
} from "lucide-react";

const scenariosSeed = [
  { name: "Tích cực", probability: 25, returnPct: 30, color: "#16a36a" },
  { name: "Cơ sở", probability: 50, returnPct: 10, color: "#4778e8" },
  { name: "Tiêu cực", probability: 25, returnPct: -20, color: "#e45757" },
];
const performance = [
  { month: "T1", portfolio: 2, benchmark: 1 },
  { month: "T2", portfolio: -1, benchmark: 0 },
  { month: "T3", portfolio: 4, benchmark: 2 },
  { month: "T4", portfolio: 3, benchmark: 4 },
  { month: "T5", portfolio: 8, benchmark: 5 },
  { month: "T6", portfolio: 6, benchmark: 6 },
  { month: "T7", portfolio: 11, benchmark: 8 },
  { month: "T8", portfolio: 9, benchmark: 7 },
  { month: "T9", portfolio: 14, benchmark: 10 },
  { month: "T10", portfolio: 12, benchmark: 11 },
  { month: "T11", portfolio: 16, benchmark: 13 },
  { month: "T12", portfolio: 18, benchmark: 14 },
];
const initialAssets = [
  { ticker: "FPT", name: "FPT Corporation", weight: 35, expected: 16.5, risk: 23.0, color: "#4778e8" },
  { ticker: "VNM", name: "Vinamilk", weight: 25, expected: 10.2, risk: 16.0, color: "#16a36a" },
  { ticker: "VCB", name: "Vietcombank", weight: 25, expected: 13.4, risk: 19.0, color: "#e6a23c" },
  { ticker: "CASH", name: "Tiền mặt", weight: 15, expected: 4.0, risk: 1.0, color: "#8b75c9" },
];
const fmt = (n, digits = 2) => `${Number(n).toLocaleString("vi-VN", { maximumFractionDigits: digits, minimumFractionDigits: digits })}%`;
const money = (n) => `${Number(n).toLocaleString("vi-VN", { maximumFractionDigits: 1 })} tr`;

function NavItem({ icon: Icon, label, active, onClick }) {
  return <button className={`nav-item ${active ? "active" : ""}`} onClick={onClick}><Icon size={18}/><span>{label}</span>{active && <span className="nav-active-dot"/>}</button>;
}
function MetricCard({ icon: Icon, label, value, sub, tone = "green", trend }) {
  return <article className="metric-card">
    <div className="metric-top"><span className={`metric-icon ${tone}`}><Icon size={19}/></span>{trend && <span className={`trend ${trend.startsWith("-") ? "negative" : ""}`}>{trend.startsWith("-") ? <ArrowDownRight size={14}/> : <ArrowUpRight size={14}/>} {trend}</span>}</div>
    <div className="metric-label">{label} <CircleHelp size={13}/></div>
    <div className="metric-value">{value}</div>
    <div className="metric-sub">{sub}</div>
  </article>;
}
function App() {
  const [page, setPage] = useState("Tổng quan");
  const [mobileNav, setMobileNav] = useState(false);
  const [period, setPeriod] = useState("12 tháng");
  const [scenarios, setScenarios] = useState(scenariosSeed);
  const [assets, setAssets] = useState(initialAssets);
  const [capital, setCapital] = useState("100");
  const [showFormulas, setShowFormulas] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const probabilityTotal = scenarios.reduce((sum, s) => sum + Number(s.probability || 0), 0);
  const expected = scenarios.reduce((sum, s) => sum + (Number(s.probability || 0) / 100) * Number(s.returnPct || 0), 0);
  const variance = scenarios.reduce((sum, s) => sum + (Number(s.probability || 0) / 100) * (Number(s.returnPct || 0) - expected) ** 2, 0);
  const std = Math.sqrt(variance);
  const assetWeightTotal = assets.reduce((sum, a) => sum + Number(a.weight || 0), 0);
  const portfolioExpected = assets.reduce((sum, a) => sum + (Number(a.weight || 0) / 100) * Number(a.expected || 0), 0);
  const portfolioRiskApprox = Math.sqrt(assets.reduce((sum, a) => sum + (Number(a.weight || 0) / 100 * Number(a.risk || 0)) ** 2, 0));
  const allocation = assets.map(a => ({ name: a.ticker, value: Number(a.weight), color: a.color }));
  const filteredAssets = assets.filter(a => `${a.ticker} ${a.name}`.toLowerCase().includes(searchTerm.toLowerCase()));

  const updateScenario = (index, field, value) => setScenarios(prev => prev.map((s, i) => i === index ? { ...s, [field]: value } : s));
  const updateAsset = (index, field, value) => setAssets(prev => prev.map((a, i) => i === index ? { ...a, [field]: value } : a));
  const nav = [
    { label: "Tổng quan", icon: LayoutDashboard },
    { label: "Lợi nhuận kỳ vọng", icon: Calculator },
    { label: "Phân tích rủi ro", icon: Activity },
    { label: "Danh mục đầu tư", icon: BriefcaseBusiness },
    { label: "Kiến thức", icon: BookOpen },
  ];

  return <div className="app-shell">
    <aside className={`sidebar ${mobileNav ? "sidebar-open" : ""}`}>
      <div className="brand"><div className="brand-mark"><BarChart3 size={22}/></div><div><b>InvestLab</b><small>INVESTMENT ANALYTICS</small></div><button className="mobile-close" onClick={() => setMobileNav(false)}><X size={18}/></button></div>
      <div className="workspace-label">WORKSPACE</div>
      <nav>{nav.map(item => <NavItem key={item.label} icon={item.icon} label={item.label} active={page === item.label} onClick={() => { setPage(item.label); setMobileNav(false); }}/>)}</nav>
      <div className="sidebar-bottom">
        <div className="help-card"><div className="help-icon"><BookOpen size={17}/></div><b>Học cách đọc dữ liệu</b><p>Khám phá các chỉ số tài chính và ý nghĩa của chúng.</p><button onClick={() => setPage("Kiến thức")}>Mở thư viện <span>↗</span></button></div>
        <NavItem icon={Settings} label="Cài đặt" active={page === "Cài đặt"} onClick={() => setPage("Cài đặt")}/>
        <div className="profile"><div className="avatar">IL</div><div><b>Nhà đầu tư</b><small>Tài khoản demo</small></div><ChevronDown size={16}/></div>
      </div>
    </aside>
    {mobileNav && <button aria-label="Đóng menu" className="scrim" onClick={() => setMobileNav(false)}/>}
    <main className="main-area">
      <header className="topbar"><div className="topbar-left"><button className="mobile-menu" onClick={() => setMobileNav(true)}><Menu size={20}/></button><span className="breadcrumb">Workspace</span><span className="crumb-sep">/</span><b>{page}</b></div><div className="topbar-right"><span className="demo-pill"><span/> DỮ LIỆU MẪU</span><button className="icon-button" aria-label="Tìm kiếm" onClick={() => document.getElementById("asset-search")?.focus()}><Search size={18}/></button><div className="avatar small-avatar">IL</div></div></header>
      <div className="page-content">
        {page === "Tổng quan" && <>
          <div className="page-heading"><div><div className="eyebrow">THỨ HAI, 13 THÁNG 10, 2026</div><h1>Tổng quan đầu tư <span className="wave">✳</span></h1><p>Theo dõi hiệu suất và hiểu rõ rủi ro trong danh mục của bạn.</p></div><div className="heading-actions"><button className="button secondary" onClick={() => setPage("Danh mục đầu tư")}><SlidersHorizontal size={16}/> Phân bổ tài sản</button><button className="button primary" onClick={() => setPage("Lợi nhuận kỳ vọng")}><Calculator size={16}/> Tính toán mới</button></div></div>
          <div className="notice"><div className="notice-icon"><ShieldAlert size={17}/></div><div><b>Không gian mô phỏng</b><span>Số liệu trên trang là dữ liệu minh họa, không phải giá thị trường hoặc khuyến nghị đầu tư.</span></div><button onClick={() => setShowFormulas(v => !v)}>{showFormulas ? "Ẩn chi tiết" : "Tìm hiểu"} <span>↗</span></button></div>
          <section className="metrics-grid">
            <MetricCard icon={Wallet} label="Vốn đầu tư giả định" value={`${Number(capital || 0).toLocaleString("vi-VN")} tr`} sub="VND • Có thể điều chỉnh" tone="blue"/>
            <MetricCard icon={ArrowUpRight} label="Lợi nhuận kỳ vọng" value={fmt(portfolioExpected)} sub="Ước tính theo năm" tone="green" trend="+2,4%"/>
            <MetricCard icon={Activity} label="Độ lệch chuẩn ước tính" value={fmt(portfolioRiskApprox)} sub="Mô hình đơn giản, chưa có tương quan" tone="orange"/>
            <MetricCard icon={BarChart3} label="Số tài sản" value={String(assets.length).padStart(2, "0")} sub={`${assetWeightTotal}% tổng tỷ trọng`} tone="purple"/>
          </section>
          {showFormulas && <div className="formula-note"><b>Cách đọc chỉ số:</b> lợi nhuận kỳ vọng là trung bình có trọng số của các mức sinh lời giả định. Độ lệch chuẩn đo độ phân tán; rủi ro danh mục thực tế còn phụ thuộc tương quan giữa các tài sản.</div>}
          <section className="content-grid">
            <article className="panel performance-panel"><div className="panel-heading"><div><h2>Hiệu suất danh mục</h2><p>So sánh với chỉ số tham chiếu giả định</p></div><select value={period} onChange={e => setPeriod(e.target.value)} aria-label="Khoảng thời gian"><option>12 tháng</option><option>6 tháng</option><option>3 tháng</option></select></div>
              <div className="performance-summary"><div><span className="summary-number">+18,0%</span><span className="summary-caption">Danh mục <i className="legend-dot green-dot"/></span></div><div><span className="summary-number muted-number">+14,0%</span><span className="summary-caption">Tham chiếu <i className="legend-dot blue-dot"/></span></div><span className="period-chip">{period}</span></div>
              <div className="chart-area"><ResponsiveContainer width="100%" height="100%"><AreaChart data={performance.slice(period === "3 tháng" ? -3 : period === "6 tháng" ? -6 : 0)} margin={{ top: 8, right: 4, left: -18, bottom: 0 }}><defs><linearGradient id="portfolioFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#16a36a" stopOpacity={0.16}/><stop offset="100%" stopColor="#16a36a" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#edf0f5" vertical={false}/><XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: "#8993a5", fontSize: 11 }}/><YAxis axisLine={false} tickLine={false} tick={{ fill: "#8993a5", fontSize: 11 }} tickFormatter={v => `${v}%`}/><Tooltip formatter={(v) => [`${v}%`]} contentStyle={{ borderRadius: 12, border: "1px solid #e8edf3", fontSize: 12 }}/><Area type="monotone" dataKey="portfolio" name="Danh mục" stroke="#16a36a" strokeWidth={2.5} fill="url(#portfolioFill)"/><Line type="monotone" dataKey="benchmark" name="Tham chiếu" stroke="#4778e8" strokeWidth={2} dot={false}/></AreaChart></ResponsiveContainer></div>
              <div className="chart-footnote"><span><i className="legend-dot green-dot"/> Danh mục</span><span><i className="legend-dot blue-dot"/> Tham chiếu</span><span className="source-note">Dữ liệu giả lập</span></div>
            </article>
            <article className="panel allocation-panel"><div className="panel-heading"><div><h2>Phân bổ tài sản</h2><p>Cơ cấu danh mục hiện tại</p></div><button className="more-button" onClick={() => setPage("Danh mục đầu tư")}>Chi tiết ↗</button></div><div className="donut-wrap"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={allocation} dataKey="value" nameKey="name" innerRadius={63} outerRadius={87} paddingAngle={3} stroke="none">{allocation.map((a, i) => <Cell key={a.name} fill={a.color}/>)}</Pie><Tooltip formatter={v => `${v}%`}/></PieChart></ResponsiveContainer><div className="donut-center"><b>{assetWeightTotal}%</b><span>Tỷ trọng</span></div></div><div className="allocation-legend">{assets.map(a => <div className="allocation-row" key={a.ticker}><span className="allocation-name"><i style={{ background: a.color }}/>{a.ticker}</span><span className="allocation-bar"><i style={{ width: `${Math.min(100, a.weight)}%`, background: a.color }}/></span><b>{a.weight}%</b></div>)}</div>{assetWeightTotal !== 100 && <div className="inline-warning">Tổng tỷ trọng hiện là {assetWeightTotal}%, cần bằng 100% để phân tích danh mục.</div>}</article>
          </section>
          <section className="panel assets-panel"><div className="panel-heading table-heading"><div><h2>Tài sản trong danh mục</h2><p>Các thông số kỳ vọng do người dùng giả định</p></div><div className="table-actions"><div className="search-field"><Search size={15}/><input id="asset-search" placeholder="Tìm tài sản..." value={searchTerm} onChange={e => setSearchTerm(e.target.value)}/></div><button className="button secondary compact" onClick={() => setPage("Danh mục đầu tư")}>Chỉnh sửa</button></div></div><div className="table-scroll"><table><thead><tr><th>TÀI SẢN</th><th>TỶ TRỌNG</th><th>LỢI NHUẬN KỲ VỌNG</th><th>ĐỘ LỆCH CHUẨN</th><th>GIÁ TRỊ ƯỚC TÍNH</th></tr></thead><tbody>{filteredAssets.map(a => <tr key={a.ticker}><td><div className="asset-cell"><span className="ticker-icon" style={{ color: a.color, background: `${a.color}16` }}>{a.ticker.slice(0, 2)}</span><div><b>{a.ticker}</b><small>{a.name}</small></div></div></td><td>{a.weight}%</td><td><span className={a.expected >= 0 ? "positive" : "negative"}>{fmt(a.expected)}</span></td><td>{fmt(a.risk)}</td><td>{money(Number(capital || 0) * a.weight / 100)}</td></tr>)}</tbody></table></div></section>
        </>}
        {page === "Lợi nhuận kỳ vọng" && <><div className="page-heading"><div><div className="eyebrow">CÔNG CỤ THỐNG KÊ</div><h1>Máy tính lợi nhuận kỳ vọng</h1><p>Xây dựng kịch bản và xem tác động lên lợi nhuận cùng mức biến động.</p></div></div><div className="calculator-layout"><section className="panel scenario-panel"><div className="panel-heading"><div><h2>Kịch bản thị trường</h2><p>Nhập xác suất và tỷ suất sinh lời cho mỗi kịch bản.</p></div><button className="button secondary compact" onClick={() => setScenarios(scenariosSeed.map(s => ({...s})))}>Đặt lại</button></div><div className="scenario-list">{scenarios.map((s, i) => <div className="scenario-row" key={s.name}><div className="scenario-title"><i style={{background:s.color}}/><b>{s.name}</b></div><label>Xác suất (%)<input type="number" min="0" max="100" value={s.probability} onChange={e => updateScenario(i, "probability", Math.max(0, Math.min(100, Number(e.target.value))))}/></label><label>Tỷ suất sinh lời (%)<input type="number" value={s.returnPct} onChange={e => updateScenario(i, "returnPct", Number(e.target.value))}/></label><div className={`scenario-contribution ${s.returnPct < 0 ? "negative" : "positive"}`}>{(s.probability * s.returnPct / 100).toFixed(2)}%</div></div>)}</div><div className={`probability-total ${probabilityTotal !== 100 ? "invalid" : ""}`}><span>Tổng xác suất</span><b>{probabilityTotal}%</b><span>{probabilityTotal === 100 ? "Hợp lệ" : "Tổng xác suất cần bằng 100%"}</span></div><p className="helper-text">Mỗi kịch bản được giả định là rời nhau và bao phủ toàn bộ các kết quả có thể xảy ra.</p></section><section className="results-column"><div className="result-card featured"><span>Lợi nhuận kỳ vọng E(X)</span><strong>{fmt(expected)}</strong><p>Trung bình có trọng số theo xác suất kịch bản.</p></div><div className="result-card"><span>Phương sai Var(X)</span><strong>{variance.toLocaleString("vi-VN", {maximumFractionDigits: 3})} %²</strong><p>Đơn vị bình phương của tỷ suất sinh lời (%²).</p></div><div className="result-card"><span>Độ lệch chuẩn σ</span><strong>{fmt(std)}</strong><p>Căn bậc hai của phương sai, cùng đơn vị với lợi nhuận.</p></div><div className="panel contribution-panel"><div className="panel-heading"><div><h2>Đóng góp theo kịch bản</h2><p>Xác suất × tỷ suất sinh lời</p></div></div><div className="contribution-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={scenarios.map(s => ({name:s.name, contribution:s.probability*s.returnPct/100, color:s.color}))} margin={{top:10,right:10,left:-12,bottom:0}}><CartesianGrid stroke="#edf0f5" vertical={false}/><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize:11,fill:"#8993a5"}}/><YAxis axisLine={false} tickLine={false} tick={{fontSize:11,fill:"#8993a5"}} tickFormatter={v=>`${v}%`}/><Tooltip formatter={v=>`${Number(v).toFixed(2)}%`}/><Bar dataKey="contribution" name="Đóng góp" radius={[5,5,0,0]}>{scenarios.map(s=><Cell key={s.name} fill={s.color}/>)}</Bar></BarChart></ResponsiveContainer></div></div></section></div></>}
        {page === "Phân tích rủi ro" && <><div className="page-heading"><div><div className="eyebrow">RISK ANALYTICS</div><h1>Phân tích rủi ro</h1><p>Đọc mức biến động, phân phối kết quả và các giới hạn của mô hình.</p></div></div><div className="metrics-grid"><MetricCard icon={Activity} label="Độ lệch chuẩn kịch bản" value={fmt(std)} sub="Từ máy tính kịch bản" tone="orange"/><MetricCard icon={BarChart3} label="Phương sai" value={variance.toLocaleString("vi-VN",{maximumFractionDigits:2})+" %²"} sub="Bình phương độ lệch quanh kỳ vọng" tone="purple"/><MetricCard icon={ArrowDownRight} label="Kịch bản âm" value={scenarios.filter(s=>s.returnPct<0).length.toString()} sub="Số kịch bản có lợi nhuận âm" tone="red"/><MetricCard icon={ShieldAlert} label="Xác suất kịch bản âm" value={fmt(scenarios.filter(s=>s.returnPct<0).reduce((sum,s)=>sum+s.probability,0),0)} sub="Theo các kịch bản nhập vào" tone="blue"/></div><div className="content-grid risk-grid"><section className="panel"><div className="panel-heading"><div><h2>Phân phối kịch bản</h2><p>Tỷ suất sinh lời và xác suất tương ứng</p></div></div><div className="risk-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={scenarios} margin={{top:10,right:10,left:-10,bottom:0}}><CartesianGrid stroke="#edf0f5" vertical={false}/><XAxis dataKey="name" axisLine={false} tickLine={false}/><YAxis axisLine={false} tickLine={false} tickFormatter={v=>`${v}%`}/><Tooltip formatter={(v,n)=>[`${v}%`,n==="probability"?"Xác suất":"Lợi nhuận"]}/><Bar dataKey="probability" name="Xác suất" fill="#4778e8" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div></section><section className="panel"><div className="panel-heading"><div><h2>Diễn giải nhanh</h2><p>Dựa trên kịch bản hiện tại</p></div></div><div className="insight-list"><div className="insight"><span className="insight-bullet green-bg"><ArrowUpRight size={16}/></span><div><b>Lợi nhuận kỳ vọng {expected >= 0 ? "dương" : "âm"}</b><p>Giá trị trung bình theo xác suất là {fmt(expected)}.</p></div></div><div className="insight"><span className="insight-bullet orange-bg"><Activity size={16}/></span><div><b>Độ phân tán {std > 15 ? "tương đối lớn" : "trong mức minh họa"}</b><p>Độ lệch chuẩn là {fmt(std)}; đây không phải xác suất thua lỗ.</p></div></div><div className="insight"><span className="insight-bullet blue-bg"><CircleHelp size={16}/></span><div><b>Không mặc định phân phối chuẩn</b><p>Ba kịch bản rời rạc không đủ để kết luận lợi nhuận tuân theo phân phối chuẩn.</p></div></div></div></section></div><div className="notice risk-notice"><div className="notice-icon"><ShieldAlert size={17}/></div><div><b>Lưu ý về mô hình</b><span>Độ lệch chuẩn không mô tả đầy đủ rủi ro đuôi, thanh khoản hoặc khả năng thua lỗ cực đoan. Cần dữ liệu lịch sử và kiểm định giả định khi dùng thực tế.</span></div></div></>}
        {page === "Danh mục đầu tư" && <><div className="page-heading"><div><div className="eyebrow">PORTFOLIO BUILDER</div><h1>Xây dựng danh mục</h1><p>Điều chỉnh tỷ trọng và giả định lợi nhuận của từng tài sản.</p></div><button className="button secondary" onClick={() => setAssets(initialAssets.map(a=>({...a})))}>Khôi phục mẫu</button></div><div className="portfolio-layout"><section className="panel editor-panel"><div className="panel-heading"><div><h2>Phân bổ tài sản</h2><p>Chỉnh sửa tỷ trọng, lợi nhuận kỳ vọng và độ lệch chuẩn giả định.</p></div></div>{assets.map((a,i)=><div className="asset-editor" key={a.ticker}><div className="asset-editor-head"><span className="ticker-icon" style={{color:a.color,background:`${a.color}16`}}>{a.ticker.slice(0,2)}</span><b>{a.ticker}</b><span className="editor-weight">{a.weight}%</span></div><label>Tỷ trọng (%)<input type="number" min="0" max="100" value={a.weight} onChange={e=>updateAsset(i,"weight",Math.max(0,Math.min(100,Number(e.target.value))))}/></label><label>Lợi nhuận kỳ vọng (%)<input type="number" value={a.expected} onChange={e=>updateAsset(i,"expected",Number(e.target.value))}/></label><label>Độ lệch chuẩn riêng (%)<input type="number" min="0" value={a.risk} onChange={e=>updateAsset(i,"risk",Math.max(0,Number(e.target.value)))}/></label></div>)}<div className={`probability-total ${assetWeightTotal !== 100 ? "invalid" : ""}`}><span>Tổng tỷ trọng</span><b>{assetWeightTotal}%</b><span>{assetWeightTotal===100?"Hợp lệ":"Cần bằng 100%"}</span></div></section><section className="results-column"><div className="result-card featured"><span>Lợi nhuận kỳ vọng danh mục</span><strong>{fmt(portfolioExpected)}</strong><p>Tổng tỷ trọng có trọng số của lợi nhuận kỳ vọng tài sản.</p></div><div className="result-card"><span>Rủi ro xấp xỉ</span><strong>{fmt(portfolioRiskApprox)}</strong><p>Giả định độc lập giữa tài sản; chưa tính hiệp phương sai.</p></div><div className="panel"><div className="panel-heading"><div><h2>Cơ cấu phân bổ</h2><p>Tỷ trọng theo từng tài sản</p></div></div><div className="donut-wrap large-donut"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={allocation} dataKey="value" nameKey="name" innerRadius={65} outerRadius={94} paddingAngle={3} stroke="none">{allocation.map(a=><Cell key={a.name} fill={a.color}/>)}</Pie><Tooltip formatter={v=>`${v}%`}/></PieChart></ResponsiveContainer><div className="donut-center"><b>{assetWeightTotal}%</b><span>Tỷ trọng</span></div></div><div className="allocation-legend">{assets.map(a=><div className="allocation-row" key={a.ticker}><span className="allocation-name"><i style={{background:a.color}}/>{a.ticker}</span><span className="allocation-bar"><i style={{width:`${Math.min(100,a.weight)}%`,background:a.color}}/></span><b>{a.weight}%</b></div>)}</div></div></section></div><div className="notice"><div className="notice-icon"><CircleHelp size={17}/></div><div><b>Giới hạn tính toán</b><span>Rủi ro danh mục đang dùng tổng bình phương có trọng số, tương đương giả định hiệp phương sai bằng 0. Cần ma trận hiệp phương sai để có ước tính thực tế hơn.</span></div></div></>}
        {page === "Kiến thức" && <><div className="page-heading"><div><div className="eyebrow">LEARNING CENTER</div><h1>Kiến thức thống kê đầu tư</h1><p>Các khái niệm nền tảng để hiểu những con số trên dashboard.</p></div></div><div className="learning-grid"><article className="panel lesson-card"><span className="lesson-icon green-bg"><Calculator/></span><h2>Lợi nhuận kỳ vọng</h2><div className="equation">E(X) = Σ pᵢxᵢ</div><p>Trung bình có trọng số của các kết quả có thể xảy ra, theo xác suất tương ứng.</p><div className="example-box"><b>Ví dụ</b><p>25% × 30% + 50% × 10% + 25% × (−20%) = <strong>7,5%</strong>.</p></div></article><article className="panel lesson-card"><span className="lesson-icon orange-bg"><Activity/></span><h2>Phương sai</h2><div className="equation">Var(X) = E[(X − μ)²]</div><p>Đo mức phân tán quanh lợi nhuận kỳ vọng. Giá trị càng lớn cho thấy kết quả càng phân tán theo thước đo này.</p><div className="example-box"><b>Ghi nhớ</b><p>Phương sai có đơn vị bình phương; độ lệch chuẩn dễ diễn giải hơn.</p></div></article><article className="panel lesson-card"><span className="lesson-icon blue-bg"><BarChart3/></span><h2>Độ lệch chuẩn</h2><div className="equation">σ = √Var(X)</div><p>Đo mức biến động quanh kỳ vọng và có cùng đơn vị với tỷ suất sinh lời.</p><div className="example-box"><b>Không đồng nghĩa</b><p>Độ lệch chuẩn không phải xác suất thua lỗ hay thước đo đầy đủ cho mọi loại rủi ro.</p></div></article><article className="panel lesson-card"><span className="lesson-icon purple-bg"><Activity/></span><h2>Phân phối chuẩn</h2><div className="equation">X ~ N(μ, σ²)</div><p>Một mô hình xác suất liên tục hình chuông, được xác định bởi trung bình μ và phương sai σ².</p><div className="example-box"><b>Lưu ý</b><p>Không nên mặc định lợi nhuận tài chính tuân theo phân phối chuẩn; dữ liệu thực có thể có đuôi dày và lệch.</p></div></article></div></>}
        {page === "Cài đặt" && <><div className="page-heading"><div><div className="eyebrow">PREFERENCES</div><h1>Cài đặt</h1><p>Tùy chỉnh các thông số trong bản demo.</p></div></div><section className="panel settings-panel"><h2>Vốn đầu tư giả định</h2><p>Đơn vị hiển thị là triệu đồng (VND).</p><label className="setting-input">Số vốn (triệu VND)<input type="number" min="0" value={capital} onChange={e=>setCapital(e.target.value)}/></label><div className="notice"><div className="notice-icon"><CircleHelp size={17}/></div><div><b>Dữ liệu chỉ lưu trong phiên hiện tại</b><span>Bản demo chưa kết nối cơ sở dữ liệu và không lưu thông tin sau khi tải lại trang.</span></div></div></section></>}
        <footer className="footer"><span>© 2026 InvestLab · Bản demo học tập</span><span><i className="status-dot"/> Hệ thống mô phỏng đang hoạt động</span></footer>
      </div>
    </main>
  </div>;
}

export default App;