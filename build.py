# Tiny generator: python3 build.py -> writes *.html from PAGES below. Output is committed; no build step needed to deploy.
import html
NAV=[("index.html","Getting started"),("authentication.html","Authentication"),("endpoints.html","Endpoints"),("pagination.html","Pagination"),("errors.html","Errors"),("webhooks.html","Webhooks"),("changelog.html","Changelog")]
BASE="https://brazen-raven-302.convex.site"
def code(s,lang=""): return f'<pre><code class="{lang}">{html.escape(s.strip())}</code></pre>'
def page(fn,title,body):
    nav="".join(f'<a href="{h}"{" class=\"active\"" if h==fn else ""}>{t}</a>' for h,t in NAV)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · FactoraERP Developers</title><meta name="description" content="FactoraERP public API and webhooks documentation.">
<link rel="stylesheet" href="assets/style.css"><link rel="icon" href="assets/favicon.svg"></head><body>
<header class="top"><a class="brand" href="index.html"><img src="assets/favicon.svg" alt="" width="26" height="26"> FactoraERP <span>Developers</span></a><a class="ext" href="https://factoraerp.com">factoraerp.com →</a></header>
<div class="wrap"><nav class="side">{nav}</nav><main><h1>{title}</h1>{body}
<footer>© Tamalaki Business Network Ltd · FactoraERP API v1</footer></main></div></body></html>'''
P={}
P["index.html"]=("Getting started",f'''
<p class="lead">The FactoraERP API gives your systems read-only access to one factory's customers, inventory items and sales invoices, plus signed webhooks for key events.</p>
<div class="note">API v1 is <b>read-only</b>. Webhook delivery is currently in <b>dry-run mode</b>: events are signed and logged but not sent.</div>
<h2>Base URL</h2>
<table><tr><th>Status</th><th>URL</th></tr><tr><td>Current</td><td><code>{BASE}</code></td></tr><tr><td>Coming soon</td><td><code>https://api.factoraerp.com</code></td></tr></table>
<h2>Quick start</h2>
<ol><li>A factory admin (Admin, CEO/Director or General Manager role) opens <b>System Settings → API access</b> in FactoraERP.</li>
<li>They create a key, choose its scopes and expiry, and copy it. The key starts with <code>fxk_</code> and is <b>shown only once</b>.</li>
<li>Call the API with the key in a header:</li></ol>
{code(f'curl -H "Authorization: Bearer $FACTORA_API_KEY" {BASE}/api/v1/me',"sh")}
{code('{"ok":true,"organizationId":"<factory id>","scopes":["read:customers","read:sales"]}',"json")}
<h2>What's available</h2>
<table><tr><th>Endpoint</th><th>Scope</th></tr>
<tr><td><code>GET /api/v1/me</code></td><td>any valid key</td></tr>
<tr><td><code>GET /api/v1/customers</code></td><td><code>read:customers</code></td></tr>
<tr><td><code>GET /api/v1/inventory-items</code></td><td><code>read:inventory</code></td></tr>
<tr><td><code>GET /api/v1/sales-invoices</code></td><td><code>read:sales</code></td></tr></table>
<p>The API is designed for server-to-server use. It sends no CORS headers, so browsers will block calls from web pages. Keep keys on your server.</p>''')
P["authentication.html"]=("Authentication",f'''
<h2>API keys</h2>
<ul><li>Format: <code>fxk_</code> followed by 48 hex characters.</li>
<li>Created and revoked by factory admins in <b>System Settings → API access</b>.</li>
<li>Shown once at creation. FactoraERP stores only a SHA-256 hash and the first 12 characters (for example <code>fxk_1a2b3c4d</code>) so you can tell keys apart. A lost key can't be recovered: revoke it and create a new one.</li>
<li>Each key belongs to one factory and can only read that factory's data.</li>
<li>Up to 20 active keys per factory.</li>
<li>Expiry: 30, 90 (default) or 365 days, or never. Expired and revoked keys stop working immediately.</li>
<li>The admin screen shows when a key was last used (updated at most once an hour).</li></ul>
<h2>Scopes</h2>
<table><tr><th>Scope</th><th>Grants</th></tr><tr><td><code>read:customers</code></td><td><code>GET /api/v1/customers</code></td></tr><tr><td><code>read:inventory</code></td><td><code>GET /api/v1/inventory-items</code></td></tr><tr><td><code>read:sales</code></td><td><code>GET /api/v1/sales-invoices</code></td></tr></table>
<h2>Sending the key</h2>
<p>Use either header:</p>
{code(f'''curl -H "Authorization: Bearer fxk_..." {BASE}/api/v1/me
curl -H "X-API-Key: fxk_..." {BASE}/api/v1/me''',"sh")}
<p>If both are present, <code>Authorization</code> wins. Never put the key in the URL: a request with an <code>api_key</code> query parameter is refused with 401 so keys don't leak into logs.</p>
<h2>Keeping keys safe</h2>
<ul><li>Store keys in a secrets manager or environment variable, never in source code or front-end apps.</li><li>Give each integration its own key with only the scopes it needs.</li><li>Prefer an expiry and rotate keys before they lapse.</li></ul>''')
def fields(rows): return "<table><tr><th>Field</th><th>Notes</th></tr>"+"".join(f"<tr><td><code>{a}</code></td><td>{b}</td></tr>" for a,b in rows)+"</table>"
COMMON=[("id","FactoraERP record id"),("_creationTime","Creation time, ms since epoch. Used for paging.")]
P["endpoints.html"]=("Endpoints",f'''
<p>All endpoints are <code>GET</code>, return JSON with <code>Cache-Control: no-store</code>, and return the newest records first. List endpoints accept <code>limit</code> and <code>before</code> (see <a href="pagination.html">Pagination</a>). A field is omitted when the record has no value for it.</p>
<h2 id="me">GET /api/v1/me</h2><p>Checks a key and shows what it can do.</p>
{code('{"ok":true,"organizationId":"<factory id>","scopes":["read:customers"]}',"json")}
<h2 id="customers">GET /api/v1/customers</h2><p>Scope <code>read:customers</code>.</p>
{fields([COMMON[0],("customerCode",""),("name",""),("email",""),("phone",""),("taxPin","KRA PIN"),("status",""),COMMON[1]])}
<h2 id="inventory">GET /api/v1/inventory-items</h2><p>Scope <code>read:inventory</code>.</p>
{fields([COMMON[0],("code",""),("name",""),("unit",""),("category",""),("isActive","boolean"),("currentStock","number"),("reorderLevel","number"),COMMON[1]])}
<h2 id="sales">GET /api/v1/sales-invoices</h2><p>Scope <code>read:sales</code>.</p>
{fields([COMMON[0],("invoiceNumber",""),("buyerName",""),("issuedDate",""),("dueDate",""),("status",""),("currency",""),("totalAmount","number"),("amountPaid","number"),("etimsStatus","KRA eTIMS submission status"),COMMON[1]])}
<h2>Example</h2>
{code(f'curl -H "X-API-Key: $FACTORA_API_KEY" "{BASE}/api/v1/sales-invoices?limit=2"',"sh")}
{code('''{
  "ok": true,
  "data": [
    {"id": "<id>", "invoiceNumber": "<number>", "buyerName": "<name>", "status": "<status>", "currency": "KES", "totalAmount": 0, "amountPaid": 0, "_creationTime": 1793000000000.0},
    {"id": "<id>", "invoiceNumber": "<number>", "...": "...", "_creationTime": 1792900000000.0}
  ],
  "nextBefore": 1792900000000.0
}''',"json")}
<p class="muted">Values above are placeholders, not real data.</p>''')
P["pagination.html"]=("Pagination",f'''
<table><tr><th>Parameter</th><th>Default</th><th>Notes</th></tr>
<tr><td><code>limit</code></td><td>50</td><td>Rounded down and clamped to 1–200.</td></tr>
<tr><td><code>before</code></td><td>none</td><td>Return records created strictly before this <code>_creationTime</code>.</td></tr></table>
<p>Each list response has <code>nextBefore</code>. When it is a number, pass it as <code>before</code> to get the next page. When it is <code>null</code>, you've reached the end. <code>nextBefore</code> is set whenever a page is full, so the last page can occasionally be empty.</p>
<p>Non-numeric <code>limit</code> or <code>before</code> returns 400.</p>
{code(f"""// Node 18+
const base = "{BASE}/api/v1/customers";
let before = null, all = [];
do {{
  const url = before ? `${{base}}?limit=200&before=${{before}}` : `${{base}}?limit=200`;
  const res = await fetch(url, {{ headers: {{ Authorization: `Bearer ${{process.env.FACTORA_API_KEY}}` }} }});
  const page = await res.json();
  if (!page.ok) throw new Error(page.error);
  all.push(...page.data);
  before = page.nextBefore;
}} while (before !== null);""","js")}''')
P["errors.html"]=("Errors",'''
<p>Errors return a JSON body of <code>{"ok": false, "error": "&lt;message&gt;"}</code>.</p>
<table><tr><th>Status</th><th><code>error</code></th><th>Cause</th></tr>
<tr><td>401</td><td>Missing API key</td><td>No key, or the value doesn't start with <code>fxk_</code>.</td></tr>
<tr><td>401</td><td>Send the key in the Authorization (Bearer) or X-API-Key header</td><td>The request had an <code>api_key</code> query parameter.</td></tr>
<tr><td>401</td><td>Invalid, expired or revoked API key</td><td>Unknown, expired or revoked key.</td></tr>
<tr><td>403</td><td>This key lacks the read:… scope</td><td>The key lacks the scope for this endpoint.</td></tr>
<tr><td>400</td><td>limit and before must be numbers</td><td>Bad paging parameters.</td></tr>
<tr><td>404</td><td>Not found</td><td>Unknown resource.</td></tr></table>
<p>Requests to paths outside the four documented endpoints may get a plain-text 404 from the platform rather than JSON. Unexpected server errors return 5xx; retry with backoff.</p>''')
NODE='''import crypto from "node:crypto";
import express from "express";

const app = express();
// Use the raw body: the signature covers the exact bytes sent.
app.post("/factora/webhook", express.raw({ type: "application/json" }), (req, res) => {
  const header = req.get("X-Factora-Signature") || "";
  const parts = Object.fromEntries(header.split(",").map((p) => p.split("=")));
  const t = parts.t, v1 = parts.v1 || "";
  const body = req.body.toString("utf8");
  const expected = crypto
    .createHmac("sha256", process.env.FACTORA_WEBHOOK_SECRET) // whsec_...
    .update(`${t}.${body}`)
    .digest("hex");
  const ok = v1.length === expected.length &&
    crypto.timingSafeEqual(Buffer.from(v1), Buffer.from(expected));
  const fresh = Math.abs(Date.now() / 1000 - Number(t)) < 300; // 5-minute tolerance
  if (!ok || !fresh) return res.status(400).send("bad signature");
  const event = JSON.parse(body);
  console.log(event.event, event.data);
  res.sendStatus(200);
});
app.listen(3000);'''
PY='''import hashlib, hmac, os, time
from flask import Flask, request, abort

app = Flask(__name__)
SECRET = os.environ["FACTORA_WEBHOOK_SECRET"].encode()  # whsec_...

@app.post("/factora/webhook")
def webhook():
    header = request.headers.get("X-Factora-Signature", "")
    parts = dict(p.split("=", 1) for p in header.split(",") if "=" in p)
    t, v1 = parts.get("t", ""), parts.get("v1", "")
    body = request.get_data(as_text=True)  # raw body, unmodified
    expected = hmac.new(SECRET, f"{t}.{body}".encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(v1, expected):
        abort(400)
    if not t.isdigit() or abs(time.time() - int(t)) > 300:
        abort(400)
    event = request.get_json()
    print(event["event"], event["data"])
    return "", 200'''
P["webhooks.html"]=("Webhooks",f'''
<div class="note"><b>Dry-run mode.</b> Webhook delivery is not switched on yet. Each event is signed and recorded in the delivery log in System Settings → API access with status <code>DRY RUN</code>, but nothing is sent to your URL. You can build and test your receiver now with the examples below.</div>
<h2>Endpoints</h2>
<ul><li>Admins add a webhook URL in <b>System Settings → API access</b> and choose its events. The URL must be a public <code>https://</code> address.</li>
<li>A signing secret starting with <code>whsec_</code> is shown <b>once</b>. Afterwards only its first 8 characters are shown.</li>
<li>New endpoints start switched off; admins switch each one on. Up to 10 active endpoints per factory.</li>
<li><b>Send test</b> emits a <code>test.ping</code> event.</li></ul>
<h2>Events</h2>
<table><tr><th>Event</th><th>Status</th></tr>
<tr><td><code>test.ping</code></td><td>Available (from Send test). <code>data</code> is <code>{{"hello":"factora"}}</code>.</td></tr>
<tr><td><code>sales_invoice.created</code></td><td>Reserved, not emitted yet</td></tr>
<tr><td><code>sales_invoice.paid</code></td><td>Reserved, not emitted yet</td></tr>
<tr><td><code>work_order.completed</code></td><td>Reserved, not emitted yet</td></tr></table>
<h2>Request</h2>
<p>When delivery is live, FactoraERP sends a <code>POST</code> with a 10-second timeout and these headers:</p>
{code('''Content-Type: application/json
X-Factora-Event: test.ping
X-Factora-Signature: t=1793000000,v1=5f2b...e9''')}
{code('{"event":"test.ping","createdAt":"2026-10-31T09:00:00.000Z","data":{"hello":"factora"}}',"json")}
<p>Respond with any 2xx status to mark the delivery sent. Anything else, or a timeout, marks it failed. There are no automatic retries at the moment.</p>
<h2>Verifying the signature</h2>
<ol><li>Split <code>X-Factora-Signature</code> on commas to get <code>t</code> (Unix seconds) and <code>v1</code>.</li>
<li>Build the signed string: <code>t + "." + rawBody</code>, where <code>rawBody</code> is the exact request body.</li>
<li>Compute HMAC-SHA256 of that string with your <code>whsec_…</code> secret (the whole string, prefix included) as the key, hex-encoded in lowercase.</li>
<li>Compare with <code>v1</code> in constant time, and reject old timestamps (we suggest 5 minutes).</li></ol>
<h3>Node.js</h3>{code(NODE,"js")}
<h3>Python</h3>{code(PY,"py")}''')
P["changelog.html"]=("Changelog",'''
<h2>v1 · October 2026</h2>
<ul><li>Per-factory API keys (<code>fxk_</code>) with scopes, expiry and revocation.</li>
<li>Read-only endpoints: <code>/api/v1/me</code>, <code>/customers</code>, <code>/inventory-items</code>, <code>/sales-invoices</code>, with <code>limit</code>/<code>before</code> paging.</li>
<li>Signed webhooks (<code>X-Factora-Signature</code>, HMAC-SHA256), in dry-run mode.</li></ul>
<h2>Coming soon</h2><ul><li><code>https://api.factoraerp.com</code> base URL.</li><li>Live webhook delivery and the sales invoice and work order events.</li></ul>''')
for fn,(t,b) in P.items(): open(fn,"w").write(page(fn,t,b))
open("404.html","w").write(page("","Page not found",'<p>That page doesn\'t exist. <a href="index.html">Back to getting started</a>.</p>'))
