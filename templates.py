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
.ref-bonus{background:#0a0f1a;border:1px solid #f59e0b44;border-radius:8px;padding:12px;color:#fbbf24;font-size:13px;margin-bottom:20px;text-align:center;display:none}
</style>
</head>
<body>
<div class="card">
  <h1>Create account</h1>
  <p class="sub">Get 10,000 free tokens. No email needed.</p>
  <div class="bonus">Free tier included: 10,000 tokens to try any model</div>
  <div class="ref-bonus" id="ref-bonus">🎉 Referred by a friend — you both get 1,000 bonus tokens + karma!</div>
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
const params=new URLSearchParams(window.location.search);
const ref=params.get('ref');
if(ref){document.getElementById('ref-bonus').style.display='block';}
document.getElementById('form').onsubmit=async e=>{
  e.preventDefault();
  const fd=new FormData(e.target);
  const body={username:fd.get('username'),password:fd.get('password'),email:fd.get('email')};
  if(ref)body.ref=ref;
  try{
    const r=await fetch('/api/auth/signup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
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
body{font-family:-apple-system,system-ui,sans-serif;background:#0d1117;color:#e6edf3;min-height:100vh}
.wrap{max-width:800px;margin:0 auto;padding:24px 20px}
a{color:#58a6ff;text-decoration:none}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid #21262d}
.logo{font-size:20px;font-weight:700}
.logo span{color:#f0883e}
.nav{display:flex;gap:16px}
.nav a{color:#8b949e;font-size:14px;padding:6px 12px;border-radius:6px}
.nav a:hover,.nav a.active{color:#e6edf3;background:#21262d}
.card{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:20px;margin-bottom:16px}
.card h2{font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px}
.stat{text-align:center;padding:16px;background:#0d1117;border:1px solid #21262d;border-radius:8px}
.stat .val{font-size:28px;font-weight:700}
.stat .lbl{font-size:11px;color:#8b949e;margin-top:4px}
.green{color:#3fb950}.orange{color:#d29922}.blue{color:#58a6ff}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:8px 12px;border-bottom:1px solid #21262d;color:#8b949e;font-size:11px;text-transform:uppercase}
td{padding:8px 12px;border-bottom:1px solid #21262d}
.btn{display:inline-block;padding:8px 16px;border-radius:6px;font-size:13px;font-weight:600;border:none;cursor:pointer}
.btn-primary{background:#f0883e;color:#000}.btn-primary:hover{background:#d29922}
.btn-sm{padding:4px 10px;font-size:12px}
.btn-outline{background:transparent;color:#8b949e;border:1px solid #21262d}
.tag{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.tag-g{background:#0d2818;color:#3fb950;border:1px solid #238636}
.tag-r{background:#2d1117;color:#f85149;border:1px solid #da3633}
.tag-o{background:#2d1f00;color:#d29922;border:1px solid #9e6a03}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.key-box{background:#0d1117;border:1px solid #238636;border-radius:6px;padding:10px;font-family:monospace;font-size:12px;word-break:break-all;margin:8px 0}
.inv-box{background:#0d1117;border:1px solid #1f6feb;border-radius:6px;padding:12px;margin-top:12px}
.err-item{padding:10px;border-bottom:1px solid #21262d;font-size:12px}
.err-item:last-child{border:none}
select,input{background:#0d1117;color:#e6edf3;border:1px solid #21262d;border-radius:6px;padding:8px 12px;font-size:13px;width:100%}
select:focus,input:focus{outline:none;border-color:#58a6ff}
.tabcontent{display:none}.tabcontent.active{display:block}
.msg{padding:8px 12px;border-radius:6px;font-size:13px;margin-bottom:12px;display:none}
.msg-ok{background:#0d2818;border:1px solid #238636;color:#3fb950;display:block}
.msg-err{background:#2d1117;border:1px solid #da3633;color:#f85149;display:block}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div class="logo">Volt<span>AI</span></div>
    <div class="nav">
      <a href="#" class="active" onclick="show('overview',this)">Dashboard</a>
      <a href="#" onclick="show('wallet',this)">Wallet</a>
      <a href="#" onclick="show('keys',this)">API Keys</a>
      <a href="#" onclick="show('models',this)">Models</a>
      <a href="#" onclick="show('errors',this)">Errors</a>
      <a href="/api/auth/logout" style="color:#8b949e">Logout</a>
    </div>
  </div>

  <!-- Overview -->
  <div id="overview" class="tabcontent active">
    <div class="row">
      <div class="stat"><div class="val green" id="credits">—</div><div class="lbl">Balance (sats)</div></div>
      <div class="stat"><div class="val orange" id="today">—</div><div class="lbl">Today (tokens)</div></div>
      <div class="stat"><div class="val blue" id="used">—</div><div class="lbl">All time (tokens)</div></div>
    </div>
    <div class="card">
      <h2>Gateway</h2>
      <table>
        <tr><td>Status</td><td><span class="tag tag-g">Connected</span></td></tr>
        <tr><td>Endpoint</td><td style="font-family:monospace;font-size:12px">localhost:11434</td></tr>
        <tr><td>Models</td><td id="gw-models">7 models</td></tr>
        <tr><td>Pricing</td><td>50 sats / 1M tokens</td></tr>
      </table>
    </div>
    <div class="card">
      <h2>Quick Start</h2>
      <div style="font-size:13px;color:#8b949e;line-height:2">
        <div>1. Copy your API key from the <a href="#" onclick="show('keys',this)">Keys</a> tab</div>
        <div>2. Add sats via Lightning in the <a href="#" onclick="show('wallet',this)">Wallet</a> tab</div>
        <div>3. Use the OpenAI-compatible API at <code style="color:#58a6ff">/v1/chat/completions</code></div>
      </div>
    </div>
  </div>

  <!-- Wallet -->
  <div id="wallet" class="tabcontent">
    <div class="grid2">
      <div class="card">
        <h2>Buy Credits</h2>
        <div style="margin-bottom:12px">
          <label style="font-size:12px;color:#8b949e;display:block;margin-bottom:4px">Select key</label>
          <select id="buy-key"><option value="">Select key...</option></select>
        </div>
        <div style="margin-bottom:14px">
          <label style="font-size:12px;color:#8b949e;display:block;margin-bottom:4px">Amount</label>
          <select id="buy-amount">
            <option value="100">100 sats</option>
            <option value="500">500 sats</option>
            <option value="1000">1,000 sats</option>
            <option value="5000">5,000 sats</option>
          </select>
        </div>
        <button class="btn btn-primary" onclick="buyCredits()" style="width:100%">Pay with Lightning</button>
        <div id="invoice-area"></div>
      </div>
      <div class="card">
        <h2>Info</h2>
        <table>
          <tr><td>Rate</td><td id="price-display">50 sats / 1M</td></tr>
          <tr><td>Network</td><td><span class="tag tag-g">Lightning</span></td></tr>
          <tr><td>Min top-up</td><td>100 sats</td></tr>
          <tr><td>Payout</td><td id="ln-addr-display">—</td></tr>
        </table>
      </div>
    </div>
  </div>

  <!-- Keys -->
  <div id="keys" class="tabcontent">
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <h2 style="margin:0">API Keys</h2>
        <button class="btn btn-primary btn-sm" onclick="document.getElementById('new-key-form').style.display='block'">+ New Key</button>
      </div>
      <div id="new-key-form" style="display:none;margin-bottom:12px">
        <div style="display:flex;gap:8px;max-width:300px">
          <input id="key-name" placeholder="Key name (optional)">
          <button class="btn btn-primary btn-sm" onclick="createKey()">Create</button>
        </div>
      </div>
      <div id="new-key-display" style="display:none"></div>
      <table>
        <thead><tr><th>Key</th><th>Name</th><th>Balance</th><th>Used</th><th>Last used</th><th></th></tr></thead>
        <tbody id="keys-table"></tbody>
      </table>
    </div>
  </div>

  <!-- Models -->
  <div id="models" class="tabcontent">
    <div class="card">
      <h2>Available Models</h2>
      <table>
        <thead><tr><th>Model</th><th>VRAM</th><th>Price</th></tr></thead>
        <tbody id="models-table"></tbody>
      </table>
    </div>
  </div>

  <!-- Errors -->
  <div id="errors" class="tabcontent">
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <h2 style="margin:0">Errors <span id="error-count" class="tag tag-r">0</span></h2>
        <button class="btn btn-sm btn-outline" onclick="clearErrors()">Clear</button>
      </div>
      <div id="error-console"><div style="color:#8b949e;font-size:13px;padding:20px;text-align:center">No errors</div></div>
    </div>
  </div>
</div>

<script>
var data={user:{username:''},keys:[],stats:{total_credits:0,total_used:0,today_tokens:0},usage_7d:[]};
var MODEL_LIST=[
  {name:'qwen3.5:4b',vram:'3 GB',price:20},
  {name:'qwen2.5:7b',vram:'5 GB',price:30},
  {name:'deepseek-r1:8b',vram:'5 GB',price:30},
  {name:'qwen2.5-coder:7b',vram:'5 GB',price:30},
  {name:'qwen3.5:9b',vram:'7 GB',price:40},
  {name:'qwen2.5:14b',vram:'10 GB',price:50},
  {name:'qwen3.6:27b',vram:'17 GB',price:80}
];

function show(name,el){
  document.querySelectorAll('.tabcontent').forEach(function(t){t.classList.remove('active')});
  var tab=document.getElementById(name);
  if(tab)tab.classList.add('active');
  document.querySelectorAll('.nav a').forEach(function(a){a.classList.remove('active')});
  if(el)el.classList.add('active');
}

async function load(){
  try{
    var r=await fetch('/api/me');
    if(!r.ok)return;
    data=await r.json();
    render();
  }catch(e){}
}

function render(){
  if(!data||!data.user)return;
  document.getElementById('credits').textContent=(data.stats.total_credits||0).toLocaleString();
  document.getElementById('today').textContent=(data.stats.today_tokens||0).toLocaleString();
  document.getElementById('used').textContent=(data.stats.total_used||0).toLocaleString();
  if(data.ln_address)document.getElementById('ln-addr-display').textContent=data.ln_address;
  if(data.price_per_m)document.getElementById('price-display').textContent=data.price_per_m+' sats / 1M';
  var sl=document.getElementById('buy-key');
  if(data.keys&&data.keys.length){
    sl.innerHTML='<option value="">Select key...</option>'+data.keys.map(function(k){return '<option value="'+k.id+'">'+k.key_prefix+' ('+k.credits+' sats)</option>';}).join('');
    document.getElementById('keys-table').innerHTML=data.keys.map(function(k){return '<tr><td style="font-family:monospace;font-size:12px">'+k.key_prefix+'</td><td>'+k.name+'</td><td class="green">'+k.credits.toLocaleString()+'</td><td>'+k.total_used.toLocaleString()+'</td><td>'+(k.last_used||'Never')+'</td><td><button class="btn btn-sm" style="color:#f85149;background:transparent;border:none" onclick="delKey('+k.id+')">x</button></td></tr>';}).join('');
  }
  document.getElementById('models-table').innerHTML=MODEL_LIST.map(function(m){return '<tr><td>'+m.name+'</td><td>'+m.vram+'</td><td class="green">'+m.price+' sats/M</td></tr>';}).join('');
}

async function createKey(){
  var name=document.getElementById('key-name').value||'Default';
  var r=await(await fetch('/api/keys',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name})})).json();
  document.getElementById('new-key-form').style.display='none';
  document.getElementById('new-key-display').style.display='block';
  document.getElementById('new-key-display').innerHTML='<div class="key-box"><div style="color:#3fb950;font-weight:600;margin-bottom:4px">Key created</div><div>'+r.key+'</div><div style="color:#8b949e;font-size:11px;margin-top:4px">Copy this now — won\'t be shown again</div></div>';
  document.getElementById('key-name').value='';
  load();
}

async function delKey(id){if(!confirm('Delete?'))return;await fetch('/api/keys/'+id,{method:'DELETE'});load();}

async function buyCredits(){
  var kid=document.getElementById('buy-key').value;
  var sats=parseInt(document.getElementById('buy-amount').value);
  if(!kid){alert('Select a key');return;}
  var r=await fetch('/api/buy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key_id:parseInt(kid),amount_sats:sats})});
  var d=await r.json();
  if(!r.ok){alert(d.detail||'Error');return;}
  document.getElementById('invoice-area').innerHTML='<div class="inv-box"><div style="font-weight:600;color:#58a6ff;margin-bottom:8px">'+d.amount_sats+' sats invoice</div><div style="font-size:12px;margin-bottom:8px">Tokens: '+d.tokens.toLocaleString()+'</div><div style="background:#0d1117;padding:10px;border-radius:4px;font-family:monospace;font-size:11px;word-break:break-all">'+d.invoice+'</div><div style="display:flex;gap:8px;margin-top:8px"><button class="btn btn-sm btn-primary" onclick="copyInv(this,\\''+d.invoice+'\\')">Copy</button><button class="btn btn-sm btn-outline" onclick="checkPay(\\''+d.payment_hash+'\\')">Check</button></div><div id="pay-status" style="margin-top:8px;font-size:12px;color:#8b949e">Waiting...</div></div>';
  pollPayment(d.payment_hash);
}

function copyInv(btn,inv){navigator.clipboard.writeText(inv);btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy';},1500);}

var pollTimer=null;
function pollPayment(hash){
  if(pollTimer)clearInterval(pollTimer);
  pollTimer=setInterval(async function(){
    try{
      var r=await(await fetch('/api/invoice/'+hash+'/status')).json();
      if(r.status==='paid'){clearInterval(pollTimer);document.getElementById('pay-status').innerHTML='<span style="color:#3fb950;font-weight:600">Paid!</span>';load();}
    }catch(e){}
  },3000);
}

async function checkPay(hash){
  var r=await(await fetch('/api/invoice/'+hash+'/status')).json();
  if(r.status==='paid'){if(pollTimer)clearInterval(pollTimer);document.getElementById('pay-status').innerHTML='<span style="color:#3fb950;font-weight:600">Paid!</span>';load();}
}

async function loadErrors(){
  try{
    var r=await fetch('/api/errors?limit=50');
    if(!r.ok)return;
    var d=await r.json();
    var el=document.getElementById('error-console');
    var count=document.getElementById('error-count');
    if(!d.errors.length){el.innerHTML='<div style="color:#8b949e;font-size:13px;padding:20px;text-align:center">No errors</div>';count.textContent='0';return;}
    count.textContent=d.errors.length;
    el.innerHTML=d.errors.map(function(e){return '<div class="err-item"><span class="tag '+(e.status_code>=500?'tag-r':'tag-o')+'">'+e.status_code+'</span> <span style="color:#d29922">'+e.method+'</span> '+e.endpoint+'<div style="color:#8b949e;margin-top:4px">'+e.error_msg+'</div></div>';}).join('');
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
