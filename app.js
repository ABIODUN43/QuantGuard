const app = document.querySelector("#app");

const navItems = [
  ["dashboard", "▦", "Dashboard"],
  ["upload", "⇧", "Upload Data"],
  ["risk", "◈", "Risk Analysis"],
  ["forecasting", "⌁", "Forecasting"],
  ["recommendations", "↯", "Recommendations"],
  ["scenario", "✣", "Scenario Simulation"],
  ["reports", "▤", "Reports"],
  ["economic", "◎", "Economic Intelligence"],
  ["alerts", "♧", "Alerts", "4"],
  ["settings", "⚙", "Settings"],
];

const kpis = [
  ["Liquidity Risk Score", "74", "/100", "High Risk", "red", "⌁"],
  ["Stress Probability (90 Days)", "72", "%", "High Probability", "purple", "◈"],
  ["Financial Stability Score", "58", "/100", "Medium", "blue", "▣"],
  ["Forecast Confidence", "89", "%", "High", "green", "◎"],
  ["Cash Reserve (Current)", "₦1,250,000", "", "2.7 months of expenses", "green", "◌"],
];

const riskFactors = [
  ["Expense Instability", "Variability in operating expenses", "75", "High", "red", "↑ 12 pts", "#ff3d43"],
  ["Liquidity Weakness", "Ability to meet short-term obligations", "68", "High", "orange", "↑ 8 pts", "#ff8a00"],
  ["Inventory Exposure", "Capital tied in inventory", "62", "Medium", "orange", "↑ 4 pts", "#f6a400"],
  ["Debt Pressure", "Debt level and repayment burden", "40", "Medium", "blue", "↓ 5 pts", "#2878e8"],
  ["Revenue Volatility", "Stability of revenue streams", "72", "High", "purple", "↑ 10 pts", "#7c3ff2"],
  ["Fuel Cost Sensitivity", "Exposure to fuel price changes", "65", "Medium", "green", "↑ 7 pts", "#06b36f"],
];

const recommendations = [
  ["Preserve Cash Reserves", "Your liquidity risk is high. Build cash reserves to cover at least 3 months of operating expenses.", "High", "High", "💰"],
  ["Reduce Inventory Exposure", "Inventory levels are above optimal. Reduce holding cost and risk of obsolescence.", "High", "High", "□"],
  ["Negotiate Better Payment Terms", "Improve your cash conversion cycle by negotiating longer payment terms with suppliers.", "Medium", "Medium", "▣"],
  ["Monitor Fuel & Logistics Costs", "Fuel price volatility is impacting your expenses. Optimize routes and suppliers.", "Medium", "Medium", "▤"],
  ["Increase Revenue Diversification", "Reduce dependency on a few products/customers to stabilize revenue streams.", "Medium", "Low", "▧"],
];

function icon(name) {
  return `<span class="iconbox">${name}</span>`;
}

function wave(color = "#06b36f") {
  return `<svg class="wave" viewBox="0 0 160 42" preserveAspectRatio="none" aria-hidden="true">
    <path d="M2 31 C18 30, 18 8, 32 13 S51 38, 66 27 S80 12, 93 20 S112 32, 126 18 S144 20, 158 18" fill="none" stroke="${color}" stroke-width="3"/>
  </svg>`;
}

function chart(type = "bars") {
  if (type === "line") {
    return `<svg class="chart" viewBox="0 0 700 260" preserveAspectRatio="none">
      ${grid()}
      <path d="M30 170 C80 120, 110 160, 150 135 S230 165, 275 128 S350 135, 390 105 S475 140, 520 95 S610 90, 670 70" fill="none" stroke="#06b36f" stroke-width="4"/>
      <path d="M30 170 C80 120, 110 160, 150 135 S230 165, 275 128 S350 135, 390 105 S475 140, 520 95 S610 90, 670 70 L670 230 L30 230 Z" fill="rgba(6,179,111,.12)"/>
    </svg>`;
  }
  if (type === "risk") {
    return `<svg class="chart" viewBox="0 0 700 260" preserveAspectRatio="none">
      ${grid()}
      <rect x="360" y="25" width="305" height="205" fill="rgba(255,61,67,.08)"/>
      <polyline points="30,190 120,180 210,170 300,155 390,125 480,90 570,70 660,62" fill="none" stroke="#ff8a00" stroke-width="4"/>
      <g fill="#ff8a00">${[30,120,210,300,390,480,570,660].map((x,i)=>`<circle cx="${x}" cy="${[190,180,170,155,125,90,70,62][i]}" r="5"/>`).join("")}</g>
    </svg>`;
  }
  return `<svg class="chart" viewBox="0 0 700 260" preserveAspectRatio="none">
    ${grid()}
    ${[70,180,290,400,510,620].map((x,i)=>`<rect x="${x}" y="${[78,62,85,72,92,80][i]}" width="30" height="${[132,148,125,138,118,130][i]}" rx="4" fill="#06b36f"/><rect x="${x+48}" y="${[116,98,128,112,126,110][i]}" width="30" height="${[94,112,82,98,84,100][i]}" rx="4" fill="#ff3d43"/>`).join("")}
    <polyline points="30,110 95,158 160,142 225,174 290,195 355,212 420,178 485,150 550,160 615,155 675,78" fill="none" stroke="#07111f" stroke-width="3"/>
  </svg>`;
}

function grid() {
  let lines = "";
  for (let i = 30; i < 240; i += 42) lines += `<line x1="25" y1="${i}" x2="675" y2="${i}" stroke="#e7edf4"/>`;
  for (let i = 60; i < 680; i += 90) lines += `<line x1="${i}" y1="25" x2="${i}" y2="230" stroke="#eef2f7"/>`;
  return lines;
}

function spark(color) {
  return `<svg class="spark" viewBox="0 0 110 34"><path d="M1 22 C12 9, 20 25, 32 16 S52 19, 63 7 S81 24, 96 14 S105 16,109 12" fill="none" stroke="${color}" stroke-width="2"/></svg>`;
}

function kpiCards(custom = kpis) {
  return `<div class="kpi-grid">${custom.map(([label, value, suffix, status, color, ico]) => `
    <div class="kpi">
      <div class="kpi-top"><label>${label}</label><span class="iconbox status-${color}">${ico}</span></div>
      <strong class="status-${color}">${value}<small>${suffix}</small></strong>
      <span class="status-${color}">${status}</span>
      ${value.includes("₦") ? "" : wave(colorMap(color))}
    </div>`).join("")}</div>`;
}

function colorMap(c) {
  return { red: "#ff3d43", orange: "#ff8a00", green: "#06b36f", blue: "#2878e8", purple: "#7c3ff2" }[c] || "#06b36f";
}

function landing() {
  app.innerHTML = `<main class="landing">
    <section class="hero">
      <nav class="landing-nav">
        ${brand()}
        <div class="nav-links">
          <a href="#features">Features</a><a href="#works">How It Works</a><a href="#use">Use Cases</a><a href="#pricing">Pricing</a><a href="#about">About Us</a>
          <a href="#" data-route="auth">Log in</a><button class="btn btn-primary" data-route="auth">Get Started Free →</button>
        </div>
      </nav>
      <div class="hero-inner">
        <div>
          <div class="pill">AI-Powered Financial Intelligence for SMEs</div>
          <h1>Predict Financial Stress <span class="accent">Before</span> It Happens.</h1>
          <p class="hero-copy">QuantGuard AI uses advanced mathematics, machine learning, and real-time economic data to detect financial instability, forecast risks, and help SMEs make smarter decisions.</p>
          <div class="hero-actions"><button class="btn btn-primary" data-route="auth">Start Your Free Analysis →</button><button class="btn btn-ghost">▷ Watch Demo</button></div>
          <div class="mini-features">
            ${mini("✥", "AI + Mathematics", "Advanced risk models")}
            ${mini("◇", "Real-Time Insights", "Economic intelligence")}
            ${mini("✣", "Actionable Advice", "Clear recommendations")}
          </div>
        </div>
        ${deviceMock()}
      </div>
    </section>
    <div class="trust-band"><div class="trust"><p>Trusted by forward-thinking SMEs and organizations</p><div class="trust-items"><span>▣ Nigerian SMEs</span><span>♟ Cooperatives</span><span>◒ Agro Businesses</span><span>🛒 Retailers</span><span>▥ Manufacturers</span><span>▤ Financial Institutions</span></div></div></div>
    <section class="section" id="features">
      <div class="section-title"><small>POWERFUL FEATURES</small><h2>Everything You Need to Stay Ahead of Risk</h2></div>
      <div class="feature-grid">
        ${feature("♧", "AI Risk Prediction", "Advanced models predict financial stress before it impacts your business.")}
        ${feature("↗", "Real-Time Intelligence", "Monitor economic indicators, market trends, and business performance in real-time.")}
        ${feature("◇", "Scenario Simulation", "Test different scenarios and see how changes affect your financial stability.")}
        ${feature("☼", "Actionable Insights", "Get clear, data-driven recommendations tailored to your business.")}
        ${feature("▤", "Smart Reports", "Generate professional reports for lenders, investors, and partners.")}
        ${feature("♧", "Risk Alerts", "Receive instant alerts when your business is at risk.")}
      </div>
    </section>
    <section class="section process" id="works">
      <div class="section-title"><small>HOW IT WORKS</small><h2>Simple Process. Powerful Results.</h2></div>
      <div class="steps">
        ${step(1, "♙", "Create Account", "Sign up and set up your business profile in minutes.")}
        ${step(2, "☁", "Upload Data", "Upload your financial data or connect your accounting system.")}
        ${step(3, "♧", "AI Analysis", "Our AI + mathematical models analyze your data and detect risks.")}
        ${step(4, "▥", "Get Insights", "View detailed insights, forecasts, and risk probabilities.")}
        ${step(5, "◎", "Take Action", "Use recommendations to make smarter financial decisions.")}
      </div>
      <div class="stat-strip">${stat("◇","95%","Prediction Accuracy")}${stat("▥","10K+","Businesses Analyzed")}${stat("◷","24/7","Real-Time Monitoring")}${stat("♕","Trusted","By SMEs Nationwide")}</div>
      <div class="cta"><div><h2>Ready to Protect Your Business?</h2><p>Join thousands of SMEs using QuantGuard AI to stay ahead of financial risk.</p></div><button class="btn btn-primary" data-route="auth">Start Your Free Analysis →</button></div>
    </section>
    <footer class="footer-wrap"><div class="footer">${brand()}<div><b>Product</b><a>Features</a><a>How It Works</a><a>Pricing</a></div><div><b>Company</b><a>About Us</a><a>Careers</a><a>Blog</a></div><div><b>Resources</b><a>Help Center</a><a>Documentation</a><a>API</a></div><div><b>Stay Updated</b><p>Get the latest insights on financial intelligence and economic trends.</p><button class="btn btn-primary">Subscribe</button></div></div></footer>
  </main>`;
  bindRoutes();
}

function brand() {
  return `<div class="brand"><div class="mark"></div><div><div class="brand-name">QuantGuard <span>AI</span></div><div class="tagline">Predict. Protect. Prosper.</div></div></div>`;
}

function mini(i, b, p) { return `<div class="mini-feature">${icon(i)}<div><b>${b}</b><span>${p}</span></div></div>`; }
function feature(i, b, p) { return `<div class="feature-card">${icon(i)}<b>${b}</b><p>${p}</p></div>`; }
function step(n, i, b, p) { return `<div class="step"><div class="icon-round">${i}</div><b><span>${n}</span> ${b}</b><p>${p}</p></div>`; }
function stat(i, n, p) { return `<div class="stat">${icon(i)}<div><strong>${n}</strong><span>${p}</span></div></div>`; }

function deviceMock() {
  return `<div class="device"><div class="device-grid"><div class="device-rail"><div class="dot-icon">◈</div><div class="dot-icon">⌂</div><div class="dot-icon">▥</div><div class="dot-icon">▤</div><div class="dot-icon">◎</div></div><div><div class="device-top"><span>Welcome back,<br><b>GreenField Stores 👋</b></span><span>Networth ◉</span></div><div class="device-cards">${[
    ["Liquidity Risk Score","74","High Risk","#ff3d43"],["Stress Probability","72%","High Probability","#ff3d43"],["Financial Stability","58","Medium","#ff8a00"],["Forecast Confidence","89%","High","#06b36f"]
  ].map(([a,b,c,d])=>`<div class="dark-card"><small>${a}</small><strong>${b}</strong><em style="color:${d}">${c}</em>${wave(d)}</div>`).join("")}</div><div class="device-main"><div class="dark-card chart-card"><small>Cash Flow Forecast (Next 90 Days)</small>${chart("line")}</div><div class="dark-card"><small>Top Risk Drivers</small><div class="risk-list">${["Expense Volatility","Low Cash Reserve","Inventory Exposure","Debt Pressure","Fuel Cost Sensitivity"].map((r,i)=>`<div class="risk-row"><span>${r}</span><span class="badge ${i<2?"red":"orange"}">${i<2?"High":"Medium"}</span></div>`).join("")}</div><button class="btn btn-light" style="width:100%;margin-top:14px">View Full Analysis</button></div></div></div></div></div>`;
}

let authMode = "signin";

function auth() {
  const isCreate = authMode === "create";
  app.innerHTML = `<main class="auth-page">
    <section class="auth-left">
      ${brand()}
      <div class="auth-copy"><h1>Predict Financial Stress <span class="accent">Before</span> It Happens.</h1><p>QuantGuard AI uses advanced mathematics, AI, and real-time economic data to detect financial instability, forecast risks, and help SMEs make smarter decisions.</p></div>
      <div>${miniAuth("↗","AI-Powered Risk Prediction","Detect liquidity stress and operational risks before they impact your business.")}${miniAuth("▥","Real-Time Economic Intelligence","Monitor inflation, exchange rates, fuel prices, and more.")}${miniAuth("◇","Smart Recommendations","Get actionable advice to strengthen your business and protect your cashflow.")}</div>
      <div class="auth-preview">${deviceMock()}</div>
    </section>
    <section class="auth-card">
      <div class="tabs"><button class="tab ${isCreate ? "" : "active"}" data-auth-mode="signin">Sign In</button><button class="tab ${isCreate ? "active" : ""}" data-auth-mode="create">Create Account</button></div>
      <h2>${isCreate ? "Create your account" : "Welcome back!"}</h2><p class="muted" style="color:rgba(255,255,255,.72)">${isCreate ? "Start your free QuantGuard AI analysis" : "Sign in to your QuantGuard AI account"}</p>
      <div class="socials"><button class="btn btn-ghost">G Continue with Google</button><button class="btn btn-ghost">▦ Continue with Microsoft</button><button class="btn btn-ghost">● Continue with Apple</button></div>
      <div class="divider">OR</div>
      ${isCreate ? `<div class="field"><label>Business Name</label><input placeholder="GreenField Stores"></div><div class="field"><label>Business Category</label><select><option>Retail Trade</option><option>Agriculture</option><option>Pharmacy</option><option>Manufacturing</option></select></div>` : ""}
      <div class="field"><label>Email Address</label><input placeholder="you@example.com"></div>
      <div class="field"><label>Password</label><input type="password" placeholder="Enter your password"></div>
      <div class="remember"><span>☑ ${isCreate ? "I agree to the Terms" : "Remember me"}</span><a href="#">${isCreate ? "Privacy Policy" : "Forgot password?"}</a></div>
      <button class="btn btn-primary" data-route="dashboard" style="width:100%;font-size:18px">${isCreate ? "Create Account" : "Sign In"} →</button>
      <p style="text-align:center;margin-top:28px;color:rgba(255,255,255,.74)">${isCreate ? "Already have an account?" : "Don’t have an account?"} <a href="#" data-auth-mode="${isCreate ? "signin" : "create"}">${isCreate ? "Sign in" : "Create one"}</a></p>
      <div class="secure-note">◇ Your data is encrypted and secure with enterprise-grade protection.</div>
    </section>
  </main>`;
  bindRoutes();
}

function miniAuth(i, b, p) { return `<div class="auth-feature">${icon(i)}<div><b>${b}</b><p>${p}</p></div></div>`; }

function shell(page) {
  app.innerHTML = `<div class="app-shell"><aside class="sidebar">${brand()}<nav class="side-nav">${navItems.map(([id, ico, label, count]) => `<button class="nav-item ${id===page?"active":""}" data-route="${id}"><span>${ico}</span>${label}${count?`<span class="count">${count}</span>`:""}</button>`).join("")}</nav><div class="side-spacer"></div><div class="side-card"><small>Your Business</small><b>▣ GreenField Stores</b><small>● Retail Trade</small><br><small>⌖ Lagos, Nigeria</small><button class="btn btn-light">View Business Profile →</button></div><div class="side-card upgrade"><b>🔥 Upgrade to Pro</b><p>Unlock advanced analytics, scenario tools and priority support.</p><button class="btn btn-primary">Upgrade Now</button></div></aside><main class="app-main"><div class="topbar"><input class="search" placeholder="Search anything..."><button class="btn btn-light">♧ <span class="badge green">3</span></button><div class="user-block"><div class="avatar">DO</div><div><b>Daniel Okafor</b><span>Business Owner</span></div></div></div><div class="page">${pages[page]()}</div></main></div>`;
  bindRoutes();
}

function pageHead(title, sub, actions = true) {
  return `<div class="page-head"><div><h2>${title}</h2><p>${sub}</p></div>${actions ? `<div class="head-actions"><button class="btn btn-light">▣ May 22 – May 28, 2026</button><button class="btn btn-light">⇩ Download Report</button></div>` : ""}</div>`;
}

const pages = {
  dashboard: () => `${pageHead("Welcome back, Daniel 👋", "Here’s what’s happening with GreenField Stores today.", false)}${kpiCards()}<div class="grid-3"><div class="panel"><h3>Cash Flow Overview</h3>${chart()}</div><div class="panel"><h3>Risk Breakdown</h3><div class="donut-wrap"><div class="donut"><strong>74</strong></div>${riskMini()}</div></div><div class="panel"><h3>Risk Level</h3><div class="alert-box"><h2>⚠ High Risk</h2><p>Your business is vulnerable to liquidity stress in the near term.</p></div><h4>Key Drivers</h4>${simpleList(["High expense volatility","+28% vs last month"],["Declining cash reserves","-15% vs last month"],["Inventory holding cost","+22% vs last month"])}</div></div><div class="grid-2"><div class="panel"><h3>Cash Flow Forecast (Next 90 Days)</h3>${chart("line")}<div class="alert-box">⚠ High probability of cash shortfall between Oct – Dec 2026</div></div><div class="panel"><h3>Top Recommendations</h3>${recommendationList(3)}</div></div><div class="assistant-bar"><div class="assistant-face">☻</div><div><b>QuantGuard AI Assistant</b><p class="muted">Ask me anything about your business risk.</p></div><button class="btn btn-primary">Ask</button></div>`,
  upload: () => `${pageHead("Upload Financial Data", "Provide accurate financial data to help our AI models generate precise insights and predictions.", false)}<div class="grid-main-side"><div><div class="data-tabs"><button class="data-tab active">${icon("▤")}<div><b>Upload File</b><br><span class="muted">Upload Excel or CSV file</span></div></button><button class="data-tab">${icon("▦")}<div><b>Manual Entry</b><br><span class="muted">Enter data manually</span></div></button><button class="data-tab">${icon("☁")}<div><b>Connect Integration</b><br><span class="muted">Connect accounting software</span></div></button></div><div class="panel"><div class="dropzone"><div><div class="icon-round" style="margin:0 auto 16px;color:var(--green)">☁</div><h3>Drag & drop your file here</h3><p>Supports .xlsx, .xls, .csv files up to 10MB</p><button class="btn btn-primary">Choose File</button></div></div><p style="text-align:center">◇ Your data is encrypted and secure. We never share your information.</p></div><div class="panel"><h3>What data should I upload?</h3>${sampleTable()}</div><div class="panel"><h3>Recent Uploads</h3>${uploadsTable()}</div></div><div><div class="panel"><h3 class="status-green">Data Requirements</h3>${checkList(["Revenue / Sales","Operating Expenses","Cost of Goods Sold (COGS)","Inventory (Stock Levels)","Debt / Loan Information","Cash & Bank Balances","Other Operating Income","Taxes (if applicable)"])}</div><div class="panel" style="margin-top:18px"><h3>Need Help?</h3>${simpleList(["Watch Tutorial","Learn how to prepare your data"],["Chat with Support","Get help from our team"],["Data Format Guide","Download our data preparation guide"])}</div></div></div>`,
  risk: () => `${pageHead("Risk Analysis", "Understand the key risk factors affecting your business.")}<div class="tabs-row">${["Overview","Liquidity Risk","Operational Risk","Financial Risk","External Risk","Risk Drivers"].map((x,i)=>`<button class="${i===0?"active":""}">${x}</button>`).join("")}</div><div class="grid-3"><div class="panel"><h3>Overall Risk Score</h3><div class="gauge"><strong>74</strong></div><p style="text-align:center" class="status-red">High Risk</p></div><div class="panel"><h3>Risk Trend</h3>${chart("risk")}</div><div class="panel"><h3>Stress Probability (90 Days)</h3><div class="donut" style="margin:auto;background:conic-gradient(var(--purple) 0 72%, #e8edf4 72% 100%)"><strong>72%</strong></div><p style="text-align:center" class="status-purple">High Probability</p></div></div><div class="grid-main-side"><div><div class="panel"><h3>Risk Breakdown</h3><p>Detailed view of key risk components and their impact on your business.</p>${riskTable()}</div><div class="panel" style="margin-top:18px"><h3>Risk Factor Details</h3><div class="grid-2"><div>${chart()}</div><div><h3>Impact on Business</h3><div class="gauge"><strong style="font-size:24px;color:var(--red)">High</strong></div><p>High and unpredictable expenses reduce profitability and increase liquidity risk.</p></div></div></div></div><div><div class="panel"><h3>Top Risk Drivers</h3>${simpleList(["High Expense Volatility","+28% vs last month"],["Low Cash Reserves","-15% vs last month"],["Inventory Holding Cost","+22% vs last month"])}</div><div class="panel" style="margin-top:18px"><h3>Risk Heatmap</h3>${heatmap()}</div><div class="panel" style="margin-top:18px"><h3>Recommendations</h3>${checkList(["Reduce expense volatility by negotiating better supplier terms.","Maintain at least 3 months of operating expenses in cash reserves.","Optimize inventory levels to reduce holding costs."])}</div></div></div>`,
  forecasting: () => `${pageHead("Forecasting", "AI-powered forecasts to help you stay ahead of financial stress.")}<div class="tabs-row">${["Cash Flow Forecast","Revenue Forecast","Expense Forecast","Risk Projection","Scenario Outlook"].map((x,i)=>`<button class="${i===0?"active":""}">${x}</button>`).join("")}</div>${kpiCards([["Projected Cash Balance (Aug 22)","₦1,240,000","","↑ 18.5% vs current balance","green","◌"],["Cash Shortfall Probability","32","%","Moderate Risk","purple","◈"],["Forecast Confidence","87","%","High","blue","◎"],["Danger Period","Oct – Dec 2026","","High stress expected","orange","⚠"],["Breakeven Point","₦2.8M"," / month","Revenue needed to stay safe","blue","◎"]])}<div class="grid-main-side"><div><div class="grid-2"><div class="panel"><h3>Cash Flow Forecast (Next 6 Months)</h3>${chart()}</div><div class="panel"><h3>Cash Balance Projection</h3>${chart("line")}</div></div><div class="grid-2"><div class="panel"><h3>Revenue Forecast</h3>${chart("line")}</div><div class="panel"><h3>Expense Forecast</h3>${chart("risk")}</div></div><div class="panel"><h3>Risk Projection (Next 6 Months)</h3>${chart("risk")}</div></div><div><div class="panel"><h3>Forecast Summary</h3>${checkList(["Seasonal revenue slowdown","Rising operating expenses","Higher inventory holding cost","Fuel price volatility"])}<div class="donut" style="margin:22px auto;background:conic-gradient(var(--orange) 0 32%, #e8edf4 32% 100%)"><strong>32%</strong></div><button class="btn btn-light" data-route="recommendations" style="width:100%">View Recommendations →</button></div><div class="panel" style="margin-top:18px"><h3>Scenario Quick View</h3>${simpleList(["Base Case (Current)","32%"],["Best Case","15%"],["Worst Case","68%"])}<button class="btn btn-primary" data-route="scenario" style="width:100%">Run Scenario Simulation →</button></div></div></div>`,
  recommendations: () => `${pageHead("AI Recommendations", "Smart, actionable steps to reduce risk and strengthen your business.")}${kpiCards([["Overall Risk Score","74","/100","High Risk","red","◇"],["Stress Probability (90 Days)","72","%","High Probability","purple","◈"],["Cash Shortfall Probability","32","%","Moderate Risk","orange","⚠"],["Forecast Confidence","89","%","High","green","◎"],["Break-even Point","₦2.8M"," / month","Revenue needed to stay safe","blue","◎"]])}<div class="grid-main-side"><div><div class="panel"><h3>Top AI Recommendations</h3><p>Personalized actions based on your risk profile and forecasts.</p>${recommendationList(5)}<button class="btn btn-light" style="width:280px;margin:18px auto 0;display:flex">View All Recommendations →</button></div><div class="panel" style="margin-top:18px"><h3>Action Plan (Next 90 Days)</h3><div class="action-plan">${["0 – 30 Days","31 – 60 Days","61 – 90 Days"].map((d,i)=>`<div class="timeline"><h4 class="${["status-green","status-orange","status-purple"][i]}">${d}</h4><ul><li>Build cash reserve buffer</li><li>Optimize inventory levels</li><li>Track daily cash flow</li></ul></div>`).join("")}</div></div></div><div><div class="panel"><h3>Why These Recommendations?</h3><div class="progress-list">${riskFactors.slice(0,5).map(r=>progress(r[0],r[2],r[6])).join("")}</div><button class="btn btn-light" data-route="risk" style="width:100%;margin-top:24px">View Detailed Risk Analysis →</button></div><div class="panel" style="margin-top:18px"><h3>Potential Impact If You Act</h3><div class="grid-3" style="grid-template-columns:repeat(3,1fr)"><div><b>Risk Score</b><h2>74 → 58</h2></div><div><b>Stress Probability</b><h2>72% → 45%</h2></div><div><b>Cash Shortfall Prob.</b><h2>32% → 15%</h2></div></div></div><div class="panel" style="margin-top:18px"><h3>AI Insight</h3><p>Your business shows high vulnerability to liquidity stress due to expense volatility and low cash reserves. Focus on cash preservation and inventory optimization for the next 90 days.</p><button class="btn btn-light" style="width:100%">Chat with AI Assistant →</button></div></div></div>`,
  scenario: () => `${pageHead("Scenario Simulation", "Model different situations and see how they impact your business risk.")}<div class="scenario-grid"><div><div class="panel"><h3>1 Choose Scenario Type</h3>${["Fuel Price Increase","Sales Drop","Take a Loan","Increase Inventory","Expense Increase","Custom Scenario"].map((x,i)=>`<div class="choice ${i===0?"active":""}"><span class="radio"></span><div><b>${x}</b><p class="muted">Simulate ${x.toLowerCase()}</p></div></div>`).join("")}</div><div class="panel" style="margin-top:18px"><h3>2 Adjust Variables</h3><div class="adjust">${["Fuel Price Increase","Sales / Revenue Change","Operating Expenses Change","Inventory Level Change","New Loan Amount","Loan Interest Rate"].map((x,i)=>`<div class="adjust-row"><label>${x}</label><input class="num" value="${[20,0,5,0,0,0][i]}"><span>${i===4?"₦":"%"}</span></div>`).join("")}</div><button class="btn btn-primary" style="width:100%;margin-top:18px">Run Simulation →</button></div></div><div><div class="panel"><h3>Scenario Impact Summary</h3>${kpiCards([["Risk Score","82","/100","Higher Risk","red","◇"],["Stress Probability (90 Days)","78","%","Higher Probability","purple","◈"],["Cash Shortfall Probability","58","%","Moderate Risk","orange","⚠"],["Forecast Confidence","78","%","Lower Confidence","green","◎"]])}</div><div class="panel" style="margin-top:18px"><h3>Financial Impact (Next 6 Months)</h3>${chart()}${scenarioTable()}</div><div class="panel" style="margin-top:18px"><h3>Scenario Comparison</h3>${comparisonTable()}</div></div><div><div class="panel"><h3>Scenario Details</h3>${simpleList(["Scenario Name","Fuel Price Increase +20%"],["Description","Impact of 20% increase in average fuel prices."],["Compared To","Baseline projection"])}</div><div class="panel" style="margin-top:18px"><h3>Key Insights</h3>${simpleList(["Cash balance declines","by ₦850K by Oct '26"],["High risk of cash shortfall","starting Nov '26"],["Operating expenses increase","by 18% on average"])}</div><div class="panel" style="margin-top:18px"><h3 class="status-green">AI Recommendation</h3>${checkList(["Optimize fuel routes and reduce wastage","Negotiate better fuel supply terms","Review pricing strategy to protect margins","Build cash reserves to cover 2–3 months of expenses"])}</div></div></div>`,
  reports: () => `${pageHead("Reports", "Comprehensive insights and analysis for better business decisions.", false)}<div class="tabs-row">${["Overview","Financial Reports","Risk Reports","Forecast Reports","Custom Reports"].map((x,i)=>`<button class="${i===0?"active":""}">${x}</button>`).join("")}</div><div class="grid-main-side"><div>${kpiCards([["Total Reports","24","","↑ 20% vs last 30 days","green","▤"],["Reports Generated","18","","↑ 12% vs last 30 days","blue","▣"],["Reports Viewed","36","","↑ 15% vs last 30 days","purple","◎"],["Downloads","12","","↑ 9% vs last 30 days","orange","⇩"]])}<div class="grid-2"><div class="panel"><h3>Reports Generated Over Time</h3>${chart("line")}</div><div class="panel"><h3>Reports by Category</h3><div class="donut-wrap"><div class="donut"><strong>24</strong></div>${simpleList(["Financial (10)","42%"],["Risk (6)","25%"],["Forecast (4)","17%"],["Custom (4)","16%"])}</div></div></div><div class="panel"><h3>All Reports</h3>${reportsTable()}</div></div><div><div class="panel"><h3>Quick Actions</h3>${simpleList(["Generate New Report","Create a custom report"],["Schedule Report","Automate report generation"],["Export Data","Export data in multiple formats"],["Report Templates","Use pre-built report templates"])}</div><div class="panel" style="margin-top:18px"><h3>Recently Generated Reports</h3>${simpleList(["Financial Performance Summary","Completed"],["Risk Assessment Report","Completed"],["Cash Flow Forecast Report","Completed"],["Scenario Analysis Report","Completed"],["Revenue Forecast Report","In Progress"])}</div><div class="panel" style="margin-top:18px"><h3>Top Insights This Period</h3>${checkList(["Revenue is projected to grow by 12.4% in Q3 2026.","Operating expenses increased by 8.7% in April 2026.","Cash reserves are sufficient to cover 2.8 months of expenses."])}</div></div></div>`,
  economic: () => `${pageHead("Economic Intelligence", "Global and local economic insights to inform smarter business decisions.")}${kpiCards([["Global Economic Outlook","Stable","","Growth projected at 3.1%","green","▣"],["Inflation (Global)","3.2","%","Moderate","purple","▤"],["Interest Rate Trend (US)","4.75","%","High","orange","▣"],["Exchange Rate (USD/NGN)","₦1,545.20","","↑ 2.3% vs last month","green","◎"],["Business Confidence (Nigeria)","62","/100","Positive","blue","◇"]])}<div class="grid-main-side"><div><div class="panel"><h3>Key Economic Indicators</h3>${chart("line")}</div><div class="grid-2"><div class="panel"><h3>Economic Calendar</h3>${simpleList(["May 29","US GDP Growth (Q1 Final)"],["May 30","Eurozone Inflation (May)"],["Jun 3","US Fed Interest Rate Decision"],["Jun 5","OPEC+ Meeting"])}</div><div class="panel"><h3>Regional Snapshot</h3>${kpiCards([["GDP Growth","2.7","%","Nigeria Q1 2026","green","↗"],["Inflation","22.4","%","April 2026","purple","⌁"]])}</div></div><div class="panel"><h3>Economic Impact on Your Business</h3><div class="grid-2">${simpleList(["Consumer Spending","Rising inflation may reduce discretionary spending."],["Operating Costs","Higher fuel prices could increase logistics costs."],["Supply Chain","Global supply chain improving, but local disruptions may persist."],["Revenue Outlook","Improving confidence supports positive revenue outlook."])}</div></div></div><div><div class="panel"><h3>Key Economic Highlights</h3>${simpleList(["Global Growth Holds Steady","Projected growth of 3.1% in 2026."],["Inflation Continues to Ease","Global inflation has fallen to 3.2%."],["Naira Under Moderate Pressure","NGN depreciated by 2.3% against USD."],["Business Confidence Improves","Nigeria confidence improved to 62/100."])}</div><div class="panel" style="margin-top:18px"><h3>Commodity Prices</h3>${commodityTable()}</div><div class="panel" style="margin-top:18px"><h3>AI Economic Insight</h3><p>Inflation is easing and business confidence is improving, creating a favorable environment for revenue growth. Focus on cost optimization and inventory efficiency to maximize profitability in the next 90 days.</p></div></div></div>`,
  settings: () => `${pageHead("Settings", "Manage your account, business, preferences and security settings.", false)}<div class="settings-grid"><div class="panel"><div class="settings-menu"><b>ACCOUNT SETTINGS</b><button class="active">♙ Profile & Account</button><button>▣ Business Information</button><button>♟ Users & Permissions</button><button>▤ Subscription & Billing</button><b>PREFERENCES</b><button>♧ Notifications</button><button>✉ Email Preferences</button><button>▦ Dashboard Preferences</button><button>◎ Regional & Currency</button><b>DATA & INTEGRATIONS</b><button>▥ Data Sources</button><button>✣ Integrations</button><button>&lt;/&gt; API Access</button><b>SECURITY</b><button>▣ Password & Security</button><button>◇ Two-Factor Authentication</button><button>◷ Login Activity</button><button>◈ Data Privacy</button></div></div><div><div class="panel"><div class="page-head"><div><h3>Profile & Account</h3><p>Manage your personal information and account details.</p></div><button class="btn btn-light">Edit Profile</button></div><div class="profile-row"><div class="big-avatar">DO</div><div><h2>Daniel Okafor <span class="badge green">Owner</span></h2><p>daniel.okafor@greenfieldstores.com</p><p>+234 801 234 5678</p></div><div>${simpleList(["Role","Business Owner"],["Account ID","QGAI-78234"],["Time Zone","(WAT) West Africa Time"],["Language","English"])}</div></div></div><div class="panel" style="margin-top:18px"><h3>Business Information</h3><div class="grid-2">${simpleList(["Business Name","GreenField Stores"],["Industry","Retail Trade"],["Business Type","Private Limited Company"],["Location","Lagos, Nigeria"],["Registration Number","RC 1234567"],["Business Email","info@greenfieldstores.com"])}</div></div><div class="panel" style="margin-top:18px"><h3>Subscription & Billing</h3><div class="grid-3"><div><b>Current Plan</b><h2>Pro Plan <span class="badge green">Active</span></h2></div><div>${checkList(["Advanced Analytics","Scenario Simulation","Custom Reports","API Access","Priority Support"])}</div><div><b>Amount</b><h2>₦95,000 <small>/ month</small></h2><button class="btn btn-light">Update</button></div></div></div><div class="grid-2" style="margin-top:18px"><div class="panel"><h3>Security</h3>${simpleList(["Password","Last changed 32 days ago"],["Two-Factor Authentication","Enabled"],["Login Activity","View recent login sessions"])}</div><div class="panel"><h3>Data & Privacy</h3>${simpleList(["Data Usage","View how your data is used"],["Data Export","Download your business data"],["Delete Account","Permanently delete your account"])}</div></div></div></div>`,
  alerts: () => `${pageHead("Alerts", "Recent warnings and risk events requiring attention.")}<div class="panel">${simpleList(["High Liquidity Risk","Stress probability above 70%"],["Expense Spike Detected","Operating expenses increased by 28%"],["Low Cash Reserve","Less than 3 months of expenses"],["Economic Update","Inflation rate increased to 24.3%"])}</div>`,
};

function riskMini() {
  return `<div class="list">${riskFactors.map(r=>`<div class="list-row"><span style="color:${r[6]}">●</span><b>${r[0]}</b><span>${r[2]} /100</span></div>`).join("")}</div>`;
}

function simpleList(...rows) {
  return `<div class="list">${rows.map(r=>`<div class="list-row"><span>${r[0].includes("High")||r[1]?.includes("High")?"⚠":"●"}</span><div><b>${r[0]}</b><p>${r[1]}</p></div><span>›</span></div>`).join("")}</div>`;
}

function checkList(items) {
  return `<div class="list">${items.map(x=>`<div class="list-row"><span class="status-green">✓</span><div><b>${x}</b></div></div>`).join("")}</div>`;
}

function sampleTable() {
  return `<table><thead><tr><th>Date</th><th>Revenue</th><th>Operating Expenses</th><th>COGS</th><th>Inventory</th><th>Debt</th><th>Cash Balance</th></tr></thead><tbody>${[
    ["2026-01","₦2,450,000","₦1,870,000","₦1,120,000","₦850,000","₦2,100,000","₦580,000"],
    ["2026-02","₦2,780,000","₦1,920,000","₦1,250,000","₦880,000","₦2,000,000","₦640,000"],
    ["2026-03","₦2,620,000","₦1,950,000","₦1,180,000","₦900,000","₦1,950,000","₦610,000"],
  ].map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}

function uploadsTable() {
  return `<table><thead><tr><th>File Name</th><th>Upload Date</th><th>Records</th><th>Status</th><th>Actions</th></tr></thead><tbody><tr><td>GreenField_Store_Financials_May2026.xlsx</td><td>May 20, 2026</td><td>24 months</td><td><span class="badge green">Processed</span></td><td>◎ 🗑</td></tr><tr><td>Q1_Financial_Records.csv</td><td>May 12, 2026</td><td>12 months</td><td><span class="badge green">Processed</span></td><td>◎ 🗑</td></tr></tbody></table>`;
}

function riskTable() {
  return `<table class="risk-table"><thead><tr><th>Risk Factor</th><th>Score</th><th>Impact</th><th>Trend</th><th>vs Last Month</th><th>Key Insight</th></tr></thead><tbody>${riskFactors.map(r=>`<tr><td><b>${r[0]}</b><br><span class="muted">${r[1]}</span></td><td class="status-${r[4]}"><b>${r[2]}</b> /100</td><td><span class="badge ${r[4]==="red"?"red":r[4]==="orange"?"orange":"green"}">${r[3]}</span></td><td>${spark(r[6])}</td><td>${r[5]}</td><td>Key driver requires active monitoring and corrective action.</td></tr>`).join("")}</tbody></table>`;
}

function recommendationList(limit) {
  return `<div class="list">${recommendations.slice(0,limit).map(r=>`<div class="list-row"><span class="iconbox">${r[4]}</span><div><b>${r[0]}</b><p>${r[1]}</p></div><div><span class="badge ${r[2]==="High"?"green":"orange"}">${r[2]}</span> <span class="badge ${r[3]==="High"?"red":r[3]==="Low"?"green":"orange"}">${r[3]}</span></div></div>`).join("")}</div>`;
}

function progress(label, value, color) {
  return `<div class="progress-row"><b>${label}</b><div class="bar"><span style="width:${value}%;background:${color}"></span></div><b>${value}/100</b></div>`;
}

function heatmap() {
  return `<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3px">${Array.from({length:25},(_,i)=>`<div style="height:42px;background:${["#96d6a9","#b7df84","#f4dc55","#ff9f4d","#ff4d4f"][Math.floor(i/5)]};opacity:${.55+(i%5)*.1};border-radius:4px"></div>`).join("")}</div>`;
}

function scenarioTable() {
  return `<table><thead><tr><th>Metric</th><th>May '26</th><th>Jun '26</th><th>Jul '26</th><th>Aug '26</th><th>Sep '26</th><th>Oct '26</th></tr></thead><tbody><tr><td>Cash Inflow</td><td>₦2.45M</td><td>₦2.60M</td><td>₦2.70M</td><td>₦2.65M</td><td>₦2.80M</td><td>₦2.90M</td></tr><tr><td>Cash Outflow</td><td>₦2.10M</td><td>₦2.40M</td><td>₦2.60M</td><td>₦2.80M</td><td>₦3.10M</td><td>₦3.60M</td></tr><tr><td>Net Cash Flow</td><td>₦350K</td><td>₦200K</td><td>₦100K</td><td class="status-red">-₦150K</td><td class="status-red">-₦300K</td><td class="status-red">-₦700K</td></tr></tbody></table>`;
}

function comparisonTable() {
  return `<table><thead><tr><th>Scenario</th><th>Risk Score</th><th>Stress Probability</th><th>Cash Shortfall Prob.</th><th>Cash Balance</th><th>Overall Impact</th></tr></thead><tbody><tr><td>Baseline</td><td>70</td><td>63%</td><td>32%</td><td>₦1.24M</td><td>–</td></tr><tr><td>Fuel Price +20%</td><td class="status-red">82</td><td class="status-red">78%</td><td class="status-red">58%</td><td class="status-red">₦390K</td><td><span class="badge red">High Negative</span></td></tr><tr><td>Sales Drop -30%</td><td class="status-red">85</td><td>84%</td><td>72%</td><td>-₦250K</td><td><span class="badge red">Very High Negative</span></td></tr></tbody></table>`;
}

function reportsTable() {
  return `<table><thead><tr><th>Report Name</th><th>Category</th><th>Generated On</th><th>Date Range</th><th>Format</th><th>Status</th><th>Actions</th></tr></thead><tbody>${["Financial Performance Summary","Risk Assessment Report","Cash Flow Forecast Report","Scenario Analysis Report","Revenue Forecast Report"].map((r,i)=>`<tr><td><b>${r}</b><br><span class="muted">${["Monthly financial performance analysis","Comprehensive risk analysis","6-month cash flow projection","Multiple scenario impact analysis","Revenue projection and trends"][i]}</span></td><td><span class="badge ${i===1?"red":i>1?"orange":"green"}">${["Financial","Risk","Forecast","Custom","Forecast"][i]}</span></td><td>May ${28-i}, 2026</td><td>May 1 – Oct 31, 2026</td><td>PDF</td><td><span class="badge ${i===4?"orange":"green"}">${i===4?"In Progress":"Completed"}</span></td><td>◎ ⇩ ⋮</td></tr>`).join("")}</tbody></table>`;
}

function commodityTable() {
  return `<table><thead><tr><th>Commodity</th><th>Price</th><th>vs Last Month</th><th>Trend</th></tr></thead><tbody>${[["Brent Crude Oil","$82.45 /bbl","↑ 4.6%"],["Natural Gas","$2.41 /MMBtu","↓ 6.2%"],["Gold","$2,345.10 /oz","↑ 1.8%"],["Copper","$9,512 /ton","↑ 3.1%"],["Wheat","$247.6 /MT","↓ 2.4%"]].map((r,i)=>`<tr><td>${r[0]}</td><td>${r[1]}</td><td class="${r[2].includes("↑")?"status-green":"status-red"}">${r[2]}</td><td>${spark(i===1||i===4?"#ff3d43":"#06b36f")}</td></tr>`).join("")}</tbody></table>`;
}

function bindRoutes() {
  document.querySelectorAll("[data-auth-mode]").forEach(el => {
    el.addEventListener("click", e => {
      e.preventDefault();
      authMode = el.dataset.authMode;
      auth();
    });
  });
  document.querySelectorAll("[data-route]").forEach(el => {
    el.addEventListener("click", e => {
      e.preventDefault();
      const route = el.dataset.route;
      if (route === "landing") landing();
      else if (route === "auth") auth();
      else shell(route);
      window.scrollTo(0, 0);
    });
  });
}

landing();
