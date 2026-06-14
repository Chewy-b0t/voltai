"""HTML templates for VoltAI."""

# ─── Landing Page ────────────────────────────────────────────────────
LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VoltAI — AI That Pays You</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0a0f;--card:#12121a;--border:#1e1e2e;--text:#e8e8f0;--dim:#6b7280;--orange:#f59e0b;--green:#22c55e;--blue:#3b82f6;--radius:12px}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{color:var(--orange);text-decoration:none}
.container{max-width:1100px;margin:0 auto;padding:0 24px}

/* Nav */
nav{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-bottom:1px solid var(--border)}
.logo{font-size:24px;font-weight:800;color:var(--orange)}
.logo span{color:var(--text)}
.nav-links{display:flex;gap:24px;align-items:center}
.nav-links a{color:var(--dim);font-size:14px;font-weight:500}
.nav-links a:hover{color:var(--text)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 24px;border-radius:8px;font-weight:600;font-size:14px;border:none;cursor:pointer;transition:all 0.2s}
.btn-primary{background:var(--orange);color:#000}
.btn-primary:hover{background:#d97706}
.btn-outline{background:transparent;color:var(--text);border:1px solid var(--border)}
.btn-outline:hover{border-color:var(--dim)}
.btn-lg{padding:14px 32px;font-size:16px}

/* Hero */
.hero{padding:80px 0 60px;text-align:center}
.hero h1{font-size:56px;font-weight:800;line-height:1.1;margin-bottom:20px;letter-spacing:-1px}
.hero h1 .highlight{background:linear-gradient(135deg,var(--orange),#ef4444);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:20px;color:var(--dim);max-width:600px;margin:0 auto 36px}
.hero-buttons{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}

/* How it works */
.how{padding:60px 0}
.section-title{text-align:center;font-size:32px;font-weight:700;margin-bottom:12px}
.section-sub{text-align:center;color:var(--dim);margin-bottom:48px;font-size:16px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:32px 24px;text-align:center}
.step-num{width:48px;height:48px;background:var(--orange);color:#000;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;margin-bottom:16px}
.step h3{font-size:18px;margin-bottom:8px}
.step p{color:var(--dim);font-size:14px}

/* Models */
.models-section{padding:60px 0}
.model-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.model-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px;text-align:center}
.model-card .name{font-size:15px;font-weight:600;margin-bottom:4px}
.model-card .size{color:var(--dim);font-size:13px}
.model-card .price{color:var(--green);font-size:13px;font-weight:500;margin-top:8px}

/* Pricing */
.pricing{padding:60px 0;text-align:center}
.price-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:40px;max-width:400px;margin:0 auto}
.price-big{font-size:48px;font-weight:800;color:var(--orange)}
.price-sub{color:var(--dim);margin-top:8px}
.price-features{text-align:left;margin:24px 0;list-style:none}
.price-features li{padding:8px 0;border-bottom:1px solid var(--border);font-size:14px;color:var(--dim)}
.price-features li::before{content:"✓ ";color:var(--green);font-weight:700}

/* Code example */
.code-section{padding:60px 0}
.code-block{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;font-family:'SF Mono',monospace;font-size:13px;overflow-x:auto;color:var(--dim);line-height:1.8}
.code-block .kw{color:var(--orange)}
.code-block .str{color:var(--green)}
.code-block .cmt{color:#4b5563}

/* Footer */
footer{padding:40px 0;border-top:1px solid var(--border);text-align:center;color:var(--dim);font-size:13px}

@media(max-width:768px){
  .hero h1{font-size:36px}
  .steps{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="container">
<nav>
  <div class="logo">Volt<span>AI</span></div>
  <div class="nav-links">
    <a href="#how">How it works</a>
    <a href="#models">Models</a>
    <a href="#pricing">Pricing</a>
    <a href="/login" class="btn btn-outline">Log in</a>
    <a href="/signup" class="btn btn-primary">Get started free</a>
  </div>
</nav>

<div class="hero">
  <h1>AI inference<br><span class="highlight">paid in Bitcoin</span></h1>
  <p>Use open-source AI models. Pay with Lightning. No account needed. No credit card. No nonsense.</p>
  <div class="hero-buttons">
    <a href="/signup" class="btn btn-primary btn-lg">Start for free &rarr;</a>
    <a href="#how" class="btn btn-outline btn-lg">Learn more</a>
  </div>
</div>

<div class="how" id="how">
  <div class="section-title">How it works</div>
  <div class="section-sub">Three steps. No forms. No waiting.</div>
  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <h3>Create account</h3>
      <p>Pick a username and password. That's it. No email required.</p>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <h3>Add credits</h3>
      <p>Pay a Lightning invoice from any wallet. Credits appear instantly.</p>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <h3>Use the API</h3>
      <p>Standard OpenAI-compatible API. Works with any tool or library.</p>
    </div>
  </div>
</div>

<div class="models-section" id="models">
  <div class="section-title">Available Models</div>
  <div class="section-sub">Run on RTX 4070 Ti SUPER — fast inference, fair prices.</div>
  <div class="model-grid">
    <div class="model-card"><div class="name">Qwen 3.5 4B</div><div class="size">3 GB VRAM</div><div class="price">20 sats/M</div></div>
    <div class="model-card"><div class="name">Qwen 2.5 7B</div><div class="size">5 GB VRAM</div><div class="price">30 sats/M</div></div>
    <div class="model-card"><div class="name">DeepSeek R1 8B</div><div class="size">5 GB VRAM</div><div class="price">30 sats/M</div></div>
    <div class="model-card"><div class="name">Qwen 2.5 Coder 7B</div><div class="size">5 GB VRAM</div><div class="price">30 sats/M</div></div>
    <div class="model-card"><div class="name">Qwen 3.5 9B</div><div class="size">7 GB VRAM</div><div class="price">40 sats/M</div></div>
    <div class="model-card"><div class="name">Qwen 2.5 14B</div><div class="size">10 GB VRAM</div><div class="price">50 sats/M</div></div>
    <div class="model-card"><div class="name">Qwen 3.6 27B</div><div class="size">17 GB VRAM</div><div class="price">80 sats/M</div></div>
  </div>
</div>

<div class="pricing" id="pricing">
  <div class="section-title">Simple pricing</div>
  <div class="section-sub">Pay only for what you use. No subscriptions.</div>
  <div class="price-card">
    <div class="price-big">50 sats</div>
    <div class="price-sub">per 1 million tokens</div>
    <ul class="price-features">
      <li>10,000 free tokens on signup</li>
      <li>Pay with any Lightning wallet</li>
      <li>Sats go directly to the provider</li>
      <li>No middleman fees</li>
      <li>Credits never expire</li>
    </ul>
    <a href="/signup" class="btn btn-primary btn-lg" style="width:100%;justify-content:center">Get started free</a>
  </div>
</div>

<div class="code-section">
  <div class="section-title">Works with everything</div>
  <div class="section-sub">Standard OpenAI-compatible API. Drop-in replacement.</div>
  <div class="code-block">
<span class="cmt"># Python (openai library)</span>
<span class="kw">from</span> openai <span class="kw">import</span> OpenAI
client = OpenAI(<span class="str">base_url="https://your-url/v1"</span>, <span class="str">api_key="sk-..."</span>)
response = client.chat.completions.create(
    <span class="str">model="qwen2.5:14b"</span>,
    messages=[{<span class="str">"role"</span>: <span class="str">"user"</span>, <span class="str">"content"</span>: <span class="str">"Hello!"</span>}]
)

<span class="cmt"># curl</span>
curl <span class="kw">-H</span> <span class="str">"Authorization: Bearer sk-..."</span> \\
     https://your-url/v1/chat/completions \\
     <span class="kw">-d</span> <span class="str">'{"model":"qwen2.5:14b","messages":[{"role":"user","content":"Hello"}]}'</span>
  </div>
</div>

<footer>
  <p>VoltAI &mdash; Open-source AI inference, paid in Bitcoin.</p>
  <p style="margin-top:8px">No tracking. No ads. No middleman. Just compute for sats.</p>
</footer>
</div>
</body>
</html>"""

# ─── Login ───────────────────────────────────────────────────────────
LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Log in — VoltAI</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,sans-serif;background:#0a0a0f;color:#e8e8f0;display:flex;align-items:center;justify-content:center;min-height:100vh}
.card{background:#12121a;border:1px solid #1e1e2e;border-radius:12px;padding:40px;width:100%;max-width:400px;margin:20px}
h1{font-size:24px;margin-bottom:4px}
.sub{color:#6b7280;font-size:14px;margin-bottom:24px}
label{display:block;font-size:13px;color:#9ca3af;margin-bottom:6px}
input{width:100%;padding:10px 14px;background:#0a0a0f;border:1px solid #1e1e2e;border-radius:8px;color:#e8e8f0;font-size:14px;margin-bottom:16px}
input:focus{outline:none;border-color:#f59e0b}
.btn{width:100%;padding:12px;background:#f59e0b;color:#000;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}
.btn:hover{background:#d97706}
.error{background:#1a0a0a;border:1px solid #ef4444;border-radius:8px;padding:10px;color:#fca5a5;font-size:13px;margin-bottom:16px;display:none}
.footer{text-align:center;margin-top:20px;font-size:13px;color:#6b7280}
.footer a{color:#f59e0b}
</style>
</head>
<body>
<div class="card">
  <h1>Welcome back</h1>
  <p class="sub">Log in to your VoltAI account</p>
  <div class="error" id="error"></div>
  <form id="form">
    <label>Username</label>
    <input name="username" required autofocus>
    <label>Password</label>
    <input name="password" type="password" required>
    <button class="btn" type="submit">Log in</button>
  </form>
  <div class="footer">Don't have an account? <a href="/signup">Sign up free</a></div>
</div>
<script>
document.getElementById('form').onsubmit=async e=>{
  e.preventDefault();
  const fd=new FormData(e.target);
  try{
    const r=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({username:fd.get('username'),password:fd.get('password')})});
    const d=await r.json();
    if(r.ok)location.href=d.redirect;
    else{document.getElementById('error').textContent=d.detail||'Login failed';document.getElementById('error').style.display='block';}
  }catch(e){document.getElementById('error').textContent='Network error';document.getElementById('error').style.display='block';}
};
</script>
</body>
</html>"""

# ─── Signup ──────────────────────────────────────────────────────────
SIGNUP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sign up — VoltAI</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,sans-serif;background:#0a0a0f;color:#e8e8f0;display:flex;align-items:center;justify-content:center;min-height:100vh}
.card{background:#12121a;border:1px solid #1e1e2e;border-radius:12px;padding:40px;width:100%;max-width:400px;margin:20px}
h1{font-size:24px;margin-bottom:4px}
.sub{color:#6b7280;font-size:14px;margin-bottom:24px}
label{display:block;font-size:13px;color:#9ca3af;margin-bottom:6px}
input{width:100%;padding:10px 14px;background:#0a0a0f;border:1px solid #1e1e2e;border-radius:8px;color:#e8e8f0;font-size:14px;margin-bottom:16px}
input:focus{outline:none;border-color:#f59e0b}
.btn{width:100%;padding:12px;background:#22c55e;color:#000;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}
.btn:hover{background:#16a34a}
.error{background:#1a0a0a;border:1px solid #ef4444;border-radius:8px;padding:10px;color:#fca5a5;font-size:13px;margin-bottom:16px;display:none}
.footer{text-align:center;margin-top:20px;font-size:13px;color:#6b7280}
.footer a{color:#f59e0b}
.bonus{background:#0a1a0a;border:1px solid #22c55e44;border-radius:8px;padding:12px;color:#86efac;font-size:13px;margin-bottom:20px;text-align:center}
</style>
</head>
<body>
<div class="card">
  <h1>Create account</h1>
  <p class="sub">Get 10,000 free tokens. No email needed.</p>
  <div class="bonus">Free tier included: 10,000 tokens to try any model</div>
  <div class="error" id="error"></div>
  <form id="form">
    <label>Username</label>
    <input name="username" required minlength="3" placeholder="Pick a username" autofocus>
    <label>Password</label>
    <input name="password" type="password" required minlength="6" placeholder="At least 6 characters">
    <label>Email (optional)</label>
    <input name="email" type="email" placeholder="For recovery only">
    <button class="btn" type="submit">Create account &amp; start free</button>
  </form>
  <div class="footer">Already have an account? <a href="/login">Log in</a></div>
</div>
<script>
document.getElementById('form').onsubmit=async e=>{
  e.preventDefault();
  const fd=new FormData(e.target);
  try{
    const r=await fetch('/api/auth/signup',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({username:fd.get('username'),password:fd.get('password'),email:fd.get('email')})});
    const d=await r.json();
    if(r.ok||r.redirected)location.href='/app';
    else{document.getElementById('error').textContent=d.detail||'Signup failed';document.getElementById('error').style.display='block';}
  }catch(e){document.getElementById('error').textContent='Network error';document.getElementById('error').style.display='block';}
};
</script>
</body>
</html>"""

# ─── App Dashboard ───────────────────────────────────────────────────
APP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VoltAI — Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0a0f;--card:#12121a;--border:#1e1e2e;--text:#e8e8f0;--dim:#6b7280;--orange:#f59e0b;--green:#22c55e;--blue:#3b82f6;--red:#ef4444;--radius:12px}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
a{color:var(--orange);text-decoration:none}

/* Sidebar */
.sidebar{position:fixed;left:0;top:0;bottom:0;width:220px;background:#0d0d14;border-right:1px solid var(--border);padding:20px 0;z-index:10}
.sidebar .logo{font-size:22px;font-weight:800;color:var(--orange);padding:0 20px 24px;border-bottom:1px solid var(--border)}
.sidebar .logo span{color:var(--text)}
.sidebar nav{padding:16px 0}
.sidebar nav a{display:flex;align-items:center;gap:10px;padding:10px 20px;color:var(--dim);font-size:13px;font-weight:500;transition:all .15s}
.sidebar nav a:hover,.sidebar nav a.active{color:var(--text);background:rgba(245,158,11,.06)}
.sidebar nav a.active{border-right:2px solid var(--orange)}
.sidebar .user-box{position:absolute;bottom:0;left:0;right:0;padding:16px 20px;border-top:1px solid var(--border);font-size:13px}
.sidebar .user-box .uname{color:var(--text);font-weight:600}
.sidebar .user-box .ulink{color:var(--dim);font-size:12px;margin-top:4px;display:block}

/* Main */
.main{margin-left:220px;padding:24px 32px}
.page-title{font-size:15px;font-weight:700;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.page-title .dot{width:8px;height:8px;border-radius:50%;background:var(--green)}

/* Grid */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.card h2{font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.8px;margin-bottom:14px;font-weight:600}
.big-num{font-size:36px;font-weight:800;letter-spacing:-1px}
.stat{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--border);font-size:13px}
.stat:last-child{border:none}
.sl{color:var(--dim)}.sv{font-weight:600}
.fw{grid-column:1/-1}
.three{grid-template-columns:1fr 1fr 1fr}

/* Buttons */
.btn{padding:8px 16px;border-radius:6px;font-weight:600;font-size:12px;border:none;cursor:pointer;transition:all .15s}
.bp{background:var(--orange);color:#000}.bp:hover{background:#d97706}
.bg{background:var(--green);color:#000}
.bo{background:transparent;color:var(--text);border:1px solid var(--border)}.bo:hover{border-color:var(--dim)}
.bd{background:var(--red);color:#fff;font-size:11px;padding:4px 8px}

/* Inputs */
input,select{background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-size:13px;width:100%}
input:focus{outline:none;border-color:var(--orange)}

/* Tables */
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--border)}
th{color:var(--dim);font-size:11px;text-transform:uppercase;font-weight:600}

/* Key box */
.key-box{background:#0a0a0f;border:1px solid var(--green);border-radius:8px;padding:14px;font-family:monospace;word-break:break-all;margin:10px 0}

/* Invoice box */
.inv-box{background:#0a0a0f;border:1px solid var(--blue);border-radius:8px;padding:16px;margin-top:12px}

/* Badges */
.ok{color:var(--green)}.err{color:var(--red)}.warn{color:var(--orange)}
.badge{display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600}
.bg-g{background:#0a1a0a;color:var(--green);border:1px solid #22c55e33}
.bg-r{background:#1a0a0a;color:var(--red);border:1px solid #ef444433}
.bg-o{background:#1a1a0a;color:var(--orange);border:1px solid #f59e0b33}
.bg-b{background:#0a0a1a;color:var(--blue);border:1px solid #3b82f633}

/* Chart */
.chart{height:100px;display:flex;align-items:flex-end;gap:3px;margin-top:12px}
.bar{background:linear-gradient(180deg,var(--orange),#d97706);border-radius:3px 3px 0 0;min-width:16px;flex:1;position:relative;opacity:.85}
.bar:hover{opacity:1}
.bar-label{position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--dim);white-space:nowrap}

/* Model cards */
.model-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.model-card{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px;text-align:center}
.model-card .mname{font-size:13px;font-weight:600;margin-bottom:4px}
.model-card .msize{color:var(--dim);font-size:11px}
.model-card .mprice{color:var(--green);font-size:12px;font-weight:600;margin-top:6px}

/* Error console */
.err-row{padding:10px 12px;border-bottom:1px solid var(--border);font-size:12px}
.err-row:last-child{border:none}
.err-head{display:flex;gap:8px;align-items:center;margin-bottom:4px}

/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:20px;border-bottom:1px solid var(--border)}
.tab{padding:10px 18px;font-size:13px;font-weight:500;color:var(--dim);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s}
.tab:hover{color:var(--text)}
.tab.active{color:var(--orange);border-bottom-color:var(--orange)}

@media(max-width:768px){.sidebar{display:none}.main{margin-left:0}.grid,.three{grid-template-columns:1fr}}
</style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
  <div class="logo">Volt<span>AI</span></div>
  <nav>
    <a href="#" class="active" onclick="showTab('overview',this)">&#9673; Overview</a>
    <a href="#" onclick="showTab('keys',this)">&#9881; API Keys</a>
    <a href="#" onclick="showTab('wallet',this)">&#9883; Wallet</a>
    <a href="#" onclick="showTab('models',this)">&#9881; Models</a>
    <a href="#" onclick="showTab('usage',this)">&#9879; Usage</a>
    <a href="#" onclick="showTab('errors',this)">&#9888; Errors</a>
    <a href="#" onclick="showTab('settings',this)">&#9881; Settings</a>
  </nav>
  <div class="user-box">
    <div class="uname" id="user-display">—</div>
    <a class="ulink" href="/api/auth/logout">Log out</a>
  </div>
</div>

<!-- Main -->
<div class="main">

<!-- OVERVIEW TAB -->
<div id="tab-overview">
  <div class="page-title"><span class="dot"></span> Dashboard</div>

  <!-- Top stats row -->
  <div class="grid three">
    <div class="card">
      <h2>Balance</h2>
      <div class="big-num" id="credits" style="color:var(--green)">—</div>
      <div style="color:var(--dim);font-size:12px;margin-top:2px">sats available</div>
    </div>
    <div class="card">
      <h2>Today</h2>
      <div class="big-num" id="today" style="color:var(--orange)">—</div>
      <div style="color:var(--dim);font-size:12px;margin-top:2px">tokens used</div>
    </div>
    <div class="card">
      <h2>All Time</h2>
      <div class="big-num" id="used" style="color:var(--blue)">—</div>
      <div style="color:var(--dim);font-size:12px;margin-top:2px">tokens used</div>
    </div>
  </div>

  <!-- Gateway + Models -->
  <div class="grid">
    <div class="card">
      <h2>Gateway Status</h2>
      <div class="stat"><span class="sl">Status</span><span class="sv ok">Connected</span></div>
      <div class="stat"><span class="sl">Endpoint</span><span class="sv" style="font-size:12px;font-family:monospace">localhost:11434</span></div>
      <div class="stat"><span class="sl">Models</span><span class="sv" id="gw-models">—</span></div>
      <div class="stat"><span class="sl">Uptime</span><span class="sv ok">Active</span></div>
    </div>
    <div class="card">
      <h2>Available Models</h2>
      <div class="model-grid" id="model-list"></div>
    </div>
  </div>

  <!-- Quick actions -->
  <div class="card fw">
    <h2>Quick Start</h2>
    <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
      <div style="flex:1;min-width:200px">
        <div style="font-size:13px;line-height:2;color:var(--dim)">
          <div style="color:var(--text)"><strong>1.</strong> Copy your API key from the Keys tab</div>
          <div style="color:var(--text)"><strong>2.</strong> Add sats via Lightning in the Wallet tab</div>
          <div style="color:var(--text)"><strong>3.</strong> Use the OpenAI-compatible API</div>
        </div>
      </div>
      <div style="flex:1;min-width:280px;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px;font-size:12px;font-family:monospace;color:var(--dim);line-height:1.8">
        <div style="color:var(--dim);font-size:11px;margin-bottom:6px">EXAMPLE — Python</div>
        <span style="color:#c084fc">from</span> openai <span style="color:#c084fc">import</span> OpenAI<br>
        client = OpenAI(<span style="color:var(--green)">base_url="https://your-url/v1"</span>,<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--green)">api_key="sk-..."</span>)<br>
        resp = client.chat.completions.create(<br>
        &nbsp;&nbsp;<span style="color:var(--green)">model="qwen2.5:14b"</span>,<br>
        &nbsp;&nbsp;messages=[{<span style="color:var(--green)">"role"</span>:<span style="color:var(--green)">"user"</span>,<span style="color:var(--green)">"content"</span>:<span style="color:var(--green)">"Hi"</span>}])
      </div>
    </div>
  </div>
</div>

<!-- KEYS TAB -->
<div id="tab-keys" style="display:none">
  <div class="page-title"><span class="dot"></span> API Keys</div>
  <div class="card fw">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <h2 style="margin:0">Your Keys</h2>
      <button class="btn bp" onclick="showNewKey()">+ New Key</button>
    </div>
    <div id="new-key-form" style="display:none;margin-bottom:12px">
      <div style="display:flex;gap:8px;max-width:300px">
        <input id="key-name" placeholder="Key name (optional)">
        <button class="btn bp" onclick="createKey()">Create</button>
      </div>
    </div>
    <div id="new-key-display" style="display:none"></div>
    <table>
      <thead><tr><th>Key</th><th>Name</th><th>Balance</th><th>Used</th><th>Last used</th><th></th></tr></thead>
      <tbody id="keys-table"></tbody>
    </table>
  </div>
</div>

<!-- WALLET TAB -->
<div id="tab-wallet" style="display:none">
  <div class="page-title"><span class="dot"></span> Wallet</div>
  <div class="grid">
    <div class="card">
      <h2>Buy Credits</h2>
      <p style="font-size:13px;color:var(--dim);margin-bottom:14px">Pay a Lightning invoice. Sats go directly to the GPU provider.</p>
      <div style="margin-bottom:12px">
        <label style="font-size:12px;color:var(--dim);display:block;margin-bottom:4px">Select key</label>
        <select id="buy-key"><option value="">Select key...</option></select>
      </div>
      <div style="margin-bottom:14px">
        <label style="font-size:12px;color:var(--dim);display:block;margin-bottom:4px">Amount</label>
        <select id="buy-amount">
          <option value="100">100 sats (~2M tokens)</option>
          <option value="500">500 sats (~10M tokens)</option>
          <option value="1000">1,000 sats (~20M tokens)</option>
          <option value="5000">5,000 sats (~100M tokens)</option>
        </select>
      </div>
      <button class="btn bp" onclick="buyCredits()" style="width:100%;justify-content:center">Pay with Lightning</button>
      <div id="invoice-area"></div>
    </div>
    <div class="card">
      <h2>Payment Info</h2>
      <div class="stat"><span class="sl">Payout address</span><span class="sv" style="font-size:12px">postalzombie921@minibits.cash</span></div>
      <div class="stat"><span class="sl">Rate</span><span class="sv">50 sats / 1M tokens</span></div>
      <div class="stat"><span class="sl">Network</span><span class="sv ok">Bitcoin Lightning</span></div>
      <div class="stat"><span class="sl">Min top-up</span><span class="sv">100 sats</span></div>
    </div>
  </div>
</div>

<!-- MODELS TAB -->
<div id="tab-models" style="display:none">
  <div class="page-title"><span class="dot"></span> Models</div>
  <div class="card fw">
    <h2>Installed Models</h2>
    <p style="font-size:13px;color:var(--dim);margin-bottom:14px">Models loaded on the local Ollama instance.</p>
    <div class="model-grid" id="model-grid"></div>
  </div>
</div>

<!-- USAGE TAB -->
<div id="tab-usage" style="display:none">
  <div class="page-title"><span class="dot"></span> Usage</div>
  <div class="card fw">
    <h2>Usage (7 days)</h2>
    <div class="chart" id="chart"></div>
    <div style="height:20px"></div>
    <table>
      <thead><tr><th>Date</th><th>Requests</th><th>Tokens</th><th>Cost (sats)</th></tr></thead>
      <tbody id="usage-table"></tbody>
    </table>
  </div>
</div>

<!-- ERRORS TAB -->
<div id="tab-errors" style="display:none">
  <div class="page-title"><span class="dot"></span> Error Console</div>
  <div class="card fw">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <div style="display:flex;gap:8px;align-items:center">
        <h2 style="margin:0">Recent Errors</h2>
        <span id="error-count" class="badge bg-r">0</span>
      </div>
      <button class="btn bo" onclick="clearErrors()">Clear all</button>
    </div>
    <div id="error-console" style="max-height:500px;overflow-y:auto">
      <div style="color:var(--dim);font-size:13px;padding:30px;text-align:center">No errors logged</div>
    </div>
  </div>
</div>

<!-- SETTINGS TAB -->
<div id="tab-settings" style="display:none">
  <div class="page-title"><span class="dot"></span> Settings</div>
  <div class="grid">
    <div class="card">
      <h2>Account</h2>
      <div class="stat"><span class="sl">Username</span><span class="sv" id="set-user">—</span></div>
      <div class="stat"><span class="sl">User ID</span><span class="sv" id="set-uid" style="font-size:11px;font-family:monospace">—</span></div>
      <div class="stat"><span class="sl">Joined</span><span class="sv" id="set-joined">—</span></div>
    </div>
    <div class="card">
      <h2>Service Info</h2>
      <div class="stat"><span class="sl">API</span><span class="sv ok">OpenAI-compatible</span></div>
      <div class="stat"><span class="sl">Proxy</span><span class="sv">Ollama (local)</span></div>
      <div class="stat"><span class="sl">Pricing</span><span class="sv">50 sats / 1M tokens</span></div>
      <div class="stat"><span class="sl">Free tier</span><span class="sv">10,000 tokens</span></div>
    </div>
  </div>
</div>

</div><!-- /main -->

<script>
let data={};
const models=['qwen3.5:4b','qwen2.5:7b','deepseek-r1:8b','qwen2.5-coder:7b','qwen3.5:9b','qwen2.5:14b','qwen3.6:27b'];
const modelInfo={
  'qwen3.5:4b':{size:'3 GB',price:'20 sats/M'},
  'qwen2.5:7b':{size:'5 GB',price:'30 sats/M'},
  'deepseek-r1:8b':{size:'5 GB',price:'30 sats/M'},
  'qwen2.5-coder:7b':{size:'5 GB',price:'30 sats/M'},
  'qwen3.5:9b':{size:'7 GB',price:'40 sats/M'},
  'qwen2.5:14b':{size:'10 GB',price:'50 sats/M'},
  'qwen3.6:27b':{size:'17 GB',price:'80 sats/M'}
};

function showTab(name,el){
  document.querySelectorAll('[id^="tab-"]').forEach(t=>t.style.display='none');
  document.getElementById('tab-'+name).style.display='';
  document.querySelectorAll('.sidebar nav a').forEach(a=>a.classList.remove('active'));
  if(el)el.classList.add('active');
  else document.querySelector('.sidebar nav a[onclick*="'+name+'"]').classList.add('active');
}

async function load(){
  try{
    data=await(await fetch('/api/me')).json();
    render();
  }catch(e){}
}

function render(){
  document.getElementById('user-display').textContent=data.user.username;
  document.getElementById('credits').textContent=data.stats.total_credits.toLocaleString()+' sats';
  document.getElementById('used').textContent=data.stats.total_used.toLocaleString();
  document.getElementById('today').textContent=data.stats.today_tokens.toLocaleString();
  document.getElementById('gw-models').textContent=models.length+' models';
  document.getElementById('set-user').textContent=data.user.username;
  document.getElementById('set-uid').textContent='id:'+data.user.id;

  // Model lists
  const ml=models.map(m=>{
    const info=modelInfo[m]||{size:'—',price:'—'};
    return '<div class="model-card"><div class="mname">'+m+'</div><div class="msize">'+info.size+' VRAM</div><div class="mprice">'+info.price+'</div></div>';
  }).join('');
  document.getElementById('model-list').innerHTML=ml;
  document.getElementById('model-grid').innerHTML=ml;

  // Keys
  const kt=document.getElementById('keys-table');
  const sl=document.getElementById('buy-key');
  if(data.keys.length){
    kt.innerHTML=data.keys.map(k=>'<tr><td><code style="font-size:12px">'+k.key_prefix+'</code></td><td>'+k.name+'</td><td class="'+(k.credits>0?'ok':'err')+'">'+k.credits.toLocaleString()+' sats</td><td>'+k.total_used.toLocaleString()+'</td><td>'+(k.last_used||'Never')+'</td><td><button class="btn bd" onclick="delKey('+k.id+')">Delete</button></td></tr>').join('');
    sl.innerHTML='<option value="">Select key...</option>'+data.keys.map(k=>'<option value="'+k.id+'">'+k.key_prefix+' ('+k.credits+' sats)</option>').join('');
  }else{
    kt.innerHTML='<tr><td colspan="6" style="text-align:center;color:var(--dim)">No keys yet — create one to get started</td></tr>';
  }

  // Usage
  const ut=document.getElementById('usage-table');
  if(data.usage_7d.length){
    ut.innerHTML=data.usage_7d.map(u=>'<tr><td>'+u.date+'</td><td>'+u.requests+'</td><td>'+u.tokens.toLocaleString()+'</td><td>'+u.sats+'</td></tr>').join('');
    renderChart(data.usage_7d);
  }
}

function renderChart(usage){
  const c=document.getElementById('chart');
  if(!usage.length){c.innerHTML='<div style="color:var(--dim);font-size:13px;padding:20px;text-align:center">No usage yet</div>';return;}
  const max=Math.max(...usage.map(u=>u.tokens),1);
  c.innerHTML=usage.map(u=>{
    const h=Math.max(4,(u.tokens/max)*100);
    return '<div class="bar" style="height:'+h+'%" title="'+u.tokens.toLocaleString()+' tokens"><div class="bar-label">'+u.date.slice(5)+'</div></div>';
  }).join('');
}

function showNewKey(){document.getElementById('new-key-form').style.display='';document.getElementById('key-name').focus();}

async function createKey(){
  const name=document.getElementById('key-name').value||'Default';
  const r=await(await fetch('/api/keys',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})})).json();
  document.getElementById('new-key-form').style.display='none';
  document.getElementById('new-key-display').style.display='block';
  document.getElementById('new-key-display').innerHTML='<div class="key-box"><div style="color:var(--green);font-weight:600;margin-bottom:4px">Key created!</div><div style="font-size:15px;margin-bottom:6px">'+r.key+'</div><div style="color:var(--dim);font-size:11px">Copy this now. It won\'t be shown again.</div></div>';
  document.getElementById('key-name').value='';
  load();
}

async function delKey(id){if(!confirm('Delete this key?'))return;await fetch('/api/keys/'+id,{method:'DELETE'});load();}

async function buyCredits(){
  const kid=document.getElementById('buy-key').value;
  const sats=parseInt(document.getElementById('buy-amount').value);
  if(!kid){alert('Select a key first');return;}
  const r=await fetch('/api/buy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key_id:parseInt(kid),amount_sats:sats})});
  const d=await r.json();
  if(!r.ok){alert(d.detail||'Error');return;}
  document.getElementById('invoice-area').innerHTML='<div class="inv-box"><div style="font-weight:600;color:var(--blue);margin-bottom:8px">Lightning Invoice — '+d.amount_sats+' sats</div><div style="font-size:13px;margin-bottom:6px">Tokens: <strong>'+d.tokens.toLocaleString()+'</strong></div><div style="font-size:13px;margin-bottom:8px;color:var(--dim)">Pay to: <strong style="color:var(--text)">'+(d.ln_address||'Minibits wallet')+'</strong></div><div style="background:#0a0a0f;padding:12px;border-radius:6px;font-family:monospace;font-size:11px;word-break:break-all;margin:10px 0">'+d.invoice+'</div><div style="display:flex;gap:8px"><button class="btn bp" onclick="copyInv(this,\''+d.invoice+'\')">Copy invoice</button><button class="btn bo" onclick="checkPay(\''+d.payment_hash+'\')">I\'ve paid</button></div><div id="pay-status" style="margin-top:10px;font-size:13px;color:var(--dim)">Waiting for payment...</div></div>';
  pollPayment(d.payment_hash);
}

function copyInv(btn,inv){navigator.clipboard.writeText(inv);btn.textContent='Copied!';setTimeout(()=>{btn.textContent='Copy invoice';},1500);}

let pollTimer=null;
function pollPayment(hash){
  if(pollTimer)clearInterval(pollTimer);
  pollTimer=setInterval(async()=>{
    try{
      const r=await(await fetch('/api/invoice/'+hash+'/status')).json();
      if(r.status==='paid'){
        clearInterval(pollTimer);
        document.getElementById('pay-status').innerHTML='<span class="ok" style="font-weight:600">Payment received! Credits added.</span>';
        load();
      }
    }catch(e){}
  },3000);
}

async function checkPay(hash){
  const r=await(await fetch('/api/invoice/'+hash+'/status')).json();
  const el=document.getElementById('pay-status');
  if(r.status==='paid'){if(pollTimer)clearInterval(pollTimer);el.innerHTML='<span class="ok" style="font-weight:600">Paid! Credits added.</span>';load();}
  else{el.textContent='Still waiting... try again in a moment.';}
}

async function loadErrors(){
  try{
    const r=await fetch('/api/errors?limit=50');
    if(!r.ok)return;
    const d=await r.json();
    const el=document.getElementById('error-console');
    const count=document.getElementById('error-count');
    if(!d.errors.length){
      el.innerHTML='<div style="color:var(--dim);font-size:13px;padding:30px;text-align:center">No errors logged</div>';
      count.textContent='0';
      return;
    }
    count.textContent=d.errors.length;
    el.innerHTML=d.errors.map(e=>'<div class="err-row"><div class="err-head"><span class="badge '+(e.status_code>=500?'bg-r':e.status_code>=400?'bg-o':'bg-g')+'">'+(e.status_code||'?')+'</span><span style="color:var(--orange);font-weight:500">'+(e.method||'?')+'</span><span style="color:var(--dim)">'+(e.endpoint||'?')+'</span></div><div style="color:var(--text)">'+(e.error_msg||'Unknown error')+'</div><div style="color:var(--dim);margin-top:4px">'+e.created_at+(e.ip_address?' from '+e.ip_address:'')+'</div></div>').join('');
  }catch(e){}
}

async function clearErrors(){await fetch('/api/errors',{method:'DELETE'});loadErrors();}

load();
setInterval(load,15000);
loadErrors();
setInterval(loadErrors,30000);
</script>
</body>
</html>"""
