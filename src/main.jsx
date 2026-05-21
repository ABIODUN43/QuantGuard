import React from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  Bell,
  Bot,
  Building2,
  Calendar,
  Check,
  ChevronRight,
  CloudUpload,
  Download,
  Eye,
  FileText,
  Gauge,
  Globe2,
  Home,
  LineChart,
  Lock,
  LogOut,
  Mail,
  Play,
  Search,
  Settings,
  Shield,
  Sparkles,
  Target,
  TrendingUp,
  Upload,
  Users,
  Wallet,
  Zap
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart as ReLineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import "../styles.css";
import "./react.css";

const SERVER_BASE = import.meta.env.VITE_SERVER_BASE || "http://127.0.0.1:8000";
const API_BASE = import.meta.env.VITE_API_BASE || `${SERVER_BASE}/api/v1`;
const green = "#06b36f";
const red = "#ff3d43";
const orange = "#ff8a00";
const blue = "#2878e8";
const purple = "#7c3ff2";

const queryClient = new QueryClient();

const nav = [
  ["dashboard", Home, "Dashboard"],
  ["upload", Upload, "Upload Data"],
  ["risk", Shield, "Risk Analysis"],
  ["forecasting", LineChart, "Forecasting"],
  ["recommendations", Sparkles, "Recommendations"],
  ["scenario", Zap, "Scenario Simulation"],
  ["reports", FileText, "Reports"],
  ["economic", Globe2, "Economic Intelligence"],
  ["settings", Settings, "Settings"]
];

function apiRequest(path, options = {}) {
  const token = localStorage.getItem("qg_token");
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  if (token) headers.Authorization = `Bearer ${token}`;
  return fetch(`${API_BASE}${path}`, { ...options, headers }).then(async (response) => {
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;
    if (!response.ok) throw new Error(data?.error?.message || data?.detail || "Request failed");
    return data;
  });
}

const money = (value) => `NGN ${Number(value || 0).toLocaleString("en-NG", { maximumFractionDigits: 0 })}`;
const pct = (value) => `${Math.round(Number(value || 0) * 100)}%`;
const scoreColor = (score) => (score >= 75 ? red : score >= 60 ? orange : green);

function AppRoot() {
  return (
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );
}

function App() {
  const [route, setRoute] = React.useState(localStorage.getItem("qg_token") ? "dashboard" : "landing");
  const [authMode, setAuthMode] = React.useState("signin");
  const [token, setToken] = React.useState(localStorage.getItem("qg_token") || "");

  const go = (next) => {
    setRoute(next);
    window.scrollTo(0, 0);
  };

  const onAuth = (payload) => {
    localStorage.setItem("qg_token", payload.access_token);
    localStorage.setItem("qg_user_id", payload.user_id);
    setToken(payload.access_token);
    go("dashboard");
  };

  const logout = () => {
    localStorage.removeItem("qg_token");
    localStorage.removeItem("qg_user_id");
    queryClient.clear();
    setToken("");
    go("landing");
  };

  if (route === "landing") return <Landing go={go} />;
  if (route === "auth") return <Auth mode={authMode} setMode={setAuthMode} onAuth={onAuth} />;
  if (!token) return <Auth mode={authMode} setMode={setAuthMode} onAuth={onAuth} />;
  return <ProtectedApp route={route} go={go} logout={logout} />;
}

function ProtectedApp({ route, go, logout }) {
  const business = useQuery({ queryKey: ["business"], queryFn: () => apiRequest("/business/me"), retry: false });
  if (business.isLoading) return <FullPageState title="Loading business workspace..." />;
  if (business.isError) return <Onboarding onDone={() => business.refetch()} logout={logout} />;
  return <Shell route={route} go={go} logout={logout} business={business.data} />;
}

function Logo() {
  return (
    <div className="brand">
      <div className="mark" />
      <div>
        <div className="brand-name">QuantGuard <span>AI</span></div>
        <div className="tagline">Predict. Protect. Prosper.</div>
      </div>
    </div>
  );
}

function Landing({ go }) {
  return (
    <main className="landing">
      <section className="hero">
        <nav className="landing-nav">
          <Logo />
          <div className="nav-links">
            <a href="#features">Features</a><a href="#works">How It Works</a><a href="#use">Use Cases</a><a href="#pricing">Pricing</a>
            <a href="#" onClick={(e) => { e.preventDefault(); go("auth"); }}>Log in</a>
            <button className="btn btn-primary" onClick={() => go("auth")}>Get Started Free <ArrowRight size={18} /></button>
          </div>
        </nav>
        <div className="hero-inner">
          <div>
            <div className="pill">AI-Powered Financial Intelligence for SMEs</div>
            <h1>Predict Financial Stress <span className="accent">Before</span> It Happens.</h1>
            <p className="hero-copy">QuantGuard AI uses advanced mathematics, machine learning, and real-time economic data to detect instability, forecast risk, and help SMEs make smarter decisions.</p>
            <div className="hero-actions">
              <button className="btn btn-primary" onClick={() => go("auth")}>Start Your Free Analysis <ArrowRight size={18} /></button>
              <button className="btn btn-ghost"><Play size={18} /> Watch Demo</button>
            </div>
            <div className="mini-features">
              <Mini icon={Sparkles} title="AI + Mathematics" text="Advanced risk models" />
              <Mini icon={Shield} title="Real-Time Insights" text="Economic intelligence" />
              <Mini icon={Target} title="Actionable Advice" text="Clear recommendations" />
            </div>
          </div>
          <DeviceMock />
        </div>
      </section>
      <div className="trust-band"><div className="trust"><p>Trusted by forward-thinking SMEs and organizations</p><div className="trust-items"><span>Nigerian SMEs</span><span>Cooperatives</span><span>Agro Businesses</span><span>Retailers</span><span>Manufacturers</span><span>Financial Institutions</span></div></div></div>
      <section className="section" id="features">
        <div className="section-title"><small>POWERFUL FEATURES</small><h2>Everything You Need to Stay Ahead of Risk</h2></div>
        <div className="feature-grid">
          <Feature icon={Bot} title="AI Risk Prediction" text="Predict financial stress before it impacts your business." />
          <Feature icon={TrendingUp} title="Real-Time Intelligence" text="Monitor economic indicators and business performance." />
          <Feature icon={Zap} title="Scenario Simulation" text="Test what-if changes before making decisions." />
          <Feature icon={Sparkles} title="Actionable Insights" text="Get clear recommendations tailored to your business." />
          <Feature icon={FileText} title="Smart Reports" text="Generate reports for lenders, investors, and partners." />
          <Feature icon={Bell} title="Risk Alerts" text="Get notified when risk indicators worsen." />
        </div>
      </section>
      <section className="section process" id="works">
        <div className="section-title"><small>HOW IT WORKS</small><h2>Simple Process. Powerful Results.</h2></div>
        <div className="steps">
          <Step n="1" icon={Users} title="Create Account" text="Sign up and set up your business profile." />
          <Step n="2" icon={CloudUpload} title="Upload Data" text="Upload financial records or enter data manually." />
          <Step n="3" icon={Bot} title="AI Analysis" text="Risk models detect drivers and probabilities." />
          <Step n="4" icon={BarChart3} title="Get Insights" text="View live forecasts and business health." />
          <Step n="5" icon={Target} title="Take Action" text="Use recommendations to reduce risk." />
        </div>
      </section>
    </main>
  );
}

function Auth({ mode, setMode, onAuth }) {
  const create = mode === "create";
  const [form, setForm] = React.useState({ full_name: "Daniel Okafor", email: "daniel@example.com", password: "securepassword" });
  const [resetToken, setResetToken] = React.useState("");
  const [newPassword, setNewPassword] = React.useState("newsecurepassword");
  const [error, setError] = React.useState("");
  const mutation = useMutation({
    mutationFn: async () => {
      if (create) await apiRequest("/auth/register", { method: "POST", body: JSON.stringify(form) }).catch((err) => {
        if (!String(err.message).includes("already exists")) throw err;
      });
      return apiRequest("/auth/login", { method: "POST", body: JSON.stringify({ email: form.email, password: form.password }) });
    },
    onSuccess: onAuth,
    onError: (err) => setError(err.message)
  });
  const resetRequest = useMutation({
    mutationFn: () => apiRequest("/auth/password-reset/request", { method: "POST", body: JSON.stringify({ email: form.email }) }),
    onError: (err) => setError(err.message)
  });
  const resetConfirm = useMutation({
    mutationFn: () => apiRequest("/auth/password-reset/confirm", { method: "POST", body: JSON.stringify({ token: resetToken || resetRequest.data?.reset_token, new_password: newPassword }) }),
    onError: (err) => setError(err.message)
  });

  return (
    <main className="auth-page">
      <section className="auth-left">
        <Logo />
        <div className="auth-copy"><h1>Predict Financial Stress <span className="accent">Before</span> It Happens.</h1><p>Sign in to access your financial intelligence workspace.</p></div>
        <AuthMini icon={TrendingUp} title="Risk Prediction" text="Detect liquidity stress before impact." />
        <AuthMini icon={BarChart3} title="Economic Intelligence" text="Track inflation, FX, and fuel pressure." />
        <AuthMini icon={Shield} title="Secure Workspace" text="JWT auth and protected business routes." />
      </section>
      <section className="auth-card">
        <div className="tabs">
          <button className={`tab ${!create ? "active" : ""}`} onClick={() => setMode("signin")}>Sign In</button>
          <button className={`tab ${create ? "active" : ""}`} onClick={() => setMode("create")}>Create Account</button>
        </div>
        <h2>{create ? "Create your account" : "Welcome back"}</h2>
        <p className="auth-muted">{create ? "Create an owner account, then onboard your business." : "Use the demo account or your registered account."}</p>
        {create && <Field label="Full Name" value={form.full_name} onChange={(v) => setForm({ ...form, full_name: v })} />}
        <Field label="Email Address" icon={Mail} value={form.email} onChange={(v) => setForm({ ...form, email: v })} />
        <Field label="Password" type="password" icon={Lock} value={form.password} onChange={(v) => setForm({ ...form, password: v })} />
        {error && <InlineError message={error} />}
        <button className="btn btn-primary" disabled={mutation.isPending} onClick={() => mutation.mutate()} style={{ width: "100%", fontSize: 18 }}>
          {mutation.isPending ? "Working..." : create ? "Create Account" : "Sign In"} <ArrowRight size={20} />
        </button>
        <p className="auth-switch">{create ? "Already have an account?" : "Don’t have an account?"} <a href="#" onClick={(e) => { e.preventDefault(); setMode(create ? "signin" : "create"); }}>{create ? "Sign in" : "Create one"}</a></p>
        {!create && (
          <div className="secure-note reset-panel">
            <Shield size={20} />
            <div>
              <b>Password reset</b>
              <p className="muted">Request a reset token, then confirm a new password. Dev mode returns the token here.</p>
              <div className="inline-actions">
                <button className="btn btn-light" disabled={resetRequest.isPending} onClick={() => resetRequest.mutate()}>{resetRequest.isPending ? "Requesting..." : "Request Token"}</button>
                <Field label="Reset Token" value={resetToken || resetRequest.data?.reset_token || ""} onChange={setResetToken} />
                <Field label="New Password" type="password" value={newPassword} onChange={setNewPassword} />
                <button className="btn btn-primary" disabled={resetConfirm.isPending} onClick={() => resetConfirm.mutate()}>{resetConfirm.isPending ? "Updating..." : "Set Password"}</button>
              </div>
              {resetRequest.data?.reset_token && <SuccessBox message={`Dev reset token: ${resetRequest.data.reset_token}`} />}
              {resetConfirm.isSuccess && <SuccessBox message="Password reset successfully. You can sign in with the new password." />}
            </div>
          </div>
        )}
        <div className="secure-note"><Shield size={20} /> Your data is protected with authenticated API access.</div>
      </section>
    </main>
  );
}

function Onboarding({ onDone, logout }) {
  const [form, setForm] = React.useState({
    business_name: "GreenField Stores",
    business_type: "Retail Trade",
    industry: "Retail",
    country: "Nigeria",
    state: "Lagos",
    city: "Ikeja",
    years_in_operation: 4,
    number_of_employees: 12,
    average_monthly_revenue: 2500000,
    average_monthly_expenses: 1800000
  });
  const mutation = useMutation({
    mutationFn: () => apiRequest("/business/onboard", { method: "POST", body: JSON.stringify(form) }),
    onSuccess: onDone
  });

  return (
    <main className="onboarding-page">
      <div className="onboarding-card">
        <Logo />
        <h1>Set Up Your Business Profile</h1>
        <p className="muted">QuantGuard needs your business baseline before running risk intelligence.</p>
        <div className="form-grid">
          {Object.keys(form).map((key) => (
            <Field key={key} label={labelize(key)} value={form[key]} type={typeof form[key] === "number" ? "number" : "text"} onChange={(value) => setForm({ ...form, [key]: typeof form[key] === "number" ? Number(value) : value })} />
          ))}
        </div>
        {mutation.isError && <InlineError message={mutation.error.message} />}
        <div className="form-actions">
          <button className="btn btn-light" onClick={logout}>Logout</button>
          <button className="btn btn-primary" disabled={mutation.isPending} onClick={() => mutation.mutate()}>Complete Onboarding <ArrowRight size={18} /></button>
        </div>
      </div>
    </main>
  );
}

function Shell({ route, go, logout, business }) {
  const Page = pages[route] || Dashboard;
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Logo />
        <nav className="side-nav">
          {nav.map(([id, Icon, label]) => <button key={id} className={`nav-item ${route === id ? "active" : ""}`} onClick={() => go(id)}><Icon size={20} />{label}</button>)}
        </nav>
        <div className="side-spacer" />
        <div className="side-card"><small>Your Business</small><b><Building2 size={16} /> {business.business_name}</b><small>{business.business_type}</small><br /><small>{business.city}, {business.country}</small><button className="btn btn-light" onClick={() => go("settings")}>View Business Profile <ArrowRight size={16} /></button></div>
        <button className="nav-item logout-btn" onClick={logout}><LogOut size={20} /> Logout</button>
      </aside>
      <main className="app-main">
        <Topbar business={business} logout={logout} />
        <div className="page"><Page go={go} business={business} logout={logout} /></div>
      </main>
    </div>
  );
}

function Dashboard({ go, business }) {
  const analysis = useLiveQuery(["analysis"], () => apiRequest("/analysis/latest"));
  const forecast = useLiveQuery(["forecast"], () => apiRequest("/forecast/latest"));
  const recommendations = useLiveQuery(["recommendations"], () => apiRequest("/recommendations"));
  const records = useLiveQuery(["records"], () => apiRequest("/data/records"));
  if (hasLoading(analysis, forecast, recommendations, records)) return <PageLoading />;
  if (analysis.isError && String(analysis.error.message).includes("No financial records")) {
    return <NoFinancialRecords go={go} />;
  }
  if (hasError(analysis, forecast, recommendations, records)) return <PageError queries={[analysis, forecast, recommendations, records]} />;
  const recordRows = records.data?.items || records.data?.records || records.data || [];
  const kpis = dashboardKpis(analysis.data, forecast.data, recordRows);
  return (
    <>
      <PageHead title={`Welcome back, ${business.business_name}`} sub="Live financial intelligence from your backend risk engine." actions={false} />
      <KpiGrid data={kpis} />
      <div className="grid-3">
        <Panel title="Cash Flow Overview"><CashflowChart data={forecast.data.cashflow_forecast} /></Panel>
        <Panel title="Risk Breakdown"><RiskDonut data={analysis.data.risk_breakdown} /><RiskMini breakdown={analysis.data.risk_breakdown} /></Panel>
        <Panel title="Risk Level"><RiskAlert analysis={analysis.data} /><button className="btn btn-light" onClick={() => go("risk")}>View Full Risk Analysis <ArrowRight size={16}/></button></Panel>
      </div>
      <div className="grid-2">
        <Panel title="Cash Balance Forecast"><BalanceChart data={forecast.data.cashflow_forecast} /><div className="alert-box">{forecast.data.danger_period}</div></Panel>
        <Panel title="Top Recommendations"><RecommendationList rows={recommendations.data.recommendations} limit={3} /><button className="btn btn-light" onClick={() => go("recommendations")}>View All Recommendations <ArrowRight size={16}/></button></Panel>
      </div>
      <div className="assistant-bar"><div className="assistant-face"><Bot /></div><div><b>QuantGuard AI Assistant</b><p className="muted">{analysis.data.summary}</p></div><button className="btn btn-primary">Ask</button></div>
    </>
  );
}

function UploadPage() {
  const [tab, setTab] = React.useState("upload");
  const qc = useQueryClient();
  const upload = useMutation({
    mutationFn: (file) => {
      const form = new FormData();
      form.append("file", file);
      return apiRequest("/data/upload", { method: "POST", body: form });
    },
    onSuccess: () => invalidateFinancial(qc)
  });
  const demoSeed = useMutation({
    mutationFn: () => apiRequest("/data/demo-seed", { method: "POST" }),
    onSuccess: () => invalidateFinancial(qc)
  });
  const records = useLiveQuery(["records"], () => apiRequest("/data/records"));
  return (
    <>
      <PageHead title="Upload Financial Data" sub="Upload CSV/Excel files or enter financial records manually." actions={false} />
      <div className="grid-main-side">
        <div>
          <div className="data-tabs">
            <DataTab active={tab === "upload"} onClick={() => setTab("upload")} icon={FileText} title="Upload File" text="Upload Excel or CSV file" />
            <DataTab active={tab === "manual"} onClick={() => setTab("manual")} icon={BarChart3} title="Manual Entry" text="Enter data manually" />
            <DataTab active={tab === "connect"} onClick={() => setTab("connect")} icon={CloudUpload} title="Connect Integration" text="Coming later" />
          </div>
          {tab === "upload" && <Panel><UploadBox mutation={upload} demoSeed={demoSeed} /></Panel>}
          {tab === "manual" && <ManualEntry />}
          {tab === "connect" && <EmptyState title="Accounting integrations are next" text="This MVP supports file upload and manual entry first." />}
      <Panel title="Recent Financial Records">{records.isLoading ? <InlineLoading /> : (records.data?.items || records.data?.records || []).length ? <RecordsTable rows={records.data.items || records.data.records} /> : <EmptyState title="No records yet" text="Upload data or add a manual entry to begin." />}</Panel>
        </div>
        <div>
          <Panel title="Data Requirements"><CheckList items={["Revenue / Sales","Operating Expenses","Cost of Goods Sold","Inventory Value","Debt Payment","Cash Balance","Fuel / Logistics Cost","Other Income"]} /></Panel>
          <Panel title="Upload Result">{upload.isPending || demoSeed.isPending ? <InlineLoading /> : upload.isError ? <InlineError message={upload.error.message} /> : demoSeed.isError ? <InlineError message={demoSeed.error.message} /> : upload.data ? <SuccessBox message={`${upload.data.records_processed} records processed.`} /> : demoSeed.data ? <SuccessBox message={`${demoSeed.data.records_processed} demo records loaded.`} /> : <p className="muted">Choose a file, enter one record, or load demo data.</p>}</Panel>
        </div>
      </div>
    </>
  );
}

export function NoFinancialRecords({ go }) {
  return (
    <div>
      <PageHead title="Add Financial Records" sub="QuantGuard needs revenue, expenses, cash, debt, inventory, and fuel data before it can calculate risk." actions={false} />
      <Panel>
        <EmptyState title="No financial records found" text="Upload a CSV/Excel file, add a manual entry, or load demo records from the Upload Data page." />
        <button className="btn btn-primary" onClick={() => go("upload")}>Go to Upload Data <ArrowRight size={16} /></button>
      </Panel>
    </div>
  );
}

function RiskPage() {
  const analysis = useLiveQuery(["analysis"], () => apiRequest("/analysis/latest"));
  if (analysis.isLoading) return <PageLoading />;
  if (analysis.isError) return <PageError queries={[analysis]} />;
  const breakdown = analysis.data.risk_breakdown;
  return (
    <>
      <PageHead title="Risk Analysis" sub="Live breakdown of the mathematical risk engine." />
      <Tabs items={["Overview","Liquidity Risk","Operational Risk","Financial Risk","External Risk","Risk Drivers"]} />
      <div className="grid-3">
        <Panel title="Overall Risk Score"><GaugeBlock value={analysis.data.risk_score} label={analysis.data.risk_level} /></Panel>
        <Panel title="Risk Driver Trend"><RiskBreakdownBars breakdown={breakdown} /></Panel>
        <Panel title="Stress Probability"><RiskDonut single value={Math.round(analysis.data.stress_probability * 100)} color={purple} /></Panel>
      </div>
      <div className="grid-main-side"><Panel title="Risk Breakdown"><RiskTable breakdown={breakdown} /></Panel><Panel title="Key Insight"><RiskAlert analysis={analysis.data} /><p>{analysis.data.summary}</p></Panel></div>
    </>
  );
}

function Forecasting() {
  const forecast = useLiveQuery(["forecast"], () => apiRequest("/forecast/latest"));
  if (forecast.isLoading) return <PageLoading />;
  if (forecast.isError) return <PageError queries={[forecast]} />;
  return (
    <>
      <PageHead title="Forecasting" sub="Cashflow and shortfall forecasts from backend projections." />
      <KpiGrid data={[
        ["Projected Cash Balance", money(forecast.data.projected_cash_balance), "", "Latest forecast", green, Wallet],
        ["Cash Shortfall Probability", pct(forecast.data.cash_shortfall_probability), "", "Forecast risk", orange, AlertTriangle],
        ["Forecast Confidence", pct(forecast.data.forecast_confidence), "", "Model confidence", blue, Target],
        ["Danger Period", forecast.data.danger_period, "", "Projected window", orange, Calendar],
        ["Breakeven Revenue", money(forecast.data.breakeven_revenue), "", "Revenue needed", blue, Target]
      ]} />
      <div className="grid-main-side"><div><Panel title="Cash Flow Forecast"><CashflowChart data={forecast.data.cashflow_forecast} /></Panel><Panel title="Cash Balance Projection"><BalanceChart data={forecast.data.cashflow_forecast} /></Panel></div><Panel title="Forecast Summary"><p>{forecast.data.danger_period}</p><RiskDonut single value={Math.round(forecast.data.cash_shortfall_probability * 100)} color={orange} /></Panel></div>
    </>
  );
}

function Recommendations() {
  const analysis = useLiveQuery(["analysis"], () => apiRequest("/analysis/latest"));
  const recQuery = useLiveQuery(["recommendations"], () => apiRequest("/recommendations"));
  if (hasLoading(analysis, recQuery)) return <PageLoading />;
  if (hasError(analysis, recQuery)) return <PageError queries={[analysis, recQuery]} />;
  return (
    <>
      <PageHead title="AI Recommendations" sub="Actionable steps generated from your current risk profile." />
      <KpiGrid data={dashboardKpis(analysis.data)} />
      <div className="grid-main-side"><Panel title="Top AI Recommendations"><RecommendationList rows={recQuery.data.recommendations} limit={10} /></Panel><Panel title="Why These Recommendations?">{Object.entries(analysis.data.risk_breakdown).map(([k, v]) => <Progress key={k} label={labelize(k)} value={v} color={scoreColor(v)} />)}</Panel></div>
    </>
  );
}

function ScenarioPage() {
  const [changes, setChanges] = React.useState({ fuel_price_increase_percent: 20, sales_change_percent: 0, operating_expenses_change_percent: 5, inventory_level_change_percent: 0, new_loan_amount: 0 });
  const mutation = useMutation({ mutationFn: () => apiRequest("/scenarios/run", { method: "POST", body: JSON.stringify({ scenario_name: "Fuel Price Increase +20%", changes }) }) });
  return (
    <>
      <PageHead title="Scenario Simulation" sub="Run backend scenario simulations against your current records." />
      <div className="scenario-grid">
        <Panel title="Adjust Variables">{Object.keys(changes).map((key) => <div className="adjust-row" key={key}><label>{labelize(key)}</label><input className="num" type="number" value={changes[key]} onChange={(e) => setChanges({ ...changes, [key]: Number(e.target.value) })} /><span>{key === "new_loan_amount" ? "NGN" : "%"}</span></div>)}<button className="btn btn-primary" onClick={() => mutation.mutate()}>Run Simulation <ArrowRight size={16}/></button></Panel>
        <Panel title="Scenario Result">{mutation.isPending ? <InlineLoading /> : mutation.isError ? <InlineError message={mutation.error.message} /> : mutation.data ? <ScenarioResult data={mutation.data} /> : <EmptyState title="No scenario run yet" text="Adjust variables and run a simulation." />}</Panel>
        <Panel title="AI Recommendation"><CheckList items={["Optimize routes and suppliers","Review pricing strategy","Preserve additional cash buffer","Monitor expenses weekly"]} /></Panel>
      </div>
    </>
  );
}

function ReportsPage() {
  const qc = useQueryClient();
  const reports = useLiveQuery(["reports"], () => apiRequest("/reports"));
  const templates = useLiveQuery(["report-templates"], () => apiRequest("/reports/templates"));
  const [reportType, setReportType] = React.useState("risk");
  const [format, setFormat] = React.useState("pdf");
  const generate = useMutation({ mutationFn: () => apiRequest("/reports/generate", { method: "POST", body: JSON.stringify({ report_type: reportType, format }) }), onSuccess: () => qc.invalidateQueries({ queryKey: ["reports"] }) });
  const templateRows = templates.data?.templates || [];
  return (
    <>
      <PageHead title="Reports" sub="Generate PDF and Excel intelligence reports." actions={false} />
      <Panel title="Quick Actions">
        <div className="inline-actions">
          <select value={reportType} onChange={(event) => setReportType(event.target.value)}>
            {(templateRows.length ? templateRows : [{ key: "risk", title: "Risk Intelligence Report" }, { key: "forecast", title: "Cashflow Forecast Report" }, { key: "scenario", title: "Scenario Simulation Report" }, { key: "lender", title: "Lender Readiness Report" }]).map((item) => <option key={item.key} value={item.key}>{item.title}</option>)}
          </select>
          <select value={format} onChange={(event) => setFormat(event.target.value)}>
            <option value="pdf">PDF</option>
            <option value="xlsx">Excel</option>
          </select>
          <button className="btn btn-primary" onClick={() => generate.mutate()} disabled={generate.isPending}>{generate.isPending ? "Generating..." : "Generate Report"}</button>
        </div>
        {generate.isError && <InlineError message={generate.error.message} />}
        {generate.data && <SuccessBox message={`Report ready: ${generate.data.download_url}`} />}
        {generate.data?.download_url && <a className="btn btn-light" href={`${SERVER_BASE}${generate.data.download_url}`} target="_blank" rel="noreferrer"><Download size={16}/> Open Download</a>}
      </Panel>
      <Panel title="All Reports">{reports.isLoading ? <InlineLoading /> : (reports.data?.items || reports.data?.reports || []).length ? <ReportsTable rows={reports.data.items || reports.data.reports} /> : <EmptyState title="No reports yet" text="Generate your first report." />}</Panel>
    </>
  );
}

function EconomicPage() {
  const qc = useQueryClient();
  const economic = useLiveQuery(["economic"], () => apiRequest("/economic/indicators"));
  const [form, setForm] = React.useState({
    country: "Nigeria",
    indicator_name: "Inflation Rate",
    indicator_value: 22.1,
    unit: "%",
    source: "manual",
    record_date: new Date().toISOString().slice(0, 10)
  });
  const addIndicator = useMutation({
    mutationFn: () => apiRequest("/economic/indicators", { method: "POST", body: JSON.stringify(form) }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["economic"] })
  });
  const seedHistory = useMutation({
    mutationFn: () => apiRequest("/economic/seed-history", { method: "POST" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["economic"] })
  });
  if (economic.isLoading) return <PageLoading />;
  if (economic.isError) return <PageError queries={[economic]} />;
  const latest = economic.data.indicators || [];
  const sortedLatest = sortEconomicIndicators(latest);
  const chartRows = economicHistoryRows(economic.data.history || {});
  return (
    <>
      <PageHead title="Economic Intelligence" sub="Manual macro indicators, risk mapping, alerts, and historical trend intelligence." />
      <KpiGrid data={sortedLatest.slice(0, 5).map((item) => [item.name, economicValue(item), "", item.trend_label || item.date, economicColor(item), Globe2])} />
      <div className="grid-main-side">
        <div>
          <Panel title="Historical Economic Indicators"><EconomicHistoryChart data={chartRows} /></Panel>
          <Panel title={`${economic.data.country} Indicators`}><EconomicTable rows={sortedLatest} /></Panel>
          <Panel title="Risk Factor Mapping"><EconomicMappingTable rows={economic.data.risk_mappings || []} /></Panel>
        </div>
        <div>
          <Panel title="Manual Indicator Entry">
            <div className="form-grid compact">
              <Field label="Country" value={form.country} onChange={(v) => setForm({ ...form, country: v })} />
              <Field label="Indicator Name" value={form.indicator_name} onChange={(v) => setForm({ ...form, indicator_name: v })} />
              <Field label="Value" type="number" value={form.indicator_value} onChange={(v) => setForm({ ...form, indicator_value: Number(v) })} />
              <Field label="Unit" value={form.unit} onChange={(v) => setForm({ ...form, unit: v })} />
              <Field label="Source" value={form.source} onChange={(v) => setForm({ ...form, source: v })} />
              <Field label="Date" type="date" value={form.record_date} onChange={(v) => setForm({ ...form, record_date: v })} />
            </div>
            {addIndicator.isError && <InlineError message={addIndicator.error.message} />}
            {addIndicator.isSuccess && <SuccessBox message="Economic indicator saved." />}
            <div className="inline-actions">
              <button className="btn btn-primary" disabled={addIndicator.isPending} onClick={() => addIndicator.mutate()}>{addIndicator.isPending ? "Saving..." : "Save Indicator"}</button>
              <button className="btn btn-light" disabled={seedHistory.isPending} onClick={() => seedHistory.mutate()}>{seedHistory.isPending ? "Loading..." : "Load History"}</button>
            </div>
          </Panel>
          <Panel title="Economic Alerts"><EconomicAlerts rows={economic.data.alerts || []} /></Panel>
          <Panel title="Public Data Sources"><DataSources rows={economic.data.public_sources || []} /></Panel>
        </div>
      </div>
    </>
  );
}

function SettingsPage({ business, logout }) {
  const settings = useLiveQuery(["settings"], () => apiRequest("/settings"));
  const auditLogs = useLiveQuery(["audit-logs"], () => apiRequest("/settings/audit-logs"));
  const exportData = useMutation({
    mutationFn: () => apiRequest("/settings/privacy/export"),
    onSuccess: (data) => {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "quantguard-account-export.json";
      anchor.click();
      URL.revokeObjectURL(url);
    }
  });
  const deleteAccount = useMutation({
    mutationFn: () => apiRequest("/settings/privacy/account", { method: "DELETE" }),
    onSuccess: () => logout?.()
  });
  return (
    <>
      <PageHead title="Settings" sub="Manage account, business, preferences and security settings." actions={false}/>
      <div className="settings-grid">
        <Panel><div className="settings-menu"><b>ACCOUNT SETTINGS</b><button className="active">Profile & Account</button><button>Business Information</button><button>Subscription & Billing</button><b>SECURITY</b><button>Password & Security</button><button>Data Privacy</button></div></Panel>
        <div>
          <Panel title="Business Information"><SimpleList rows={[["Business Name", business.business_name],["Industry", business.industry],["Location", `${business.city}, ${business.country}`],["Monthly Revenue", money(business.average_monthly_revenue)],["Monthly Expenses", money(business.average_monthly_expenses)]]}/></Panel>
          <Panel title="Profile">{settings.isLoading ? <InlineLoading /> : settings.isError ? <InlineError message={settings.error.message} /> : <SimpleList rows={Object.entries(settings.data.profile).map(([k, v]) => [labelize(k), String(v)])}/>}</Panel>
          <Panel title="Data Privacy">
            <div className="inline-actions">
              <button className="btn btn-light" disabled={exportData.isPending} onClick={() => exportData.mutate()}><Download size={16}/> {exportData.isPending ? "Exporting..." : "Export My Data"}</button>
              <button className="btn btn-danger" disabled={deleteAccount.isPending} onClick={() => window.confirm("Delete this account and business data?") && deleteAccount.mutate()}><AlertTriangle size={16}/> {deleteAccount.isPending ? "Deleting..." : "Delete Account"}</button>
            </div>
            {exportData.isError && <InlineError message={exportData.error.message} />}
            {deleteAccount.isError && <InlineError message={deleteAccount.error.message} />}
          </Panel>
          <Panel title="Audit Logs">{auditLogs.isLoading ? <InlineLoading /> : auditLogs.isError ? <InlineError message={auditLogs.error.message} /> : <AuditLogTable rows={auditLogs.data.items || []} />}</Panel>
        </div>
      </div>
    </>
  );
}

const pages = { dashboard: Dashboard, upload: UploadPage, risk: RiskPage, forecasting: Forecasting, recommendations: Recommendations, scenario: ScenarioPage, reports: ReportsPage, economic: EconomicPage, settings: SettingsPage };

function ManualEntry() {
  const qc = useQueryClient();
  const [form, setForm] = React.useState({ record_date: new Date().toISOString().slice(0, 10), revenue: 2450000, operating_expenses: 1870000, cost_of_goods_sold: 1120000, inventory_value: 850000, debt_payment: 210000, cash_balance: 580000, fuel_logistics_cost: 250000, other_income: 0 });
  const mutation = useMutation({ mutationFn: () => apiRequest("/data/manual-entry", { method: "POST", body: JSON.stringify(form) }), onSuccess: () => invalidateFinancial(qc) });
  return <Panel title="Manual Financial Entry"><div className="form-grid">{Object.keys(form).map((key) => <Field key={key} label={labelize(key)} value={form[key]} type={key === "record_date" ? "date" : "number"} onChange={(value) => setForm({ ...form, [key]: key === "record_date" ? value : Number(value) })} />)}</div>{mutation.isError && <InlineError message={mutation.error.message} />}{mutation.isSuccess && <SuccessBox message="Financial record saved and analysis refreshed." />}<button className="btn btn-primary" disabled={mutation.isPending} onClick={() => mutation.mutate()}>{mutation.isPending ? "Saving..." : "Save Record"}</button></Panel>;
}

function UploadBox({ mutation, demoSeed }) {
  const inputRef = React.useRef(null);
  return <div className="dropzone" onClick={() => inputRef.current?.click()}><input ref={inputRef} className="hidden-file" type="file" accept=".csv,.xlsx,.xls" onChange={(e) => e.target.files?.[0] && mutation.mutate(e.target.files[0])}/><div><div className="icon-round"><CloudUpload /></div><h3>Drag & drop your file here</h3><p>Supports .xlsx, .xls, .csv files up to 10MB</p><div className="inline-actions"><button className="btn btn-primary" type="button">Choose File</button><button className="btn btn-light" type="button" disabled={demoSeed?.isPending} onClick={(e) => { e.stopPropagation(); demoSeed?.mutate(); }}>{demoSeed?.isPending ? "Loading..." : "Load Demo Data"}</button></div></div></div>;
}

export function KpiGrid({ data }) {
  return <div className="kpi-grid">{data.map(([label, value, suffix, status, color, Icon]) => <div className="kpi" key={label}><div className="kpi-top"><label>{label}</label><span className="iconbox" style={{ color }}><Icon size={20}/></span></div><strong style={{ color }}>{value}<small>{suffix}</small></strong><span style={{ color }}>{status}</span></div>)}</div>;
}

function dashboardKpis(analysis, forecast, records = []) {
  const latestCash = records?.at?.(-1)?.cash_balance || forecast?.projected_cash_balance || 0;
  return [
    ["Liquidity Risk Score", Math.round(analysis?.risk_score || 0), "/100", analysis?.risk_level || "Unknown", scoreColor(analysis?.risk_score || 0), Gauge],
    ["Stress Probability", pct(analysis?.stress_probability), "", "90 day outlook", purple, Shield],
    ["Financial Stability", Math.round(analysis?.financial_stability_score || 0), "/100", "Backend score", blue, Shield],
    ["Forecast Confidence", pct(analysis?.forecast_confidence || forecast?.forecast_confidence), "", "Model confidence", green, Target],
    ["Cash Reserve", money(latestCash), "", "Current / projected", green, Wallet]
  ];
}

function CashflowChart({ data = [] }) {
  if (!data.length) return <EmptyState title="No forecast data" text="Run analysis after adding records." />;
  return <div className="chart-box"><ResponsiveContainer><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="month" tick={{ fontSize: 11 }} /><YAxis tickFormatter={(v) => `${Math.round(v / 1000000)}M`} /><Tooltip formatter={(v) => money(v)} /><Bar dataKey="projected_revenue" fill={green} name="Revenue" /><Bar dataKey="projected_expenses" fill={red} name="Expenses" /></BarChart></ResponsiveContainer></div>;
}

function BalanceChart({ data = [] }) {
  if (!data.length) return <EmptyState title="No projection data" text="Add financial records first." />;
  return <div className="chart-box"><ResponsiveContainer><AreaChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="month" tick={{ fontSize: 11 }} /><YAxis tickFormatter={(v) => `${Math.round(v / 1000000)}M`} /><Tooltip formatter={(v) => money(v)} /><Area dataKey="projected_cash_balance" stroke={green} fill="rgba(6,179,111,.16)" name="Cash Balance" /></AreaChart></ResponsiveContainer></div>;
}

function RiskBreakdownBars({ breakdown }) {
  const data = Object.entries(breakdown).map(([name, value]) => ({ name: labelize(name), value }));
  return <div className="chart-box"><ResponsiveContainer><BarChart data={data} layout="vertical" margin={{ left: 70 }}><CartesianGrid strokeDasharray="3 3" /><XAxis type="number" domain={[0, 100]} /><YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} /><Tooltip /><Bar dataKey="value" fill={orange} /></BarChart></ResponsiveContainer></div>;
}

function RiskDonut({ data, single, value, color = purple }) {
  const rows = single ? [{ name: "Risk", value }, { name: "Remaining", value: 100 - value }] : Object.entries(data || {}).map(([name, val]) => ({ name: labelize(name), value: val }));
  const colors = [red, orange, blue, purple, green, "#f6a400"];
  return <div className="donut-chart"><ResponsiveContainer><PieChart><Pie data={rows} innerRadius={55} outerRadius={82} dataKey="value">{rows.map((_, i) => <Cell key={i} fill={single ? (i === 0 ? color : "#e8edf4") : colors[i % colors.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer><strong>{single ? `${value}%` : "Risk"}</strong></div>;
}

function RiskMini({ breakdown }) { return <div className="list">{Object.entries(breakdown).map(([k, v]) => <div className="list-row" key={k}><span style={{ color: scoreColor(v) }}>●</span><b>{labelize(k)}</b><span>{Math.round(v)} /100</span></div>)}</div>; }
function RiskAlert({ analysis }) { return <div className="alert-box"><h2><AlertTriangle size={22}/> {analysis.risk_level}</h2><p>{analysis.summary}</p></div>; }
function RiskTable({ breakdown }) { return <table className="risk-table"><thead><tr><th>Risk Factor</th><th>Score</th><th>Impact</th><th>Key Insight</th></tr></thead><tbody>{Object.entries(breakdown).map(([k, v]) => <tr key={k}><td><b>{labelize(k)}</b></td><td style={{ color: scoreColor(v) }}><b>{Math.round(v)}</b> /100</td><td><span className={`badge ${v >= 70 ? "red" : v >= 50 ? "orange" : "green"}`}>{v >= 70 ? "High" : v >= 50 ? "Medium" : "Low"}</span></td><td>Monitor this driver and take corrective action when it rises.</td></tr>)}</tbody></table>; }
function RecommendationList({ rows = [], limit = 5 }) { if (!rows.length) return <EmptyState title="No recommendations yet" text="Run analysis to generate recommendations." />; return <div className="list">{rows.slice(0, limit).map((r) => <div className="list-row" key={r.id || r.title}><span className="iconbox"><Sparkles size={20}/></span><div><b>{r.title}</b><p>{r.description}</p></div><div><span className={`badge ${r.impact === "High" ? "green" : "orange"}`}>{r.impact}</span> <span className={`badge ${r.priority === "High" ? "red" : "orange"}`}>{r.priority}</span></div></div>)}</div>; }
function GaugeBlock({ value, label }) { return <><div className="gauge"><strong>{Math.round(value)}</strong></div><p className="center status-red">{label}</p></>; }
function Progress({ label, value, color }) { return <div className="progress-row"><b>{label}</b><div className="bar"><span style={{ width: `${value}%`, background: color }} /></div><b>{Math.round(value)}/100</b></div>; }

function RecordsTable({ rows }) { return <table><thead><tr><th>Date</th><th>Revenue</th><th>Expenses</th><th>Inventory</th><th>Debt</th><th>Cash</th></tr></thead><tbody>{rows.slice(-8).reverse().map((r) => <tr key={r.id}><td>{r.record_date}</td><td>{money(r.revenue)}</td><td>{money(r.operating_expenses)}</td><td>{money(r.inventory_value)}</td><td>{money(r.debt_payment)}</td><td>{money(r.cash_balance)}</td></tr>)}</tbody></table>; }
function ReportsTable({ rows }) { return <table><thead><tr><th>Report</th><th>Status</th><th>Created</th><th>Download</th></tr></thead><tbody>{rows.map((r) => <tr key={r.id}><td>{labelize(r.report_type)}</td><td><span className="badge green">{r.status}</span></td><td>{new Date(r.created_at).toLocaleString()}</td><td><a href={`${SERVER_BASE}${r.file_url}`} target="_blank" rel="noreferrer">Open file</a></td></tr>)}</tbody></table>; }
const economicPriority = ["Official USD/NGN", "Parallel USD/NGN", "USD/NGN Spread", "Inflation Rate", "Fuel Price Index", "Interest Rate", "Business Confidence"];

function sortEconomicIndicators(rows) {
  return [...rows].sort((a, b) => {
    const aIndex = economicPriority.indexOf(a.name);
    const bIndex = economicPriority.indexOf(b.name);
    return (aIndex === -1 ? 99 : aIndex) - (bIndex === -1 ? 99 : bIndex) || a.name.localeCompare(b.name);
  });
}

function economicColor(item) {
  if (item.name.includes("Parallel") || item.name.includes("Spread") || item.name.includes("Fuel") || item.name.includes("Inflation")) return orange;
  return green;
}

export function economicValue(item) {
  if (item.unit === "%") return `${item.value}%`;
  if (item.unit === "NGN") {
    const decimals = item.name.includes("Official") || item.name.includes("Spread") ? 2 : 0;
    return `₦${Number(item.value || 0).toLocaleString("en-NG", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
  }
  return `${item.value} ${item.unit}`;
}

export function economicHistoryRows(history) {
  const byDate = {};
  Object.entries(history).forEach(([name, points]) => {
    points.forEach((point) => {
      byDate[point.date] = byDate[point.date] || { date: point.date };
      byDate[point.date][name] = point.value;
    });
  });
  return Object.values(byDate).sort((a, b) => String(a.date).localeCompare(String(b.date)));
}

function EconomicHistoryChart({ data }) {
  if (!data.length) return <EmptyState title="No economic history yet" text="Load history or add indicators over time." />;
  return (
    <div className="chart-box">
      <ResponsiveContainer>
        <ReLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Line dataKey="Inflation Rate" stroke={purple} dot={false} />
          <Line dataKey="Fuel Price Index" stroke={orange} dot={false} />
          <Line dataKey="Interest Rate" stroke={red} dot={false} />
          <Line dataKey="Business Confidence" stroke={blue} dot={false} />
        </ReLineChart>
      </ResponsiveContainer>
    </div>
  );
}

function EconomicTable({ rows }) { return <table><thead><tr><th>Indicator</th><th>Value</th><th>Trend</th><th>Date</th><th>Source</th></tr></thead><tbody>{rows.map((r) => <tr key={r.name}><td>{r.name}</td><td>{economicValue(r)}</td><td>{r.trend_label}</td><td>{r.date}</td><td>{r.source}</td></tr>)}</tbody></table>; }

function EconomicMappingTable({ rows }) {
  if (!rows.length) return <EmptyState title="No risk mappings" text="Add indicators to map macro pressure to business risk." />;
  return <table><thead><tr><th>Indicator</th><th>Risk Factor</th><th>Severity</th><th>Impact</th></tr></thead><tbody>{rows.map((r) => <tr key={r.indicator}><td>{r.indicator}</td><td>{r.risk_factor}</td><td><span className={`badge ${r.severity === "high" ? "red" : r.severity === "medium" ? "orange" : "green"}`}>{r.severity}</span></td><td>{r.impact}</td></tr>)}</tbody></table>;
}

function EconomicAlerts({ rows }) {
  if (!rows.length) return <EmptyState title="No economic alerts" text="Current macro indicators are not breaching alert thresholds." />;
  return <div className="list">{rows.map((row) => <div className="list-row" key={`${row.indicator}-${row.date}`}><span className="iconbox"><AlertTriangle size={18}/></span><div><b>{row.indicator}</b><p>{row.message}</p></div><span className={`badge ${row.severity === "high" ? "red" : "orange"}`}>{row.severity}</span></div>)}</div>;
}

function DataSources({ rows }) {
  return <div className="list">{rows.map((row) => <div className="list-row" key={row.name}><span className="iconbox"><Globe2 size={18}/></span><div><b>{row.name}</b><p>{row.note}</p></div><span className="badge orange">{row.status}</span></div>)}</div>;
}
function AuditLogTable({ rows }) {
  if (!rows.length) return <EmptyState title="No audit logs yet" text="Security events will appear here after account and data actions." />;
  return <table><thead><tr><th>Action</th><th>Resource</th><th>Metadata</th><th>Time</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id}><td>{labelize(row.action)}</td><td>{row.resource}</td><td>{JSON.stringify(row.metadata || {})}</td><td>{new Date(row.created_at).toLocaleString()}</td></tr>)}</tbody></table>;
}
function ScenarioResult({ data }) { return <div className="scenario-result"><KpiGrid data={[["Risk Score", Math.round(data.risk_score), "/100", data.impact, scoreColor(data.risk_score), Shield],["Stress Probability", pct(data.stress_probability), "", "Scenario", purple, AlertTriangle],["Cash Shortfall", pct(data.cash_shortfall_probability), "", "Scenario", orange, Wallet]]}/><p>{data.summary}</p></div>; }

function Topbar({ business, logout }) { return <div className="topbar"><div className="search-wrap"><Search size={18}/><input className="search" placeholder="Search anything..." /></div><button className="btn btn-light bell-btn"><Bell size={20}/><span className="badge green">3</span></button><div className="user-block"><div className="avatar">{business.business_name.slice(0, 2).toUpperCase()}</div><div><b>{business.business_name}</b><span>{business.business_type}</span></div></div><button className="btn btn-light top-logout" onClick={logout}><LogOut size={16}/></button></div>; }
function PageHead({ title, sub, actions = true }) { return <div className="page-head"><div><h2>{title}</h2><p>{sub}</p></div>{actions && <div className="head-actions"><button className="btn btn-light"><Calendar size={16}/> May 22 - May 28, 2026</button><button className="btn btn-light"><Download size={16}/> Download Report</button></div>}</div>; }
function Panel({ title, children }) { return <section className="panel">{title && <h3>{title}</h3>}{children}</section>; }
function Field({ label, value, onChange, type = "text", icon: Icon }) { return <div className="field"><label>{label}</label><div className="field-inline">{Icon && <Icon size={20}/>}<input type={type} value={value} onChange={(e) => onChange(e.target.value)} /></div></div>; }
function Mini({ icon: Icon, title, text }) { return <div className="mini-feature"><span className="iconbox"><Icon size={20}/></span><div><b>{title}</b><span>{text}</span></div></div>; }
function AuthMini({ icon: Icon, title, text }) { return <div className="auth-feature"><span className="iconbox"><Icon size={24}/></span><div><b>{title}</b><p>{text}</p></div></div>; }
function Feature({ icon: Icon, title, text }) { return <div className="feature-card"><span className="iconbox"><Icon size={28}/></span><b>{title}</b><p>{text}</p></div>; }
function Step({ n, icon: Icon, title, text }) { return <div className="step"><div className="icon-round"><Icon size={30}/></div><b><span>{n}</span> {title}</b><p>{text}</p></div>; }
function DataTab({ icon: Icon, title, text, active, onClick }) { return <button className={`data-tab ${active ? "active" : ""}`} onClick={onClick}><span className="iconbox"><Icon/></span><div><b>{title}</b><br/><span className="muted">{text}</span></div></button>; }
function Tabs({ items }) { return <div className="tabs-row">{items.map((x, i) => <button className={i === 0 ? "active" : ""} key={x}>{x}</button>)}</div>; }
function SimpleList({ rows }) { return <div className="list">{rows.map((r) => <div className="list-row" key={r[0]}><span>●</span><div><b>{r[0]}</b><p>{r[1]}</p></div><ChevronRight size={16}/></div>)}</div>; }
function CheckList({ items }) { return <div className="list">{items.map((x) => <div className="list-row" key={x}><span className="status-green"><Check size={18}/></span><div><b>{x}</b></div></div>)}</div>; }

function DeviceMock() { return <div className="device"><div className="device-grid"><div className="device-rail"><Shield/><Home/><BarChart3/><FileText/><Settings/></div><div><div className="device-top"><span>Welcome back,<br/><b>GreenField Stores</b></span><span>Live AI</span></div><div className="device-cards">{[["Liquidity Risk","74","High Risk",red],["Stress Probability","72%","High",purple],["Stability","58","Medium",blue],["Confidence","89%","High",green]].map((c)=><div className="dark-card" key={c[0]}><small>{c[0]}</small><strong>{c[1]}</strong><em style={{color:c[3]}}>{c[2]}</em></div>)}</div><div className="device-main"><div className="dark-card chart-card"><small>Cash Flow Forecast</small><div className="mock-line"/></div><div className="dark-card"><small>Top Risk Drivers</small><div className="risk-list">{["Expense Volatility","Low Cash Reserve","Inventory Exposure","Fuel Sensitivity"].map((r)=><div className="risk-row" key={r}><span>{r}</span><span className="badge orange">Medium</span></div>)}</div></div></div></div></div></div>; }

function useLiveQuery(queryKey, queryFn) { return useQuery({ queryKey, queryFn, staleTime: 15000, retry: 1 }); }
function hasLoading(...queries) { return queries.some((q) => q.isLoading); }
function hasError(...queries) { return queries.some((q) => q.isError); }
function invalidateFinancial(qc) { ["records", "analysis", "forecast", "recommendations"].forEach((key) => qc.invalidateQueries({ queryKey: [key] })); }
export function labelize(value) { return value.replaceAll("_", " ").replace(/\b\w/g, (m) => m.toUpperCase()); }
function InlineLoading() { return <p className="muted">Loading...</p>; }
function PageLoading() { return <FullPageState title="Loading live financial intelligence..." />; }
function FullPageState({ title }) { return <main className="state-page"><Logo/><div className="panel"><h2>{title}</h2></div></main>; }
function InlineError({ message }) { return <div className="inline-error">{message}</div>; }
function PageError({ queries }) { return <div><PageHead title="Something needs attention" sub="One of the backend requests failed." actions={false}/>{queries.filter((q) => q.isError).map((q, i) => <InlineError key={i} message={q.error.message}/>)}</div>; }
export function EmptyState({ title, text }) { return <div className="empty-state"><h3>{title}</h3><p>{text}</p></div>; }
function SuccessBox({ message }) { return <div className="success-box">{message}</div>; }

const mount = document.getElementById("app");
if (mount) createRoot(mount).render(<AppRoot />);
